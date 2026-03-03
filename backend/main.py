from utils import load_playbook, extract_text_from_docx
from graph import build_graph

if __name__ == "__main__":

    playbook = load_playbook("backend/playbook.json")

    #document_text = extract_text_from_docx("data/msa.docx")
    #document_text = extract_text_from_docx("data/msa_medium_risk.docx")
    document_text = extract_text_from_docx("data/msa_high_risk.docx")

    app = build_graph()

    result = app.invoke({
        "playbook": playbook,
        "document_text": document_text
    })

    print("\n--- WORKFLOW OUTPUT ---\n")
    print(result)