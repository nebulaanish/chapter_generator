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


class TextParser:
    def __init__(self, tesseract_path=None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )

    def extract_from_url(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return self.process_text(article.text)
        except Exception as e:
            print(f"Error extracting from URL: {e}")
            return []

    def extract_from_pdf(self, pdf_path):
        try:
            extracted_text = []
            with open(pdf_path, "rb") as file:
                pdf_reader = pypdf.PdfReader(file)
                for page in pdf_reader.pages:
                    text = page.extract_text().strip()
                    if len(text) < 10:
                        images = convert_from_path(pdf_path)
                        text = pytesseract.image_to_string(images[0])
                    if text:
                        extracted_text.append(text)
            return self.process_text("\n".join(extracted_text))
        except Exception as e:
            print(f"Error extracting from PDF: {e}")
            return []

    def process_text(self, text):
        if not text:
            return []
        try:
            chunks = self.text_splitter.split_text(text)
            return [chunk for chunk in chunks if len(chunk.strip()) > 0]
        except Exception as e:
            print(f"Error processing text: {e}")
            return []
