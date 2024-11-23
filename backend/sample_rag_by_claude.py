import google.generativeai as genai
from newspaper import Article
from PyPDF2 import PdfReader
import numpy as np
from typing import List, Dict, Union
import requests
from bs4 import BeautifulSoup
import os
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from collections import defaultdict


class DocumentRAG:
    def __init__(self, google_api_key: str):
        """
        Initialize the RAG system with Google API key for Gemini

        Args:
            google_api_key (str): Google API key for accessing Gemini
        """
        # Configure Gemini
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.embedding_model = genai.GenerativeModel("embedding-001")

        # Initialize NLTK for text processing
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")

        # Storage for documents and embeddings
        self.documents = defaultdict(dict)
        self.document_embeddings = {}

    def _get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding for a piece of text using Gemini

        Args:
            text (str): Text to embed

        Returns:
            np.ndarray: Embedding vector
        """
        try:
            embedding = self.embedding_model.embed_content(text)
            return np.array(embedding.values)
        except Exception as e:
            print(f"Error getting embedding: {str(e)}")
            return None

    def _chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """
        Split text into smaller chunks for processing

        Args:
            text (str): Text to chunk
            chunk_size (int): Maximum size of each chunk

        Returns:
            List[str]: List of text chunks
        """
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            if current_length + len(sentence) > chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_length = len(sentence)
            else:
                current_chunk.append(sentence)
                current_length += len(sentence)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def process_pdf(self, pdf_path: str, doc_id: str = None) -> str:
        """
        Process a PDF document and store its embeddings

        Args:
            pdf_path (str): Path to PDF file
            doc_id (str): Optional document identifier

        Returns:
            str: Document ID
        """
        if doc_id is None:
            doc_id = f"pdf_{len(self.documents)}"

        try:
            # Read PDF
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            # Process the text
            chunks = self._chunk_text(text)
            chunk_embeddings = []

            for i, chunk in enumerate(chunks):
                embedding = self._get_embedding(chunk)
                if embedding is not None:
                    self.documents[doc_id][i] = chunk
                    chunk_embeddings.append(embedding)

            self.document_embeddings[doc_id] = np.vstack(chunk_embeddings)
            return doc_id

        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return None

    def process_url(self, url: str, doc_id: str = None) -> str:
        """
        Process a URL and store its embeddings

        Args:
            url (str): URL to process
            doc_id (str): Optional document identifier

        Returns:
            str: Document ID
        """
        if doc_id is None:
            doc_id = f"url_{len(self.documents)}"

        try:
            # Download and parse article
            article = Article(url)
            article.download()
            article.parse()

            # Process the text
            chunks = self._chunk_text(article.text)
            chunk_embeddings = []

            for i, chunk in enumerate(chunks):
                embedding = self._get_embedding(chunk)
                if embedding is not None:
                    self.documents[doc_id][i] = chunk
                    chunk_embeddings.append(embedding)

            self.document_embeddings[doc_id] = np.vstack(chunk_embeddings)
            return doc_id

        except Exception as e:
            print(f"Error processing URL: {str(e)}")
            return None

    def query(self, query: str, top_k: int = 3) -> List[Dict[str, Union[str, float]]]:
        """
        Query the RAG system

        Args:
            query (str): Query text
            top_k (int): Number of top results to return

        Returns:
            List[Dict]: List of top matching chunks with their scores
        """
        try:
            # Get query embedding
            query_embedding = self._get_embedding(query)
            if query_embedding is None:
                return []

            results = []

            # Search through all documents
            for doc_id in self.documents:
                # Calculate similarities
                similarities = cosine_similarity(
                    query_embedding.reshape(1, -1), self.document_embeddings[doc_id]
                )[0]

                # Get top chunks from this document
                top_indices = np.argsort(similarities)[-top_k:][::-1]

                for idx in top_indices:
                    results.append(
                        {
                            "doc_id": doc_id,
                            "chunk": self.documents[doc_id][idx],
                            "score": float(similarities[idx]),
                        }
                    )

            # Sort all results and return top k
            results.sort(key=lambda x: x["score"], reverse=True)
            return results[:top_k]

        except Exception as e:
            print(f"Error during query: {str(e)}")
            return []

    def generate_response(self, query: str, top_k: int = 3) -> str:
        """
        Generate a response using RAG

        Args:
            query (str): User query
            top_k (int): Number of chunks to consider

        Returns:
            str: Generated response
        """
        # Get relevant chunks
        relevant_chunks = self.query(query, top_k=top_k)

        if not relevant_chunks:
            return "I couldn't find relevant information to answer your query."

        # Prepare context
        context = "\n\n".join([chunk["chunk"] for chunk in relevant_chunks])

        # Generate response using Gemini
        prompt = f"""Based on the following context, please answer the query.
        
Context:
{context}

Query: {query}

Answer:"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "Sorry, I encountered an error while generating the response."
