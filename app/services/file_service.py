from fastapi import UploadFile
from PyPDF2 import PdfReader
from docx import Document
import io


def extract_text_from_file(uploaded_file: UploadFile) -> str:
    filename = uploaded_file.filename.lower()
    file_bytes = uploaded_file.file.read()
    file_stream = io.BytesIO(file_bytes)

    text = ""

    if filename.endswith(".pdf"):
        reader = PdfReader(file_stream)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    elif filename.endswith(".docx"):
        document = Document(file_stream)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    else:
        raise ValueError("Only PDF and DOCX files are supported.")

    return text.strip()