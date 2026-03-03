import re
import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


# -----------------------------
# LLM Provider Abstraction
# -----------------------------

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "groq")

    if provider == "groq":
        return ChatOpenAI(
            model="llama-3.1-8b-instant",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0
        )

    elif provider == "openai":
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

    else:
        raise ValueError("Unsupported LLM Provider")


def llm_clause_evaluation(context_text: str, rule: dict):
    llm = get_llm()

    prompt = f"""
    You are a strict enterprise compliance validator.

    Rule:
    {rule['description']}

    Relevant Contract Context:
    {context_text}

    Evaluate compliance strictly.

    Return ONLY JSON:
    {{
        "compliance_status": "Compliant / Non-Compliant / Partial",
        "risk_level": "Low / Medium / High",
        "reason": "short explanation"
    }}
    """

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return json.loads(response.content)
    except Exception as e:
        return {
            "compliance_status": "ERROR",
            "risk_level": "Unknown",
            "reason": str(e)
        }


# -----------------------------
# Core Validation Engine
# -----------------------------

def validate_document(playbook: dict, document_text: str):

    results = {
        "violations": [],
        "passed_rules": [],
        "llm_analysis": [],
        "total_risk_score": 0
    }

    clauses = document_text.split("\n\n")

    for category in playbook.get("categories", []):
        for rule in category.get("rules", []):

            rule_type = rule.get("type")
            keywords = rule.get("keywords", [])

            matched_clauses = []

            # Collect ALL relevant clauses
            for clause in clauses:
                if any(keyword.lower() in clause.lower() for keyword in keywords):
                    matched_clauses.append(clause)

            combined_context = "\n\n".join(matched_clauses)

            # -----------------------------
            # 1️⃣ Existence Check
            # -----------------------------
            if rule_type == "existence_check":

                if not matched_clauses:
                    results["violations"].append({
                        "rule_id": rule["rule_id"],
                        "description": rule["description"],
                        "category": category["category_name"]
                    })
                    results["total_risk_score"] += rule["risk_score"]

                else:
                    results["passed_rules"].append(rule["rule_id"])

                    # Send aggregated context to LLM
                    llm_result = llm_clause_evaluation(combined_context, rule)

                    results["llm_analysis"].append({
                        "rule_id": rule["rule_id"],
                        "category": category["category_name"],
                        "llm_result": llm_result
                    })

            # -----------------------------
            # 2️⃣ Threshold Check
            # -----------------------------
            elif rule_type == "threshold_check":

                pattern = rule.get("field_pattern", "")
                threshold = rule.get("threshold_value")
                comparison = rule.get("comparison")

                match = re.search(rf"{pattern}.*?(\d+)", document_text, re.IGNORECASE)

                if match:
                    value = int(match.group(1))

                    valid = False
                    if comparison == ">=" and value >= threshold:
                        valid = True
                    elif comparison == "<=" and value <= threshold:
                        valid = True

                    if not valid:
                        results["violations"].append({
                            "rule_id": rule["rule_id"],
                            "description": rule["description"],
                            "found_value": value,
                            "expected": f"{comparison} {threshold}",
                            "category": category["category_name"]
                        })
                        results["total_risk_score"] += rule["risk_score"]

                    else:
                        results["passed_rules"].append(rule["rule_id"])

                else:
                    results["violations"].append({
                        "rule_id": rule["rule_id"],
                        "description": rule["description"],
                        "issue": "Value not found",
                        "category": category["category_name"]
                    })
                    results["total_risk_score"] += rule["risk_score"]

            # -----------------------------
            # 3️⃣ Prohibited Check
            # -----------------------------
            elif rule_type == "prohibited_check":

                if matched_clauses:
                    results["violations"].append({
                        "rule_id": rule["rule_id"],
                        "description": rule["description"],
                        "category": category["category_name"]
                    })
                    results["total_risk_score"] += rule["risk_score"]

                else:
                    results["passed_rules"].append(rule["rule_id"])

    return results