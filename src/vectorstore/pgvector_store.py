import psycopg2
import psycopg2.extras
from typing import List, Tuple
from langchain_core.documents import Document
from .base_store import BaseVectorStore
import json

class PGVectorStore(BaseVectorStore):

    def __init__(self, conn_str: str, embedding_dim: int = 768, table_name: str = "documents"):
        self.conn_str = conn_str
        self.table_name = table_name
        self.embedding_dim = embedding_dim
        self._connect()

    def _connect(self):
        self.conn = psycopg2.connect(self.conn_str)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def create_collection(self):
        create_sql = f"""
            CREATE EXTENSION IF NOT EXISTS vector;

            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id TEXT PRIMARY KEY,
                content TEXT,
                metadata JSONB,
                embedding vector({self.embedding_dim})
            );
        """
        self.cursor.execute(create_sql)

    def upsert(self, docs: List[Document], embeddings: List[List[float]]):
        sql = f"""
            INSERT INTO {self.table_name} (id, content, metadata, embedding)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                content = EXCLUDED.content,
                metadata = EXCLUDED.metadata,
                embedding = EXCLUDED.embedding;
        """

        for doc, emb in zip(docs, embeddings):
            self.cursor.execute(
                sql,
                (
                    doc.metadata.get("id", doc.metadata.get("source", "unknown") + "_" + str(hash(doc.page_content))),
                    doc.page_content,
                    json.dumps(doc.metadata),
                    emb
                )
            )

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[Document, float]]:
        # pgvector requires embedding to be passed as a string cast to vector
        emb_str = "[" + ",".join([str(x) for x in query_embedding]) + "]"

        sql = f"""
            SELECT id, content, metadata, embedding <-> %s::vector AS score
            FROM {self.table_name}
            ORDER BY embedding <-> %s::vector
            LIMIT {top_k};
        """

        self.cursor.execute(sql, (emb_str, emb_str))
        rows = self.cursor.fetchall()

        results = []
        for row in rows:
            doc = Document(page_content=row[1], metadata=row[2])
            score = row[3]
            results.append((doc, score))

        return results

    def delete(self, doc_id: str):
        self.cursor.execute(
            f"DELETE FROM {self.table_name} WHERE id = %s",
            (doc_id,)
        )
