# 🏛️ AI Contract Compliance Engine

### LangGraph-Powered Enterprise Contract & Governance Analyzer

------------------------------------------------------------------------

## 📌 Overview

**AI Contract Compliance Engine** is an enterprise-grade contract
validation and risk assessment system built using LangGraph and Large
Language Models (LLMs).

The system analyzes uploaded contracts (e.g., MSAs, NDAs, vendor
agreements) and performs structured compliance validation, risk
detection, and enterprise-style escalation workflows.

This project simulates real-world governance pipelines while remaining
deployable and extensible.

------------------------------------------------------------------------

# 🚀 Core Features

  Feature                 Description
  ----------------------- -------------------------------------------
  Document Upload         Accepts `.docx` contract files
  Hybrid Validation       Rule-based + LLM-based clause analysis
  Risk Scoring Engine     Calculates cumulative risk score
  LangGraph Workflow      Multi-stage escalation routing
  Compliance Checks       Threshold, existence, and red-flag checks
  Enterprise Escalation   Legal → Finance → Security → Executive
  Executive Report        Downloadable structured PDF
  API Ready               FastAPI backend
  Dashboard               Streamlit UI with risk visualization

------------------------------------------------------------------------

# 🏗️ Architecture Overview

User Upload\
↓\
Document Extraction\
↓\
Rule-Based Validation\
↓\
LLM Clause Evaluation\
↓\
Risk Scoring\
↓\
LangGraph Decision Engine\
↓\
Escalation Routing\
↓\
Executive Output\
↓\
PDF Report Generation

------------------------------------------------------------------------

# 🧱 Project Structure

contract-risk-ai/ ├── backend/ │ ├── api.py │ ├── graph.py │ ├──
state.py │ ├── validator.py │ ├── utils.py │ ├── playbook.json │ ├──
data/ │ └── msa.docx │ ├── frontend.py ├── requirements.txt └──
README.md

------------------------------------------------------------------------

# 🧠 Implementation Details

## 1️⃣ Validator Module

Responsibilities: - Core rule engine - Hybrid validation logic - LLM
clause evaluation - Risk score calculation

### Rule Types Implemented

  Rule Type                  Purpose
  -------------------------- ---------------------------------
  existence_check            Verify clause presence
  threshold_check            Validate numeric thresholds
  prohibited_check           Detect red-flag clauses
  prohibited_absence_check   Detect missing required clauses

------------------------------------------------------------------------

## 2️⃣ LangGraph Workflow (graph.py)

Implements enterprise escalation workflow using StateGraph.

### Nodes

  Node                Function
  ------------------- --------------------------------
  validation          Executes rule + LLM validation
  standard_approval   Auto-approval for low risk
  legal_review        Medium & High risk legal stage
  finance_review      Financial exposure evaluation
  security_review     Security impact evaluation
  executive_signoff   Final executive escalation

------------------------------------------------------------------------

## 3️⃣ State Management (state.py)

Defines structured state flow between LangGraph nodes including: -
Playbook - Document text - Validation results - Escalation decisions -
Approval status

------------------------------------------------------------------------

## 4️⃣ Playbook Configuration (playbook.json)

Defines categorized compliance rules under:

-   Commercial Validation
-   Regulatory & Legal Validation
-   Red Flags

Each rule includes rule ID, description, type, keywords, and risk score.

------------------------------------------------------------------------

## 5️⃣ FastAPI Backend (api.py)

### Endpoint

POST /validate

Accepts `.docx` file upload and returns structured validation and
escalation output.

------------------------------------------------------------------------

## 6️⃣ Streamlit Frontend (frontend.py)

### UI Features

-   File upload interface
-   Risk gauge visualization
-   Workflow pipeline diagram
-   Compliance findings table
-   Expandable technical details
-   Downloadable PDF report

------------------------------------------------------------------------

# 📊 Risk Model

## Risk Score Calculation

Total risk score is cumulative of violated rules.

### Risk Levels

  Score   Classification
  ------- ----------------
  0       Low
  1--10   Medium
  \>10    High

LLM-based high severity can override numerical score when required.

------------------------------------------------------------------------

# 📄 PDF Report Structure

Generated using ReportLab.

Includes:

1.  Executive Summary
2.  Risk Score & Classification
3.  Compliance Findings
4.  Red Flags Identified
5.  Recommended Remediation Actions
6.  Governance Recommendation

Designed for board-level readability.

------------------------------------------------------------------------

# ⚙️ Tech Stack

  Layer             Technology
  ----------------- ---------------
  Language          Python 3.11
  LLM Framework     LangChain
  Orchestration     LangGraph
  LLM Provider      OpenAI / Groq
  Backend           FastAPI
  Frontend          Streamlit
  Visualization     Plotly
  PDF Generation    ReportLab
  Data Validation   Pydantic
  API Server        Uvicorn

------------------------------------------------------------------------

# 🔄 Workflow Escalation Logic

  Risk Level   Action
  ------------ ----------------------------------------
  Low          Auto Approval
  Medium       Legal Review
  High         Legal → Finance → Security → Executive

Escalation chain is configurable.

------------------------------------------------------------------------

# 🛠️ Setup Instructions

1.  Clone the repository\
2.  Create virtual environment\
3.  Install dependencies\
4.  Set API keys\
5.  Run backend using Uvicorn\
6.  Run frontend using Streamlit

------------------------------------------------------------------------

# 📈 Future Improvements

-   Multi-framework comparison
-   RAG-based compliance engine
-   Clause rewriting suggestions
-   Multi-user SaaS support
-   Authentication layer
-   Audit log storage
-   Public deployment

------------------------------------------------------------------------

# 🏁 Conclusion

AI Contract Compliance Engine demonstrates:

-   Enterprise workflow modeling
-   Hybrid AI validation systems
-   Multi-stage governance routing
-   Production-style architecture
-   Real-world compliance simulation

------------------------------------------------------------------------

### Contact Information:

For any inquiries or collaborations, feel free to reach out: - LinkedIn:
[Priyadharshini NRS](https://www.linkedin.com/in/priyadharshininrs) -
Email: <priyadharshininrs@gmail.com>
