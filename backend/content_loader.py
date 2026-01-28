from pypdf import PdfReader
from docx import Document

def load_pdf_content(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"

    return text


def load_txt_content(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def load_docx_content(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def load_file_content(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        return load_pdf_content(file_path)
    elif file_path.lower().endswith(".txt"):
        return load_txt_content(file_path)
    elif file_path.lower().endswith(".docx"):
        return load_docx_content(file_path)
    else:
        return ""
