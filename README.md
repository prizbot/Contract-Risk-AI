# 🏛️ AI Contract Compliance Engine  
### LangGraph-Powered Enterprise Contract & Governance Analyzer

---

## 📌 Overview

**AI Contract Compliance Engine** is an enterprise-grade contract validation and risk assessment system built using **LangGraph**, **LLMs**, and a modular rule-based compliance framework.

The system analyzes uploaded contracts (e.g., MSAs, NDAs, vendor agreements) and:

- Performs structured compliance validation
- Detects red flags
- Calculates risk scores
- Executes escalation workflows
- Generates executive summaries
- Produces downloadable compliance reports

The architecture is built to simulate real enterprise governance workflows while remaining deployable and extensible.

---

# 🚀 Core Features

| Feature | Description |
|----------|-------------|
| 📄 Document Upload | Accepts `.docx` contract files |
| 🧠 Hybrid Validation | Rule-based + LLM-based clause analysis |
| 📊 Risk Scoring Engine | Calculates cumulative risk score |
| 🔀 LangGraph Workflow | Multi-stage escalation routing |
| ⚖️ Compliance Checks | Threshold, existence, and red-flag checks |
| 🏢 Enterprise Escalation | Legal → Finance → Security → Executive |
| 📑 Executive Report | Downloadable structured PDF |
| 🌐 API Ready | FastAPI backend |
| 🖥 Dashboard | Streamlit UI with risk visualization |

---

# 🏗️ Architecture Overview

```text
User Upload
     ↓
Document Extraction
     ↓
Rule-Based Validation
     ↓
LLM Clause Evaluation
     ↓
Risk Scoring
     ↓
LangGraph Decision Engine
     ↓
Escalation Routing
     ↓
Executive Output
     ↓
PDF Report Generation
```
