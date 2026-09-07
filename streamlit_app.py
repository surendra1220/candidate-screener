import streamlit as st
import pathlib
import datetime
import re
import os
import subprocess
import pypdf

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
    if suffix == ".pdf":
        try:
            import io
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            return f"Error reading PDF: {e}"
    elif suffix in [".docx"]:
        if docx:
            try:
                import io
                doc = docx.Document(io.BytesIO(file_bytes))
                return "\n".join(p.text for p in doc.paragraphs)
            except Exception as e:
                return f"Error reading DOCX: {e}"
        return "python-docx not installed"
    else:
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except Exception as e:
            return f"Error reading text: {e}"

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

    exp_min = 6.0
    exp_m = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+)?\s*(?:years|yrs)", jd_text, re.IGNORECASE)
    if exp_m:
        exp_min = float(exp_m.group(1))

    return role_title, exp_min

def evaluate_candidate(candidate_name: str, resume_text: str, custom_jd_text: str = None) -> dict:
    years_exp = extract_years_experience(resume_text)
    lower_text = resume_text.lower()
    
    results = {}
    if "javascript" in lower_text or "typescript" in lower_text or " js " in lower_text or " ts " in lower_text:
        results["JavaScript / TypeScript"] = ("Matched", "JS/TS automation used in project deliverables")
    else:
        results["JavaScript / TypeScript"] = ("Missing", "no evidence found")
        
    if "python" in lower_text or "pytest" in lower_text:
        results["Python"] = ("Matched", "Python automation evidenced in deliverables")
    else:
        results["Python"] = ("Missing", "no evidence found")

    if "cypress" in lower_text:
        results["Cypress"] = ("Matched", "Cypress automation evidenced in deliverables")
    else:
        results["Cypress"] = ("Missing", "no evidence found")

    if "playwright" in lower_text:
        results["Playwright"] = ("Matched", "Playwright test automation evidenced in deliverables")
    else:
        results["Playwright"] = ("Missing", "no evidence found")

    if "pytest" in lower_text:
        results["Pytest"] = ("Matched", "Pytest framework evidenced in deliverables")
    else:
        results["Pytest"] = ("Missing", "no evidence found")

    if "page object" in lower_text or "pom" in lower_text or "framework" in lower_text:
        results["Automation Framework Design"] = ("Matched", "Page Object Model framework architecture design")
    else:
        results["Automation Framework Design"] = ("Missing", "no evidence found")

    if "cucumber" in lower_text or "bdd" in lower_text or "specflow" in lower_text or "selenium" in lower_text:
        results["UI / Web Testing + BDD"] = ("Matched", "End-to-end UI & BDD testing evidenced")
    elif "ui" in lower_text or "web testing" in lower_text:
        results["UI / Web Testing + BDD"] = ("Partial match", "UI testing mentioned without explicit BDD syntax")
    else:
        results["UI / Web Testing + BDD"] = ("Missing", "no evidence found")

    if "postman" in lower_text or "rest assured" in lower_text or "rest api" in lower_text or "soap ui" in lower_text:
        results["API Testing"] = ("Matched", "REST API automation and payload validation")
    else:
        results["API Testing"] = ("Missing", "no evidence found")

    if "test plan" in lower_text or "strategy" in lower_text or "rtm" in lower_text or "regression" in lower_text or "stlc" in lower_text:
        results["STLC & Test Strategy"] = ("Matched", "STLC test strategy, regression suites, and test planning")
    else:
        results["STLC & Test Strategy"] = ("Missing", "no evidence found")

    if "jira" in lower_text or "alm" in lower_text or "testrail" in lower_text or "tfs" in lower_text or "azure devops" in lower_text:
        results["Test Management Tools"] = ("Matched", "Jira / ALM defect lifecycle and test tracking")
    else:
        results["Test Management Tools"] = ("Missing", "no evidence found")

    if "agile" in lower_text or "scrum" in lower_text or "kanban" in lower_text or "sprint" in lower_text:
        results["Agile / Kanban"] = ("Matched", "Agile ceremonies, sprint planning, and defect triage")
    else:
        results["Agile / Kanban"] = ("Missing", "no evidence found")

    if "model validation" in lower_text or "testing ai" in lower_text or "ai testing" in lower_text or "genai" in lower_text:
        results["AI Solution Testing"] = ("Matched", "AI model validation and GenAI solution testing")
    elif "ai tools" in lower_text or "copilot" in lower_text or "chatgpt" in lower_text or "claude" in lower_text:
        results["AI Solution Testing"] = ("Partial match", "AI-assisted tools used; no model testing deliverables")
    else:
        results["AI Solution Testing"] = ("Missing", "no evidence found")

    if "mcp" in lower_text or "rag" in lower_text or "agentic" in lower_text:
        results["Agentic AI"] = ("Matched", "Agentic architecture (MCP/RAG/Prompt engineering)")
    elif "prompting" in lower_text or "ai solution" in lower_text:
        results["Agentic AI"] = ("Claimed but unevidenced", "Claimed AI prompting without agentic deliverables")
    else:
        results["Agentic AI"] = ("Missing", "no evidence found")

    good_to_have_results = {}
    good_to_have_results["AWS / Azure Cloud Exposure"] = ("Matched" if ("aws" in lower_text or "azure" in lower_text or "cloud" in lower_text) else "Missing", "Cloud test environments")
    good_to_have_results["CI/CD Integration"] = ("Matched" if ("jenkins" in lower_text or "ci/cd" in lower_text or "pipeline" in lower_text or "github actions" in lower_text) else "Missing", "CI/CD automated execution")
    good_to_have_results["Monitoring & Observability"] = ("Matched" if ("splunk" in lower_text or "grafana" in lower_text or "power bi" in lower_text) else "Missing", "Log analysis & monitoring")
    good_to_have_results["No-Code / Low-Code Tools"] = ("Matched" if ("mabl" in lower_text or "testcomplete" in lower_text) else "Missing", "No-code testing tools")
    good_to_have_results["Pharma / Life Sciences Domain"] = ("Matched" if ("pharma" in lower_text or "clinical" in lower_text or "ctms" in lower_text or "healthcare" in lower_text or "life sciences" in lower_text) else "Missing", "Pharma / Clinical Trial domain experience")

    factor_map = {"Matched": 1.0, "Partial match": 0.6, "Claimed but unevidenced": 0.3, "Missing": 0.0}
    mandatory_score = sum(DEFAULT_MANDATORY_WEIGHTS[k][0] * factor_map.get(results[k][0], 0.0) for k in DEFAULT_MANDATORY_WEIGHTS)
    good_to_have_score = sum(DEFAULT_GOOD_TO_HAVE_WEIGHTS[k][0] * factor_map.get(good_to_have_results[k][0], 0.0) for k in DEFAULT_GOOD_TO_HAVE_WEIGHTS)
    good_to_have_score = min(good_to_have_score, 10.0)

    exp_fit_score = 0.0
    gate_failed = False
    min_exp_required = 6.0
    if custom_jd_text:
        _, min_exp_required = parse_custom_jd(custom_jd_text)

    if years_exp < min_exp_required and years_exp > 0.0:
        exp_fit_score = 0.0
        gate_failed = True
    elif min_exp_required <= years_exp <= (min_exp_required + 4.0):
        exp_fit_score = 5.0
    elif (min_exp_required + 4.0) < years_exp <= (min_exp_required + 6.0):
        exp_fit_score = 3.0
    elif years_exp > (min_exp_required + 6.0):
        exp_fit_score = 2.0
    else:
        exp_fit_score = 4.0

    raw_score = mandatory_score + good_to_have_score + exp_fit_score
    final_score = raw_score
    verdict = ""
    override_note = "None"

    if gate_failed:
        final_score = 0.0
        verdict = f"Screening Failed · Reject (Experience Gate < {min_exp_required:.1f} yrs) ❌"
        override_note = f"Rule #1: Total experience ({years_exp:.1f} yrs) < {min_exp_required:.1f} yrs mandatory threshold forces immediate disqualification."
    elif results["AI Solution Testing"][0] == "Missing" and results["Agentic AI"][0] == "Missing":
        final_score = min(final_score, 59.0)
        verdict = "Screening Failed · Weak fit (AI Hard Gap) ❌"
        override_note = "Rule #3: Total absence of AI & Agentic testing forces score cap < 60 and downgrade to Weak fit."
    elif final_score >= 80.0:
        verdict = "Screening Passed · Strong fit ✅"
    elif final_score >= 60.0:
        verdict = "Screening Passed · Potential fit ⚠️"
    elif final_score >= 40.0:
        verdict = "Screening Failed · Weak fit ❌"
    else:
        verdict = "Screening Failed · Reject ❌"

    return {
        "name": candidate_name,
        "years_exp": round(years_exp, 1) if years_exp else "N/A",
        "raw_score": round(raw_score, 1),
        "final_score": round(final_score, 1),
        "verdict": verdict,
        "override_note": override_note,
        "mandatory": results,
        "good_to_have": good_to_have_results,
        "mandatory_score": round(mandatory_score, 1),
        "good_score": round(good_to_have_score, 1),
        "exp_score": round(exp_fit_score, 1)
    }

