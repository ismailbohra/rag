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

    def search(self, query_embedding: List[float], top_k: int = 5, metadata_filter: dict = None) -> List[Tuple[Document, float]]:
        # pgvector requires embedding to be passed as a string cast to vector
        emb_str = "[" + ",".join([str(x) for x in query_embedding]) + "]"

        # Build WHERE clause for metadata filtering if provided
        where_clause = ""
        params = [emb_str, emb_str]
        
        if metadata_filter:
            # Support filtering by any metadata key-value pair
            where_clauses = []
            for key, value in metadata_filter.items():
                where_clauses.append(f"(metadata->>'%s') = %%s" % key)
                params.insert(1, str(value))
            where_clause = "WHERE " + " AND ".join(where_clauses) + " "

        sql = f"""
            SELECT id, content, metadata, embedding <-> %s::vector AS score
            FROM {self.table_name}
            {where_clause}
            ORDER BY embedding <-> %s::vector
            LIMIT {top_k};
        """

        self.cursor.execute(sql, tuple(params))
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

    def upsert_chat_embedding(self, chat_id: int, embedding: List[float], metadata: dict = None):
        """
        Upsert embedding for a chat message into the chat_embeddings table.
        
        Args:
            chat_id: ID of the chat message
            embedding: Vector embedding as list of floats
            metadata: Optional JSONB metadata (e.g., session_id, user_id)
        """
        sql = """
            INSERT INTO chat_embeddings (chat_id, embedding, chat_metadata)
            VALUES (%s, %s, %s)
            ON CONFLICT (chat_id) DO UPDATE
              SET embedding = EXCLUDED.embedding,
                  chat_metadata = EXCLUDED.chat_metadata;
        """
        self.cursor.execute(
            sql,
            (chat_id, embedding, json.dumps(metadata or {}))
        )

    def search_chat_embeddings(self, query_embedding: List[float], top_k: int = 5, session_id: int = None) -> List[Tuple[str, float]]:
        """
        Search chat embeddings with optional session filtering.
        
        Args:
            query_embedding: Query vector as list of floats
            top_k: Number of results to return
            session_id: Optional session ID to filter results
        
        Returns:
            List of tuples (chat_message_content, similarity_score)
        """
        where_clause = ""
        params = [query_embedding]
        
        if session_id:
            where_clause = "WHERE (ce.chat_metadata->>'session_id') = %s "
            params.insert(0, str(session_id))

        sql = f"""
            SELECT c.content, ce.embedding <-> %s AS score
            FROM chat_embeddings ce
            JOIN chats c ON ce.chat_id = c.id
            {where_clause}
            ORDER BY ce.embedding <-> %s
            LIMIT %s;
        """
        
        params.append(query_embedding)
        params.append(top_k)
        
        self.cursor.execute(sql, tuple(params))
        rows = self.cursor.fetchall()

        results = [(row[0], row[1]) for row in rows]
        return results
