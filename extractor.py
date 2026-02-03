from pypdf import PdfReader
from docx import Document

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    
    for para in doc.paragraphs:
        text += para.text + "\n"
        
    return text


def extract_resume_text(file_path):
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
        
    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
        
    else:
        raise ValueError("Unsupported file format")