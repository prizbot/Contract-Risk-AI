import streamlit as st
import requests
import plotly.graph_objects as go
import streamlit.components.v1 as components
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import tempfile

# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="Enterprise Contract Compliance Engine",
    layout="wide"
)

st.title("Enterprise Contract Compliance Assessment")


# -------------------------------------------------
# Risk Gauge (Professional)
# -------------------------------------------------

def generate_risk_gauge(score):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Risk Score"},
        gauge={
            'axis': {'range': [0, 30]},
            'bar': {'color': "#1E1E1E"},
            'steps': [
                {'range': [0, 5], 'color': "#1B5E20"},
                {'range': [6, 10], 'color': "#F9A825"},
                {'range': [11, 30], 'color': "#B71C1C"}
            ],
        }
    ))

    fig.update_layout(height=280, margin=dict(t=40, b=0, l=0, r=0))
    return fig


# -------------------------------------------------
# Static Enterprise Workflow Diagram
# -------------------------------------------------

def render_workflow_pipeline(score):

    if score == 0:
        steps = ["Validation", "Auto Approval"]
        active_index = 1

    elif score <= 10:
        steps = ["Validation", "Legal Review", "Approval"]
        active_index = 2

    else:
        steps = [
            "Validation",
            "Legal Review",
            "Finance Review",
            "Security Review",
            "Executive Approval"
        ]
        active_index = len(steps) - 1

    step_blocks = ""

    for i, step in enumerate(steps):

        if i < active_index:
            color = "#2E7D32"  # completed
        elif i == active_index:
            color = "#1E3A8A"  # active
        else:
            color = "#6B7280"  # pending (better grey for dark theme)

        connector = ""
        if i < len(steps) - 1:
            connector = """
            <div class="arrow">➜</div>
            """

        step_blocks += f"""
        <div class="step-wrapper">
            <div class="step">
                <div class="circle" style="background:{color};">{i+1}</div>
                <div class="label">{step}</div>
            </div>
            {connector}
        </div>
        """

    html = f"""
    <html>
    <head>
    <style>
    body {{
        margin:0;
        padding:0;
        background-color:transparent;
        font-family: Arial, sans-serif;
    }}

    .container {{
        display:flex;
        align-items:center;
        justify-content:center;
        gap:20px;
        margin-top:25px;
    }}

    .step-wrapper {{
        display:flex;
        align-items:center;
        gap:20px;
    }}

    .step {{
        text-align:center;
    }}

    .circle {{
        width:48px;
        height:48px;
        border-radius:50%;
        margin:0 auto;
        line-height:48px;
        color:white;
        font-weight:bold;
        font-size:16px;
    }}

    .label {{
        margin-top:10px;
        font-size:14px;
        font-weight:500;
        color:white;   /* <-- FIXED: white text for dark theme */
    }}

    .arrow {{
        font-size:22px;
        color:white;   /* <-- FIXED: white arrow */
        margin-bottom:15px;
    }}

    </style>
    </head>
    <body>
        <div class="container">
            {step_blocks}
        </div>
    </body>
    </html>
    """

    components.html(html, height=170)
    # -------------------------------------------------
# Executive PDF Generator
# -------------------------------------------------

def generate_pdf_report(validation):

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    score = validation.get("total_risk_score", 0)
    violations = validation.get("violations", [])

    elements.append(Paragraph("Enterprise Contract Compliance Report", styles["Title"]))
    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph("1. Executive Summary", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    risk_level = "Low"
    if score > 10:
        risk_level = "High"
    elif score > 0:
        risk_level = "Medium"

    elements.append(Paragraph(f"Overall Risk Score: {score}", styles["Normal"]))
    elements.append(Paragraph(f"Risk Classification: {risk_level}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("2. Compliance Findings", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    if violations:
        issue_list = []
        for v in violations:
            issue_list.append(
                ListItem(
                    Paragraph(f"{v['rule_id']} – {v['description']}", styles["Normal"])
                )
            )
        elements.append(ListFlowable(issue_list))
    else:
        elements.append(Paragraph("No compliance violations identified.", styles["Normal"]))

    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph("3. Remediation Recommendations", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    if violations:

        remediation_list = []

        for v in violations:
            desc = v["description"].lower()

            if "hipaa" in desc:
                recommendation = (
                    "Insert explicit HIPAA compliance clause in the Data Protection section."
                )
            elif "retention" in desc:
                recommendation = (
                    "Amend retention policy to minimum 7 years to meet healthcare standards."
                )
            elif "liability" in desc:
                recommendation = (
                    "Replace unlimited liability with a capped liability framework."
                )
            else:
                recommendation = "Review and revise clause per enterprise compliance standards."

            remediation_list.append(
                ListItem(Paragraph(recommendation, styles["Normal"]))
            )

        elements.append(ListFlowable(remediation_list))

    else:
        elements.append(Paragraph("No remediation required.", styles["Normal"]))

    doc.build(elements)
    return temp_file.name


# -------------------------------------------------
# Upload + API
# -------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Contract Document (.docx)",
    type=["docx"]
)

if uploaded_file:

    with st.spinner("Running compliance workflow..."):

        try:
            response = requests.post(
                "http://127.0.0.1:8000/validate",
                files={"file": uploaded_file}
            )
            result = response.json()
        except Exception:
            st.error("Backend service is not available.")
            st.stop()

    validation = result.get("validation_result", {})
    score = validation.get("total_risk_score", 0)
    violations = validation.get("violations", [])

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Risk Overview")
        st.plotly_chart(generate_risk_gauge(score), width="stretch")

    with col2:
       st.subheader("Workflow Process")
       render_workflow_pipeline(score)

    st.markdown("---")

    st.subheader("Compliance Findings")

    if violations:
        table_data = [["Rule ID", "Description"]]
        for v in violations:
            table_data.append([v["rule_id"], v["description"]])
        st.table(table_data)
    else:
        st.write("All compliance checks passed.")

    st.markdown("---")

    with st.expander("Technical Validation Details"):
        st.json(validation)

    pdf_path = generate_pdf_report(validation)

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="Download Compliance Report (PDF)",
            data=f,
            file_name="Enterprise_Compliance_Report.pdf",
            mime="application/pdf"
        )