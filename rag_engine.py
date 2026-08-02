from __future__ import annotations

import re
import uuid
from pathlib import Path
from typing import Any

import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer


class PersonalRAG:
    """Core embedding, storage and retrieval logic."""

    def __init__(
        self,
        database_path: str = "./chroma_data",
        collection_name: str = "personal_information",
    ) -> None:
        self.database_path = Path(database_path)
        self.database_path.mkdir(parents=True, exist_ok=True)

        # Downloads the model during the first run.
        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # PersistentClient saves the vector database locally.
        self.client = chromadb.PersistentClient(
            path=str(self.database_path)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    @staticmethod
    def clean_text(text: str) -> str:
        """Remove unnecessary spaces and empty lines."""
        text = text.strip()
        text = re.sub(r"\r\n?", "\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 100,
        overlap: int = 20,
    ) -> list[str]:
        """
        Split text into word-based chunks.

        Example:
        chunk_size=100 means around 100 words in each chunk.
        overlap=20 repeats the previous 20 words in the next chunk.
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        if overlap < 0:
            raise ValueError("overlap cannot be negative.")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size.")

        words = text.split()

        if not words:
            return []

        chunks: list[str] = []
        start = 0

        while start < len(words):
            end = start + chunk_size
            chunk = " ".join(words[start:end]).strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(words):
                break

            start = end - overlap

        return chunks

    def create_embeddings(
        self,
        texts: list[str],
    ) -> np.ndarray:
        """Convert text chunks into normalized embeddings."""
        if not texts:
            return np.empty((0, 0))

        embeddings = self.embedding_model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return np.asarray(embeddings)

    def store_text(
        self,
        text: str,
        title: str = "Manual information",
        category: str = "General",
        chunk_size: int = 100,
        overlap: int = 20,
    ) -> dict[str, Any]:
        """Clean, chunk, embed and store information."""

        cleaned_text = self.clean_text(text)

        if not cleaned_text:
            raise ValueError("Please enter some information.")

        chunks = self.chunk_text(
            text=cleaned_text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        embeddings = self.create_embeddings(chunks)

        document_id = str(uuid.uuid4())

        ids = [
            f"{document_id}_chunk_{index + 1}"
            for index in range(len(chunks))
        ]

        metadata = [
            {
                "document_id": document_id,
                "title": title,
                "category": category,
                "chunk_number": index + 1,
                "total_chunks": len(chunks),
                "source": "manual_input",
            }
            for index in range(len(chunks))
        ]

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=metadata,
        )

        return {
            "document_id": document_id,
            "ids": ids,
            "chunks": chunks,
            "embeddings": embeddings,
            "metadata": metadata,
        }

    def search(
        self,
        question: str,
        number_of_results: int = 3,
    ) -> dict[str, Any]:
        """Search ChromaDB using the question embedding."""

        cleaned_question = self.clean_text(question)

        if not cleaned_question:
            raise ValueError("Please enter a question.")

        if self.collection.count() == 0:
            raise ValueError(
                "The vector database is empty. Add information first."
            )

        query_embedding = self.create_embeddings(
            [cleaned_question]
        )[0]

        maximum_results = min(
            number_of_results,
            self.collection.count(),
        )

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=maximum_results,
            include=[
                "documents",
                "metadatas",
                "distances",
                "embeddings",
            ],
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        stored_embeddings = results["embeddings"][0]

        matches: list[dict[str, Any]] = []

        for index, document in enumerate(documents):
            stored_vector = np.asarray(stored_embeddings[index])

            # Embeddings were normalized, so dot product gives cosine similarity.
            cosine_score = float(
                np.dot(query_embedding, stored_vector)
            )

            matches.append(
                {
                    "text": document,
                    "metadata": metadatas[index],
                    "database_distance": float(distances[index]),
                    "cosine_similarity": cosine_score,
                }
            )

        # Highest cosine similarity first.
        matches.sort(
            key=lambda item: item["cosine_similarity"],
            reverse=True,
        )

        context = "\n\n".join(
            match["text"] for match in matches
        )

        return {
            "question": cleaned_question,
            "query_embedding": query_embedding,
            "matches": matches,
            "context": context,
        }

    def get_all_records(self) -> dict[str, Any]:
        """Return every record currently stored in ChromaDB."""
        return self.collection.get(
            include=[
                "documents",
                "metadatas",
                "embeddings",
            ]
        )

    def database_count(self) -> int:
        """Return the number of stored chunks."""
        return self.collection.count()

    def clear_database(self) -> None:
        """Delete and recreate the personal-information collection."""
        collection_name = self.collection.name

        self.client.delete_collection(
            name=collection_name
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )