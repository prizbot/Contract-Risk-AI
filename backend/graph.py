from langgraph.graph import StateGraph, END
from backend.state import ComplianceState
from backend.validator import validate_document


# -----------------------------
# Node 1: Validation
# -----------------------------
def validation_node(state: ComplianceState) -> ComplianceState:

    result = validate_document(
        state["playbook"],
        state["document_text"]
    )

    return {
        **state,
        "validation_result": result
    }


# -----------------------------
# Risk Decision Logic
# -----------------------------
def risk_decision_node(state: ComplianceState) -> str:

    result = state["validation_result"]
    score = result.get("total_risk_score", 0)

    # If any LLM result says High → escalate
    for item in result.get("llm_analysis", []):
        if item["llm_result"].get("risk_level") == "High":
            return "high_risk"

    if score == 0:
        return "low_risk"
    elif score <= 10:
        return "medium_risk"
    else:
        return "high_risk"


# -----------------------------
# Standard Low-Risk Approval
# -----------------------------
def standard_approval_node(state: ComplianceState) -> ComplianceState:
    return {
        **state,
        "approval_status": "Auto-approved (Low Risk)."
    }


# -----------------------------
# Legal Review (Medium + High)
# -----------------------------
def legal_review_node(state: ComplianceState) -> ComplianceState:

    score = state["validation_result"].get("total_risk_score", 0)

    if score <= 10:
        # Medium risk ends here
        return {
            **state,
            "legal_review": "Legal review completed (Medium Risk).",
            "approval_status": "Approved after legal review."
        }

    # High risk continues escalation
    return {
        **state,
        "legal_review": "High risk detected. Escalating to Finance review."
    }


# -----------------------------
# Finance Review (High Only)
# -----------------------------
def finance_review_node(state: ComplianceState) -> ComplianceState:
    return {
        **state,
        "finance_review": "Finance reviewing commercial exposure."
    }


# -----------------------------
# Security Review (High Only)
# -----------------------------
def security_review_node(state: ComplianceState) -> ComplianceState:
    return {
        **state,
        "security_review": "CISO reviewing security and compliance exposure."
    }


# -----------------------------
# Executive Sign-Off (High Only)
# -----------------------------
def executive_signoff_node(state: ComplianceState) -> ComplianceState:
    return {
        **state,
        "executive_decision": "Executive approval required due to High Risk."
    }

# -----------------------------
# LangGraph Workflow
# -----------------------------
def build_graph():

    graph = StateGraph(ComplianceState)

    # Add nodes
    graph.add_node("validation", validation_node)
    graph.add_node("standard_approval", standard_approval_node)
    graph.add_node("legal_review", legal_review_node)
    graph.add_node("finance_review", finance_review_node)
    graph.add_node("security_review", security_review_node)
    graph.add_node("executive_signoff", executive_signoff_node)

    # Entry point
    graph.set_entry_point("validation")

    # First conditional routing (after validation)
    graph.add_node("legal_review_medium", legal_review_node)
    graph.add_node("legal_review_high", legal_review_node)

    graph.add_conditional_edges(
        "validation",
        risk_decision_node,
        {
            "low_risk": "standard_approval",
            "medium_risk": "legal_review_medium",
            "high_risk": "legal_review_high"
        }
    )

    # Medium ends after legal
    graph.add_edge("legal_review_medium", END)

    # High continues escalation
    graph.add_edge("legal_review_high", "finance_review")

    # Low risk ends immediately
    graph.add_edge("standard_approval", END)

    # # Legal review conditional continuation
    # graph.add_conditional_edges(
    #     "legal_review",
    #     lambda state: "end_medium" if state.get("approval_status") else "continue_high",
    #     {
    #         "end_medium": END,
    #         "continue_high": "finance_review"
    #     }
    # )

    # High-risk escalation chain
    graph.add_edge("finance_review", "security_review")
    graph.add_edge("security_review", "executive_signoff")
    graph.add_edge("executive_signoff", END)

    return graph.compile()


# -------------------------------------------------
# Compile once at module level
# -------------------------------------------------

workflow = build_graph()


# -------------------------------------------------
# Export Mermaid Diagram (Left to Right)
# -------------------------------------------------

def export_graph_diagram():
    mermaid_code = workflow.get_graph().draw_mermaid()
    mermaid_code = mermaid_code.replace("graph TD", "graph LR")

    with open("workflow_diagram.mmd", "w") as f:
        f.write(mermaid_code)

    return mermaid_code