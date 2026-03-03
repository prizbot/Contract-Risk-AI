from typing import TypedDict, Dict, Any


class ComplianceState(TypedDict, total=False):
    playbook: Dict[str, Any]
    document_text: str
    validation_result: Dict[str, Any]

    legal_review: str
    finance_review: str
    security_review: str
    executive_decision: str

    approval_status: str