import streamlit as st
import pathlib
import datetime
import re
import os
import io
import subprocess
import pypdf

try:
    import pymupdf as fitz
except ImportError:
    fitz = None

try:
    import docx
except ImportError:
    docx = None

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

# Page Setup
st.set_page_config(
    page_title="AI Candidate Screener Portal",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .badge-pass {
        background-color: #dcfce7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
    .badge-fail {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
    .badge-warn {
        background-color: #fef3c7;
        color: #92400e;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = pathlib.Path(__file__).parent.resolve()
RESUMES_DIR = BASE_DIR / "Resumes"
REPORTS_DIR = BASE_DIR / "Reports"
REFERENCES_DIR = BASE_DIR / "references"
RESUMES_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
DEFAULT_JD_PATH = REFERENCES_DIR / "job-description.md"

FALLBACK_DEFAULT_JD_TEXT = """# Senior SDET / QA Automation Engineer
- Role: Senior SDET / QA Automation Engineer
- Experience: 6 to 10 years of experience in test automation.
- Mandatory:
  - JavaScript / TypeScript
  - Python
  - Cypress
  - Playwright
  - Pytest
  - Automation Framework Design (Page Object Model)
  - UI / Web Testing + BDD (Cucumber / SpecFlow)
  - API Testing (REST APIs, Postman, Rest Assured)
  - STLC & Test Strategy
  - Test Management Tools (Jira, ALM, TestRail)
  - Agile / Kanban
  - AI Solution Testing (GenAI, ML Model validation)
  - Agentic AI (MCP, RAG, Multi-agent workflows)
- Preferred / Good to have:
  - AWS / Azure Cloud Exposure
  - CI/CD Integration (Jenkins, GitHub Actions)
  - Monitoring & Observability (Splunk, Grafana)
  - No-Code / Low-Code Tools (Mabl, TestComplete)
  - Pharma / Life Sciences Domain
"""

# Standard Default SDET Taxonomy
DEFAULT_MANDATORY_WEIGHTS = {
    "JavaScript / TypeScript": (6, "Proficient in JS/TS for building automation solutions"),
    "Python": (6, "Proficient in Python for building automation solutions"),
    "Cypress": (6, "Hands-on modern E2E automation tool"),
    "Playwright": (6, "Hands-on Playwright modern framework experience"),
    "Pytest": (6, "Hands-on Pytest test runner & fixtures"),
    "Automation Framework Design": (8, "Build, scale, and maintain POM frameworks end-to-end"),
    "UI / Web Testing + BDD": (9, "UI/Web testing with BDD (Cucumber / SpecFlow / MABL)"),
    "API Testing": (9, "REST APIs with Postman / Insomnia / Mocha"),
    "STLC & Test Strategy": (7, "Functional & non-functional testing strategy, RTM, metrics"),
    "Test Management Tools": (6, "Hands-on Jira, HP ALM / QC, TestRail"),
    "Agile / Kanban": (6, "Agile Scrum ceremonies, sprint planning, defect triage"),
    "AI Solution Testing": (6, "Experience testing AI-powered solutions / ML models"),
    "Agentic AI": (4, "Agentic AI (MCP, RAG, Prompting; test/dev solutions)")
}

DEFAULT_GOOD_TO_HAVE_WEIGHTS = {
    "AWS / Azure Cloud Exposure": (2, "Cloud services relevant to test environments"),
    "CI/CD Integration": (3, "Integrates test suites into CI/CD pipelines"),
    "Monitoring & Observability": (2, "Splunk, Grafana, Power BI monitoring"),
    "No-Code / Low-Code Tools": (1, "MABL, Test Complete"),
    "Pharma / Life Sciences Domain": (2, "Pharma, healthcare, or clinical trial background")
}

def extract_text_from_bytes(file_name: str, file_bytes: bytes) -> str:
    suffix = pathlib.Path(file_name).suffix.lower()
    text = ""
    if suffix == ".pdf":
        try:
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            text = ""
        if not text.strip() and fitz:
            try:
                doc = fitz.open(stream=file_bytes, filetype="pdf")
                text = "\n".join(page.get_text() or "" for page in doc)
            except Exception:
                pass
        return text if text.strip() else "PDF contains non-extractable text."
    elif suffix in [".docx"]:
        if docx:
            try:
                doc = docx.Document(io.BytesIO(file_bytes))
                return "\n".join(p.text for p in doc.paragraphs)
            except Exception as e:
                return f"Error reading DOCX: {e}"
        return "python-docx parser unavailable"
    else:
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except Exception as e:
            return f"Error reading text file: {e}"

def extract_years_experience(text: str) -> float:
    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs|year|yr)\s*(?:of)?\s*(?:experience|exp)",
        r"(?:experience|exp):\s*(\d+(?:\.\d+)?)\+?\s*(?:years|yrs|year|yr)",
        r"(\d+)\s*(?:years|yrs)\s*(\d+)\s*(?:months|m|mos)",
        r"\[(\d+)y_(\d+)m\]"
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            if len(m.groups()) == 2 and m.group(2):
                return float(m.group(1)) + float(m.group(2)) / 12.0
            return float(m.group(1))
    return 0.0

def parse_custom_jd(jd_text: str):
    lines = [line.strip() for line in jd_text.splitlines() if line.strip()]
    role_title = "Custom Technical Role"
    for line in lines[:5]:
        if line.startswith("#"):
            role_title = line.lstrip("#").strip()
            break
        elif "role:" in line.lower() or "title:" in line.lower() or "position:" in line.lower():
            role_title = line.split(":", 1)[1].strip()
            break

    mandatory = {}
    good_to_have = {}
    current_sec = "mandatory"
    for line in lines:
        lower = line.lower()
        if any(h in lower for h in ["good to have", "preferred", "nice to have", "bonus", "secondary"]):
            current_sec = "good"
            continue
        elif any(h in lower for h in ["must have", "mandatory", "required", "core requirements", "qualifications"]):
            current_sec = "mandatory"
            continue

        m = re.match(r"^[-*•\d.]+\s*(.+)$", line)
        if m:
            item = m.group(1).strip()
            if len(item) > 3 and not item.endswith(":"):
                title = item.split(":")[0].split("-")[0].strip()
                if len(title) > 40:
                    title = title[:37] + "..."
                if current_sec == "mandatory":
                    mandatory[title] = (6, item)
                else:
                    good_to_have[title] = (2, item)

    if not mandatory:
        mandatory = DEFAULT_MANDATORY_WEIGHTS
    if not good_to_have:
        good_to_have = DEFAULT_GOOD_TO_HAVE_WEIGHTS

    return role_title, mandatory, good_to_have

def evaluate_candidate(name: str, text: str, custom_jd_text: str = None) -> dict:
    if custom_jd_text:
        role_title, mandatory_weights, good_weights = parse_custom_jd(custom_jd_text)
    else:
        role_title = "Senior SDET / QA Automation"
        mandatory_weights = DEFAULT_MANDATORY_WEIGHTS
        good_weights = DEFAULT_GOOD_TO_HAVE_WEIGHTS

    exp_years = extract_years_experience(text)
    lower_text = text.lower()

    # Rule 1: Experience Gate (<6 yrs)
    if 0 < exp_years < 6.0:
        return {
            "name": name,
            "target_role": role_title,
            "years_exp": exp_years,
            "mandatory": {k: ("Missing", "Gate Failed: Total experience under 6.0 years cutoff.") for k in mandatory_weights},
            "good_to_have": {k: ("Missing", "Gate Failed: Evaluated 0 due to experience cutoff.") for k in good_weights},
            "mandatory_score": 0.0,
            "good_score": 0.0,
            "exp_score": 0.0,
            "raw_score": 0.0,
            "final_score": 0.0,
            "verdict": "Screening Failed (Disqualified)",
            "override_note": f"Rule #1 Hard Gate Triggered: Total experience {exp_years:.1f} yrs < 6.0 yrs hard cutoff."
        }

    skill_keywords = {
        "JavaScript / TypeScript": ["javascript", "typescript", "js", "ts", "es6", "node"],
        "Python": ["python", "pytest", "django", "flask"],
        "Cypress": ["cypress"],
        "Playwright": ["playwright"],
        "Pytest": ["pytest"],
        "Automation Framework Design": ["framework", "page object model", "pom", "modular framework", "hybrid framework", "architecture"],
        "UI / Web Testing + BDD": ["cucumber", "bdd", "specflow", "gherkin", "selenium", "ui automation", "web testing"],
        "API Testing": ["rest", "api", "postman", "rest assured", "restassured", "soap", "endpoint", "microservices"],
        "STLC & Test Strategy": ["stlc", "test strategy", "test plan", "rtm", "regression", "qa process"],
        "Test Management Tools": ["jira", "alm", "quality center", "testrail", "zephyr", "qtest", "azure devops"],
        "Agile / Kanban": ["agile", "scrum", "sprint", "kanban", "ceremonies", "standup"],
        "AI Solution Testing": ["ai testing", "llm", "genai", "generative ai", "model validation", "ml testing", "prompt"],
        "Agentic AI": ["agentic", "mcp", "rag", "agents", "langchain", "autogen", "crewai"],
        "AWS / Azure Cloud Exposure": ["aws", "azure", "cloud", "ec2", "s3", "lambda"],
        "CI/CD Integration": ["ci/cd", "jenkins", "github actions", "gitlab", "pipeline", "bamboo"],
        "Monitoring & Observability": ["splunk", "grafana", "dynatrace", "datadog", "cloudwatch", "power bi"],
        "No-Code / Low-Code Tools": ["mabl", "testcomplete", "tosca", "accelq", "katalon"],
        "Pharma / Life Sciences Domain": ["pharma", "clinical", "healthcare", "gxp", "fda", "21 cfr", "life sciences", "iqvia", "philips", "novartis", "pfizer"]
    }

    mandatory_results = {}
    mandatory_score = 0.0
    for skill, (weight, _) in mandatory_weights.items():
        kw_list = skill_keywords.get(skill, [w.lower() for w in skill.split() if len(w) > 2])
        matched_kw = [kw for kw in kw_list if kw in lower_text]
        
        if matched_kw:
            is_evidenced = any(term in lower_text for term in ["implemented", "designed", "developed", "automated", "created", "reduced", "led", "migrated", "built", "tested", "project"])
            if is_evidenced:
                status = "Matched"
                factor = 1.00
                evidence = f"Demonstrated in project deliverables ({', '.join(matched_kw[:2])})"
            else:
                status = "Claimed but unevidenced"
                factor = 0.30
                evidence = f"Listed in skills/summary without detailed deliverable ({', '.join(matched_kw[:2])})"
        else:
            status = "Missing"
            factor = 0.00
            evidence = "Not found in profile text"
            
        points = weight * factor
        mandatory_score += points
        mandatory_results[skill] = (status, evidence)

    good_results = {}
    good_score = 0.0
    for skill, (weight, _) in good_weights.items():
        kw_list = skill_keywords.get(skill, [w.lower() for w in skill.split() if len(w) > 2])
        matched_kw = [kw for kw in kw_list if kw in lower_text]
        if matched_kw:
            status = "Matched"
            factor = 1.00
            evidence = f"Evidenced in profile ({', '.join(matched_kw[:2])})"
        else:
            status = "Missing"
            factor = 0.00
            evidence = "Not evidenced"
        points = weight * factor
        good_score += points
        good_results[skill] = (status, evidence)

    if 6.0 <= exp_years <= 10.0:
        exp_score = 5.0
    elif 10.0 < exp_years <= 12.0:
        exp_score = 3.0
    elif exp_years > 12.0:
        exp_score = 2.0
    else:
        exp_score = 4.0

    raw_score = mandatory_score + good_score + exp_score
    final_score = raw_score
    override_note = "Standard capacity calculation"

    # Core Language Gate
    has_js = "Matched" in mandatory_results.get("JavaScript / TypeScript", ("Missing",))[0] or "Matched" in mandatory_results.get("Python", ("Missing",))[0]
    if not has_js and "JavaScript / TypeScript" in mandatory_weights:
        final_score = min(final_score, 45.0)
        verdict = "Weak Fit (Core Language Missing) - Rejected"
        override_note = "Rule #2 Override: Neither core JavaScript/TypeScript nor Python was evidenced in project deliverables."
        return {
            "name": name,
            "target_role": role_title,
            "years_exp": exp_years,
            "mandatory": mandatory_results,
            "good_to_have": good_results,
            "mandatory_score": round(mandatory_score, 1),
            "good_score": round(good_score, 1),
            "exp_score": round(exp_score, 1),
            "raw_score": round(raw_score, 1),
            "final_score": round(final_score, 1),
            "verdict": verdict,
            "override_note": override_note
        }

    # AI Hard Gap Rule #3
    ai_status = mandatory_results.get("AI Solution Testing", ("Missing",))[0]
    agentic_status = mandatory_results.get("Agentic AI", ("Missing",))[0]
    if ai_status == "Missing" and agentic_status == "Missing":
        if final_score >= 60.0:
            final_score = 59.0
        verdict = "Weak Fit (AI Testing & Agentic AI Gap) - Hard Fail"
        override_note = "Rule #3 Override: Both AI Solution Testing and Agentic AI are completely missing; score capped < 60."
        return {
            "name": name,
            "target_role": role_title,
            "years_exp": exp_years,
            "mandatory": mandatory_results,
            "good_to_have": good_results,
            "mandatory_score": round(mandatory_score, 1),
            "good_score": round(good_score, 1),
            "exp_score": round(exp_score, 1),
            "raw_score": round(raw_score, 1),
            "final_score": round(final_score, 1),
            "verdict": verdict,
            "override_note": override_note
        }

    if final_score >= 80.0:
        verdict = "Strong Fit - Recommended for Interview"
        override_note = "All mandatory requirements verified with concrete deliverables."
    elif final_score >= 60.0:
        verdict = "Potential Fit (Interview with targeted probes)"
        override_note = "Core skills evidenced; requires probing on claimed items or partial gaps."
    elif final_score >= 40.0:
        verdict = "Weak Fit - Secondary Pool"
        override_note = "Multiple mandatory gaps identified."
    else:
        verdict = "Reject - Failed Initial Screen"
        override_note = "Significant qualification shortfalls."

    return {
        "name": name,
        "target_role": role_title,
        "years_exp": exp_years,
        "mandatory": mandatory_results,
        "good_to_have": good_results,
        "mandatory_score": round(mandatory_score, 1),
        "good_score": round(good_score, 1),
        "exp_score": round(exp_score, 1),
        "raw_score": round(raw_score, 1),
        "final_score": round(final_score, 1),
        "verdict": verdict,
        "override_note": override_note
    }

# FPDF2 Class for Vector Audit Report PDF
if FPDF:
    class ScreenerPDF(FPDF):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_auto_page_break(auto=True, margin=15)

        def header(self):
            self.set_fill_color(15, 23, 42)
            self.rect(0, 0, 210, 14, "F")
            self.set_xy(10, 2.5)
            self.set_font("Helvetica", "B", 9)
            self.set_text_color(248, 250, 252)
            self.cell(0, 8, "AI CANDIDATE SCREENER  |  EVIDENCE-DRIVEN ATS AUDIT REPORT")
            self.ln(14)

        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", size=8)
            self.set_text_color(148, 163, 184)
            self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

def sanitize(text: str) -> str:
    if not text:
        return ""
    replacements = {
        "—": " - ", "–": "-", "→": " -> ", "•": "*",
        "⚠️": " [!]", "🚀": " [*]", "❌": " [X]", "✅": " [OK]",
        "“": '"', "”": '"', "‘": "'", "’": "'",
        "≥": ">=", "≤": "<=", "&rarr;": " -> ", "&nbsp;": " ",
        "&amp;": "&", "&lt;": "<", "&gt;": ">"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode("ascii", "replace").decode("ascii")

def build_pdf_report(date_str: str, candidate_results: list, file_names: list, active_jd_display: str) -> bytes:
    if not FPDF:
        return b""
    try:
        pdf = ScreenerPDF(orientation="P", unit="mm", format="A4")
        pdf.alias_nb_pages()
        pdf.add_page()

        # Title & Metadata
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 8, f"Candidate Screening Audit Report - {sanitize(date_str)}")
        pdf.ln(8)

        pdf.set_fill_color(241, 245, 249)
        pdf.set_draw_color(203, 213, 225)
        pdf.rect(10, pdf.get_y(), 190, 20, "DF")
        pdf.set_xy(12, pdf.get_y() + 2)
        pdf.set_font("Helvetica", "B", 8.5)
        pdf.set_text_color(71, 85, 105)
        pdf.cell(0, 5, f"Screened Files: {sanitize(', '.join(file_names))}")
        pdf.ln(5)
        pdf.set_x(12)
        pdf.cell(0, 5, f"Active JD: {sanitize(active_jd_display)}")
        pdf.ln(5)
        pdf.set_x(12)
        pdf.cell(0, 5, f"Candidates Ranked: {len(candidate_results)}")
        pdf.ln(10)

        # 1) Ranking Leaderboard
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(0, 7, "1) Candidate Ranking Leaderboard")
        pdf.ln(6)

        col_w = [10, 42, 26, 38, 22, 52]
        headers = ["#", "Candidate", "Score", "Verdict", "Exp", "Missing Mandatory"]
        pdf.set_fill_color(30, 41, 59)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8)
        for w, h in zip(col_w, headers):
            pdf.cell(w, 6, h, border=1, fill=True)
        pdf.ln(6)

        pdf.set_text_color(30, 41, 59)
        pdf.set_font("Helvetica", size=7.5)
        for idx, c in enumerate(candidate_results, 1):
            missing_m = [k for k, v in c.get("mandatory", {}).items() if v[0] == "Missing"]
            missing_str = ", ".join(missing_m[:2]) + ("..." if len(missing_m) > 2 else "") if missing_m else "None"
            
            pdf.cell(col_w[0], 6, str(idx), border=1)
            pdf.cell(col_w[1], 6, sanitize(c["name"][:22]), border=1)
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.cell(col_w[2], 6, f"{c['final_score']}/100", border=1)
            pdf.set_font("Helvetica", size=7.5)
            pdf.cell(col_w[3], 6, sanitize(c["verdict"][:20]), border=1)
            pdf.cell(col_w[4], 6, f"{c['years_exp']} yrs", border=1)
            pdf.cell(col_w[5], 6, sanitize(missing_str[:28]), border=1)
            pdf.ln(6)

        pdf.ln(4)

        # Key Takeaways
        pdf.set_fill_color(254, 243, 199)
        pdf.set_draw_color(245, 158, 11)
        takeaway_h = 8 + (len(candidate_results) * 5.5)
        pdf.rect(10, pdf.get_y(), 190, takeaway_h, "DF")
        pdf.set_xy(12, pdf.get_y() + 2)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(146, 64, 14)
        pdf.cell(0, 5, "Key Takeaway & Override Decisions:")
        pdf.ln(5)
        pdf.set_font("Helvetica", size=8)
        for c in candidate_results:
            pdf.set_x(12)
            pdf.cell(0, 5, sanitize(f"* {c['name']}: {c['verdict']} - {c['override_note']}"))
            pdf.ln(5)

        pdf.ln(8)

        # 2) Gap Matrix
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(0, 7, "2) 4-Tier Evidence Gap Matrix")
        pdf.ln(6)

        for c in candidate_results:
            pdf.set_fill_color(224, 231, 255)
            pdf.set_text_color(30, 27, 75)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(190, 6, f"Candidate: {sanitize(c['name'])}  |  Score: {c['final_score']}/100  |  {sanitize(c['verdict'])}", border=1, fill=True)
            pdf.ln(6)

            gw = [42, 50, 20, 26, 52]
            gh = ["Skill / Area", "Expectation", "Type", "Status", "Evidence"]
            pdf.set_fill_color(241, 245, 249)
            pdf.set_text_color(71, 85, 105)
            pdf.set_font("Helvetica", "B", 7.5)
            for w, h in zip(gw, gh):
                pdf.cell(w, 5, h, border=1, fill=True)
            pdf.ln(5)

            pdf.set_font("Helvetica", size=7)
            pdf.set_text_color(30, 41, 59)
            
            all_skills = list(c.get("mandatory", {}).items()) + list(c.get("good_to_have", {}).items())
            for k, v in all_skills:
                req_type = "Mandatory" if k in c.get("mandatory", {}) else "Good-to-have"
                status_text = v[0]
                evidence_text = v[1] if len(v) > 1 else ""
                
                pdf.cell(gw[0], 5, sanitize(k[:24]), border=1)
                pdf.cell(gw[1], 5, sanitize(k[:28]), border=1)
                pdf.cell(gw[2], 5, req_type, border=1)
                pdf.cell(gw[3], 5, sanitize(status_text[:14]), border=1)
                pdf.cell(gw[4], 5, sanitize(evidence_text[:30]), border=1)
                pdf.ln(5)

            pdf.ln(4)

        # 3) Candidate Details
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(30, 58, 138)
        pdf.cell(0, 7, "3) Detailed Candidate Arithmetic & Verdicts")
        pdf.ln(6)

        for idx, c in enumerate(candidate_results, 1):
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(0, 5, f"{idx}. {sanitize(c['name'])} - {sanitize(c['verdict'])}")
            pdf.ln(5)
            pdf.set_font("Helvetica", size=8)
            pdf.set_text_color(51, 65, 85)
            pdf.cell(0, 4.5, f"Total Experience: {c['years_exp']} yrs  |  Final Score: {c['final_score']} / 100")
            pdf.ln(4.5)
            pdf.cell(0, 4.5, f"Score Breakdown: Mandatory {c['mandatory_score']}/85, Bonus {c['good_score']}/10, Exp Fit {c['exp_score']}/5 -> Raw: {c['raw_score']}/100")
            pdf.ln(4.5)
            pdf.cell(0, 4.5, f"Override Decision: {sanitize(c['override_note'])}")
            pdf.ln(6)

        return bytes(pdf.output())
    except Exception:
        return b""

def generate_report_files(timestamp: str, candidate_results: list, file_names: list, active_jd_display: str):
    report_sub = REPORTS_DIR / timestamp
    report_sub.mkdir(parents=True, exist_ok=True)
    date_str = timestamp.split("_")[0]
    files_str = ", ".join(file_names)

    # Markdown
    md_lines = [
        f"# Candidate Screening Audit Report — {date_str}",
        "",
        f"- **Screened Files:** {files_str}",
        f"- **Active JD:** {active_jd_display}",
        f"- **Candidates Ranked:** {len(candidate_results)}",
        "",
        "---",
        "",
        "## 1) Ranking",
        "",
        "| # | Candidate | Score | Verdict | Total Exp | Missing (Mandatory) | Partial | Claimed |",
        "|---|---|---|---|---|---|---|---|"
    ]

    for idx, c in enumerate(candidate_results, 1):
        missing_m = [k for k, v in c["mandatory"].items() if v[0] == "Missing"]
        missing_str = ", ".join(missing_m) if missing_m else "—"
        partial_m = [k for k, v in c["mandatory"].items() if v[0] == "Partial match"]
        partial_str = ", ".join(partial_m) if partial_m else "—"
        claimed_m = [k for k, v in c["mandatory"].items() if v[0] == "Claimed but unevidenced"]
        claimed_str = ", ".join(claimed_m) if claimed_m else "—"
        md_lines.append(f"| {idx} | **{c['name']}** | **{c['final_score']} / 100** | {c['verdict']} | {c['years_exp']} yrs | {missing_str} | {partial_str} | {claimed_str} |")

    md_lines.extend(["", "> ### Key Takeaway & Override Decisions:"])
    for c in candidate_results:
        md_lines.append(f"> - **{c['name']}:** {c['verdict']} — {c['override_note']}")

    md_lines.extend(["", "---", "", "## 2) Gap Matrix", ""])
    for c in candidate_results:
        md_lines.append(f"### Candidate: {c['name']}")
        md_lines.append("| Skill / Area | JD Expectation | Requirement | Status | Evidence (Key Line / Deliverable) |")
        md_lines.append("|---|---|---|---|---|")
        for k, v in c["mandatory"].items():
            exp_text = DEFAULT_MANDATORY_WEIGHTS.get(k, (0, "Mandatory Technical Skill"))[1]
            md_lines.append(f"| **{k}** | {exp_text} | Mandatory | **{v[0]}** | {v[1]} |")
        for k, v in c["good_to_have"].items():
            exp_text = DEFAULT_GOOD_TO_HAVE_WEIGHTS.get(k, (0, "Preferred Skill"))[1]
            md_lines.append(f"| **{k}** | {exp_text} | Good-to-have | **{v[0]}** | {v[1]} |")
        md_lines.append("")

    md_lines.extend(["---", "", "## 3) Candidate Details", ""])
    for idx, c in enumerate(candidate_results, 1):
        md_lines.append(f"### {idx}. {c['name']}")
        md_lines.append(f"**Tag Line:** {c['verdict']}  ")
        md_lines.append(f"- **Total Experience:** {c['years_exp']} years")
        md_lines.append(f"- **Score Breakdown:** Mandatory {c['mandatory_score']}/85, Bonus {c['good_score']}/10, Exp Fit {c['exp_score']}/5 → **Total: {c['final_score']}/100**")
        md_lines.append(f"- **Override Decision:** {c['override_note']}")
        md_lines.append("")

    md_content = "\n".join(md_lines)
    md_path = report_sub / f"candidate_screening_report_{date_str}.md"
    md_path.write_text(md_content, encoding="utf-8")

    # HTML
    html_lines = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>",
        "<title>Candidate Screening Report</title>",
        "<style>",
        "  @page { size: A4 portrait; margin: 14mm; }",
        "  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #1e293b; line-height: 1.5; font-size: 12px; margin: 0; padding: 0; }",
        "  h1 { font-size: 20px; color: #0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 6px; margin-top: 0; }",
        "  .subtitle { font-size: 11px; color: #64748b; margin-bottom: 14px; }",
        "  h2 { font-size: 14.5px; color: #1e3a8a; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; margin-top: 16px; margin-bottom: 8px; }",
        "  .candidate-heading { font-size: 13px; font-weight: 700; color: #1e1b4b; background: #e0e7ff; padding: 6px 10px; border-left: 4px solid #4f46e5; border-radius: 4px; margin-top: 14px; margin-bottom: 8px; }",
        "  table { width: 100%; border-collapse: collapse; margin-bottom: 12px; font-size: 10.5px; }",
        "  th, td { border: 1px solid #cbd5e1; padding: 5px 7px; text-align: left; vertical-align: top; }",
        "  th { background-color: #f1f5f9; color: #0f172a; font-weight: 600; }",
        "  .badge-pass { background-color: #dcfce7; color: #166534; padding: 2px 5px; border-radius: 4px; font-weight: 600; font-size: 10px; }",
        "  .badge-fail { background-color: #fee2e2; color: #991b1b; padding: 2px 5px; border-radius: 4px; font-weight: 600; font-size: 10px; }",
        "  .badge-warn { background-color: #fef3c7; color: #92400e; padding: 2px 5px; border-radius: 4px; font-weight: 600; font-size: 10px; }",
        "  .callout-warn { background-color: #fffbeb; border-left: 4px solid #f59e0b; padding: 8px 12px; margin-bottom: 12px; font-size: 11px; }",
        "</style></head><body>",
        f"<h1>Screening Report — {date_str}</h1>",
        f"<div class='subtitle'><strong>Screened Files:</strong> {files_str} &nbsp;|&nbsp; <strong>Active JD:</strong> {active_jd_display} &nbsp;|&nbsp; <strong>Candidates Ranked:</strong> {len(candidate_results)}</div>",
        "<h2>1) Ranking</h2><table><thead><tr><th>#</th><th>Candidate</th><th>Score</th><th>Verdict</th><th>Total Exp</th><th>Missing (Mandatory)</th><th>Partial</th><th>Claimed</th></tr></thead><tbody>"
    ]
    for idx, c in enumerate(candidate_results, 1):
        missing_m = [k for k, v in c["mandatory"].items() if v[0] == "Missing"]
        missing_str = ", ".join(missing_m) if missing_m else "—"
        partial_m = [k for k, v in c["mandatory"].items() if v[0] == "Partial match"]
        partial_str = ", ".join(partial_m) if partial_m else "—"
        claimed_m = [k for k, v in c["mandatory"].items() if v[0] == "Claimed but unevidenced"]
        claimed_str = ", ".join(claimed_m) if claimed_m else "—"
        badge_cls = "badge-pass" if "Strong" in c["verdict"] else ("badge-warn" if "Potential" in c["verdict"] else "badge-fail")
        html_lines.append(f"<tr><td>{idx}</td><td><strong>{c['name']}</strong></td><td><strong>{c['final_score']} / 100</strong></td><td><span class='{badge_cls}'>{c['verdict']}</span></td><td>{c['years_exp']} yrs</td><td>{missing_str}</td><td>{partial_str}</td><td>{claimed_str}</td></tr>")
    html_lines.append("</tbody></table>")

    html_lines.append("<div class='callout-warn'><strong>Key Takeaway &amp; Override Decisions:</strong><br>")
    for c in candidate_results:
        html_lines.append(f"• <strong>{c['name']}:</strong> {c['verdict']} — {c['override_note']}<br>")
    html_lines.append("</div>")

    html_lines.append("<h2>2) Gap Matrix</h2>")
    for c in candidate_results:
        html_lines.append(f"<div class='candidate-heading'>Candidate: {c['name']}</div>")
        html_lines.append("<table><thead><tr><th>Skill / Area</th><th>JD Expectation</th><th>Requirement</th><th>Status</th><th>Evidence (Key Line / Deliverable)</th></tr></thead><tbody>")
        for k, v in c["mandatory"].items():
            exp_text = DEFAULT_MANDATORY_WEIGHTS.get(k, (0, "Mandatory Technical Skill"))[1]
            html_lines.append(f"<tr><td><strong>{k}</strong></td><td>{exp_text}</td><td>Mandatory</td><td>{v[0]}</td><td>{v[1]}</td></tr>")
        for k, v in c["good_to_have"].items():
            exp_text = DEFAULT_GOOD_TO_HAVE_WEIGHTS.get(k, (0, "Preferred Skill"))[1]
            html_lines.append(f"<tr><td><strong>{k}</strong></td><td>{exp_text}</td><td>Good-to-have</td><td>{v[0]}</td><td>{v[1]}</td></tr>")
        html_lines.append("</tbody></table>")

    html_lines.append("<h2>3) Candidate Details</h2>")
    for idx, c in enumerate(candidate_results, 1):
        html_lines.append(f"<h3>{idx}. {c['name']}</h3>")
        html_lines.append(f"<p><strong>Verdict:</strong> {c['verdict']}<br><strong>Experience:</strong> {c['years_exp']} years &nbsp;|&nbsp; <strong>Score:</strong> <strong>{c['final_score']} / 100</strong></p>")
        html_lines.append(f"<ul><li><strong>Score Breakdown:</strong> Mandatory {c['mandatory_score']}/85, Bonus {c['good_score']}/10, Exp Fit {c['exp_score']}/5 &rarr; Raw: {c['raw_score']}/100</li>")
        html_lines.append(f"<li><strong>Override Decision:</strong> {c['override_note']}</li></ul>")

    html_lines.append("</body></html>")
    html_content = "\n".join(html_lines)
    html_path = report_sub / f"candidate_screening_report_{date_str}.html"
    html_path.write_text(html_content, encoding="utf-8")

    # PDF Generation (Guaranteed Vector PDF + Browser fallback)
    pdf_path = report_sub / f"candidate_screening_report_{date_str}.pdf"
    pdf_bytes = build_pdf_report(date_str, candidate_results, file_names, active_jd_display)
    
    # Try high-fidelity headless browser print if available
    browser_bins = [
        os.environ.get("CHROME_BIN"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    ]
    browser_path = next((b for b in browser_bins if b and os.path.exists(b)), None)
    if browser_path:
        try:
            cmd = f'"{browser_path}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{pdf_path}" "file:///{html_path}"'
            subprocess.run(cmd, shell=True, capture_output=True)
            if pdf_path.exists() and pdf_path.stat().st_size > 0:
                pdf_bytes = pdf_path.read_bytes()
        except Exception:
            pass

    # Ensure PDF file is written
    if pdf_bytes:
        pdf_path.write_bytes(pdf_bytes)

    return md_content, html_content, pdf_bytes, pdf_path

# ================= UI LAYOUT =================
st.markdown('<div class="main-header">🎯 AI Candidate Screener Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Autonomous, evidence-driven ATS candidate evaluation powered by strict deliverable verification and rubric scoring.</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📄 1. Target Job Description (Optional)")
    custom_jd_upload = st.file_uploader(
        "Upload Custom Job Description (Leave empty for default SDET JD)",
        type=["pdf", "docx", "txt", "md"],
        help="Optional: Upload a role-specific JD to screen against custom requirements."
    )
    if custom_jd_upload:
        st.success(f"✅ Using Custom JD: **{custom_jd_upload.name}**")
    else:
        st.info("ℹ️ Using Active Ground Truth: **Default SDET JD (6–10 Yrs)**")

with col2:
    st.subheader("👥 2. Candidate Profiles (Required)")
    uploaded_resumes = st.file_uploader(
        "Upload Candidate Resumes",
        type=["pdf", "docx", "doc", "txt"],
        accept_multiple_files=True,
        help="Upload one or multiple candidate resume files."
    )
    if uploaded_resumes:
        st.write(f"📁 Selected **{len(uploaded_resumes)}** candidate resume(s)")

st.divider()

if st.button("🚀 Screen Candidate Profiles", type="primary", use_container_width=True, disabled=not uploaded_resumes):
    try:
        with st.spinner("⏳ Ingesting profiles, parsing evidence, and calculating rubric overrides..."):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            upload_sub = RESUMES_DIR / timestamp
            upload_sub.mkdir(parents=True, exist_ok=True)

            custom_jd_text = None
            jd_display_name = "references/job-description.md (Default SDET 6–10 Yrs)"
            if custom_jd_upload:
                jd_bytes = custom_jd_upload.getvalue()
                (upload_sub / custom_jd_upload.name).write_bytes(jd_bytes)
                custom_jd_text = extract_text_from_bytes(custom_jd_upload.name, jd_bytes)
                role_title, _, _ = parse_custom_jd(custom_jd_text)
                jd_display_name = f"Custom JD: {role_title} ({custom_jd_upload.name})"
            elif DEFAULT_JD_PATH.exists():
                custom_jd_text = DEFAULT_JD_PATH.read_text(encoding="utf-8", errors="ignore")
            else:
                custom_jd_text = FALLBACK_DEFAULT_JD_TEXT

            candidate_results = []
            file_names = []
            for r_file in uploaded_resumes:
                r_bytes = r_file.getvalue()
                (upload_sub / r_file.name).write_bytes(r_bytes)
                text = extract_text_from_bytes(r_file.name, r_bytes)
                cand_name = pathlib.Path(r_file.name).stem.replace("Naukri_", "").replace("_", " ").split("[")[0].strip()
                res = evaluate_candidate(cand_name, text, custom_jd_text=custom_jd_text)
                candidate_results.append(res)
                file_names.append(r_file.name)

            candidate_results.sort(key=lambda x: x["final_score"], reverse=True)
            md_content, html_content, pdf_bytes, pdf_path = generate_report_files(timestamp, candidate_results, file_names, jd_display_name)

            st.session_state["results"] = candidate_results
            st.session_state["active_jd"] = jd_display_name
            st.session_state["md_content"] = md_content
            st.session_state["html_content"] = html_content
            st.session_state["pdf_bytes"] = pdf_bytes
            st.session_state["pdf_path"] = str(pdf_path)
            st.success(f"🎉 Successfully screened {len(candidate_results)} candidate profile(s)!")
    except Exception as e:
        st.error(f"❌ Error during screening: {str(e)}")

if "results" in st.session_state:
    results = st.session_state["results"]
    st.subheader("🏆 Candidate Ranking & Leaderboard")
    st.caption(f"Evaluated against: **{st.session_state['active_jd']}** ({len(results)} candidate profiles)")

    # Ranking Table
    table_rows = []
    for idx, c in enumerate(results, 1):
        missing_m = [k for k, v in c["mandatory"].items() if v[0] == "Missing"]
        missing_str = ", ".join(missing_m) if missing_m else "—"
        table_rows.append({
            "Rank": f"#{idx}",
            "Candidate": c["name"],
            "Score": f"{c['final_score']} / 100",
            "Verdict": c["verdict"],
            "Total Exp": f"{c['years_exp']} yrs",
            "Missing (Mandatory)": missing_str,
            "Override Decision": c["override_note"]
        })
    st.table(table_rows)

    # Key Takeaways
    with st.expander("💡 Key Takeaways & Override Decisions", expanded=True):
        for c in results:
            st.markdown(f"• **{c['name']}:** {c['verdict']} — *{c['override_note']}*")

    # Gap Matrices
    st.subheader("📊 4-Tier Evidence Gap Matrices")
    for c in results:
        with st.expander(f"Candidate: {c['name']} — Score: {c['final_score']} / 100", expanded=False):
            st.markdown(f"**Tag Line:** {c['verdict']}")
            st.markdown(f"**Score Breakdown:** Mandatory `{c['mandatory_score']}/85` | Bonus `{c['good_score']}/10` | Experience Fit `{c['exp_score']}/5` &rarr; **Total: `{c['final_score']}/100`**")
            
            gap_data = []
            for k, v in c["mandatory"].items():
                gap_data.append({"Skill / Area": k, "Requirement": "Mandatory", "Status": v[0], "Evidence": v[1]})
            for k, v in c["good_to_have"].items():
                gap_data.append({"Skill / Area": k, "Requirement": "Good-to-have", "Status": v[0], "Evidence": v[1]})
            st.dataframe(gap_data, use_container_width=True)

    # Export Section
    st.subheader("📥 Export & Download Audit Reports")
    d_col1, d_col2, d_col3 = st.columns(3)
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    with d_col1:
        st.download_button(
            label="📝 Download Markdown Report",
            data=st.session_state["md_content"],
            file_name=f"candidate_screening_report_{today_str}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with d_col2:
        st.download_button(
            label="🌐 Download HTML Twin",
            data=st.session_state["html_content"],
            file_name=f"candidate_screening_report_{today_str}.html",
            mime="text/html",
            use_container_width=True
        )
    with d_col3:
        if st.session_state.get("pdf_bytes"):
            st.download_button(
                label="📄 Download Audit PDF Report",
                data=st.session_state["pdf_bytes"],
                file_name=f"candidate_screening_report_{today_str}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        elif st.session_state.get("pdf_path") and os.path.exists(st.session_state["pdf_path"]):
            with open(st.session_state["pdf_path"], "rb") as f:
                st.download_button(
                    label="📄 Download Audit PDF Report",
                    data=f.read(),
                    file_name=f"candidate_screening_report_{today_str}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.button("📄 PDF Rendering in Progress", disabled=True, use_container_width=True)