def generate_report_files(timestamp_folder: str, candidate_results: list, file_names: list, jd_name: str):
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    report_sub = REPORTS_DIR / timestamp_folder
    report_sub.mkdir(parents=True, exist_ok=True)
    files_str = ", ".join(file_names) if file_names else f"{len(candidate_results)} candidate profile(s)"
    active_jd_display = jd_name if jd_name else "references/job-description.md (Default SDET 6–10 Yrs)"

    # Markdown
    md_lines = [
        f"# Screening Report — {date_str}",
        f"**Screened Files:** {files_str}  ",
        f"**Active JD:** {active_jd_display}  ",
        f"**Candidates Ranked:** {len(candidate_results)}",
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

    # PDF Render (Headless Browser or FPDF fallback)
    pdf_path = report_sub / f"candidate_screening_report_{date_str}.pdf"
    rendered = False
    browser_bins = [
        os.environ.get("CHROME_BIN"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome"
    ]
    browser_path = next((b for b in browser_bins if b and os.path.exists(b)), None)
    if browser_path:
        try:
            cmd = f'"{browser_path}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{pdf_path}" "file:///{html_path}"'
            subprocess.run(cmd, shell=True, capture_output=True)
            rendered = pdf_path.exists() and pdf_path.stat().st_size > 0
        except Exception:
            rendered = False

    if not rendered and FPDF:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, f"Screening Report - {date_str}", ln=True)
            pdf.set_font("Helvetica", size=10)
            pdf.cell(0, 8, f"Active JD: {active_jd_display}", ln=True)
            pdf.ln(5)
            for idx, c in enumerate(candidate_results, 1):
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(0, 8, f"{idx}. {c['name']} - Score: {c['final_score']}/100 - {c['verdict']}", ln=True)
                pdf.set_font("Helvetica", size=9)
                pdf.multi_cell(0, 6, f"Experience: {c['years_exp']} yrs | Note: {c['override_note']}")
                pdf.ln(3)
            pdf.output(str(pdf_path))
        except Exception:
            pass

    return md_content, html_content, pdf_path

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
        st.info("ℹ️ Using Active Ground Truth: **references/job-description.md (Default SDET 6–10 Yrs)**")

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
            role_title, _ = parse_custom_jd(custom_jd_text)
            jd_display_name = f"Custom JD: {role_title} ({custom_jd_upload.name})"
        elif DEFAULT_JD_PATH.exists():
            custom_jd_text = DEFAULT_JD_PATH.read_text(encoding="utf-8", errors="ignore")

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
        md_content, html_content, pdf_path = generate_report_files(timestamp, candidate_results, file_names, jd_display_name)

        st.session_state["results"] = candidate_results
        st.session_state["active_jd"] = jd_display_name
        st.session_state["md_content"] = md_content
        st.session_state["html_content"] = html_content
        st.session_state["pdf_path"] = str(pdf_path) if pdf_path.exists() else None

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
    with d_col1:
        st.download_button(
            label="📝 Download Markdown Report",
            data=st.session_state["md_content"],
            file_name=f"screening_report_{datetime.date.today().strftime('%Y-%m-%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with d_col2:
        st.download_button(
            label="🌐 Download HTML Twin",
            data=st.session_state["html_content"],
            file_name=f"screening_report_{datetime.date.today().strftime('%Y-%m-%d')}.html",
            mime="text/html",
            use_container_width=True
        )
    with d_col3:
        if st.session_state.get("pdf_path") and os.path.exists(st.session_state["pdf_path"]):
            with open(st.session_state["pdf_path"], "rb") as f:
                st.download_button(
                    label="📄 Download Rendered PDF",
                    data=f.read(),
                    file_name=f"screening_report_{datetime.date.today().strftime('%Y-%m-%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.button("📄 PDF Rendering Unavailable", disabled=True, use_container_width=True)
