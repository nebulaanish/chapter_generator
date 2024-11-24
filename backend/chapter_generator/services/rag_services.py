from django.conf import settings
from chapter_generator.services.textparser_services import TextParser
import pytesseract
from pdf2image import convert_from_path
import pypdf
import requests
from newspaper import Article
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.schema.embeddings import Embeddings
import google.generativeai as genai
import numpy as np
import os


class GeminiEmbeddings(Embeddings):
    def __init__(self, api_key=settings.GEMINI_API_KEY):
        genai.configure(api_key=api_key)
        self.model = "models/text-embedding-004"

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            try:
                result = genai.embed_content(model=self.model, content=text)
                embeddings.append(result["embedding"])
            except Exception as e:
                print(f"Error embedding document: {e}")
                embeddings.append([0] * 768)  # fallback for error cases
        return embeddings

    def embed_query(self, text):
        try:
            result = genai.embed_content(model=self.model, content=text)
            return result["embedding"]
        except Exception as e:
            print(f"Error embedding query: {e}")
            return [0] * 768  # fallback for error cases


class RAGSystem:
    def __init__(self, api_key=settings.GEMINI_API_KEY):
        self.text_parser = TextParser()
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")
        self.embeddings = GeminiEmbeddings(api_key)
        self.vector_store = None

    def load_document(self, source, source_type="url"):
        try:
            if source_type == "url":
                texts = self.text_parser.extract_from_url(source)
            else:
                texts = self.text_parser.extract_from_pdf(source)

            if not texts:
                print("No text extracted from document")
                return

            documents = [Document(page_content=text) for text in texts]

            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
            else:
                self.vector_store.add_documents(documents)

            print(f"Successfully processed {len(texts)} text chunks")

        except Exception as e:
            print(f"Error loading document: {e}")

    def query(self, query_text, k=3):
        try:
            if not self.vector_store:
                print("Vector store not initialized")
                return []
            return self.vector_store.similarity_search(query_text, k=k)
        except Exception as e:
            print(f"Error during query: {e}")
            return []

    def get_response(self, query_text, k=3):
        try:
            relevant_docs = self.query(query_text, k)
            if not relevant_docs:
                return "No relevant documents found."

            context = "\n".join([doc.page_content for doc in relevant_docs])
            prompt = f"Context: {context}\nQuestion: {query_text}\nAnswer:"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error getting response: {e}")
            return "Error generating response"

    def save_index(self, folder_path):
        try:
            if self.vector_store:
                os.makedirs(folder_path, exist_ok=True)
                self.vector_store.save_local(folder_path)
                print(f"Index saved to {folder_path}")
        except Exception as e:
            print(f"Error saving index: {e}")

    def load_index(self, folder_path):
        try:
            if os.path.exists(folder_path):
                self.vector_store = FAISS.load_local(
                    folder_path, self.embeddings, allow_dangerous_deserialization=True
                )
                print(f"Index loaded from {folder_path}")
            else:
                print(f"No index found at {folder_path}")
        except Exception as e:
            print(f"Error loading index: {e}")

    def get_response_to_prompt(self, query_text, k=3):
        try:
            response = self.model.generate_content(query_text)
            return response.text
        except Exception as e:
            print(f"Error getting response: {e}")
            return "Error generating response"
