# RAG Knowledge Assistant

A Retrieval-Augmented Generation (RAG) system for semantic document search and AI-powered querying.

## What it does
- Ingests documents (PDF, text) into a Qdrant vector store
- Answers natural language queries using semantic retrieval + LLM
- FastAPI backend with a React frontend

## Stack
Python · FastAPI · Qdrant · LangChain · React

## Run locally
```bash
pip install -r requirements.txt
python bootstrap_db.py   # seed vector store
uvicorn main:app --reload
```
