import json
from docx import Document

def load_playbook(path: str):
    with open(path, "r") as f:
        return json.load(f)


def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text).lower()

def split_into_clauses(document_text: str):
    clauses = document_text.split("\n\n")
    return [c.strip() for c in clauses if len(c.strip()) > 50]