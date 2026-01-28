from pypdf import PdfReader
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

def load_pdf(filename: str) -> str:
    pdf_path = DATA_DIR / filename

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"

    return text


def load_txt(filename: str) -> str:
    txt_path = DATA_DIR / filename

    if not txt_path.exists():
        raise FileNotFoundError(f"Text file not found: {txt_path}")

    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read()
