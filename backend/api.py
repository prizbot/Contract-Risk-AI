from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from backend.utils import load_playbook, extract_text_from_docx
from backend.graph import build_graph

app = FastAPI(title="AI Contract Compliance Engine")

# Allow frontend calls later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

playbook = load_playbook("backend/playbook.json")
graph_app = build_graph()


@app.post("/validate")
async def validate_contract(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document_text = extract_text_from_docx(file_path)

    result = graph_app.invoke({
        "playbook": playbook,
        "document_text": document_text
    })

    return result