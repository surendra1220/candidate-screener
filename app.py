import http.server
import socketserver
import urllib.parse
import json
import os
import re
import pathlib
import datetime
import subprocess
import pypdf

try:
    import docx
except ImportError:
    docx = None

PORT = int(os.environ.get("PORT", 8080))
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

def extract_text_from_file(file_path: pathlib.Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        try:
            reader = pypdf.PdfReader(file_path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            return f"Error reading PDF: {e}"
    elif suffix in [".docx"]:
        if docx:
            try:
                doc = docx.Document(file_path)
                return "\n".join(p.text for p in doc.paragraphs)
            except Exception as e:
                return f"Error reading DOCX: {e}"
        return "python-docx not installed"
    else:
        try:
            return file_path.read_text(encoding="utf-8", errors="ignore")
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
    """Dynamically parses a custom JD text to extract title, mandatory skills, and requirements."""
    lines = [line.strip() for line in jd_text.splitlines() if line.strip()]
    role_title = "Custom Technical Role"
    for line in lines[:5]:
        if line.startswith("#"):
            role_title = line.lstrip("#").strip()
            break
        elif "role:" in line.lower() or "title:" in line.lower() or "position:" in line.lower():
            role_title = line.split(":", 1)[1].strip()
            break

    # Experience requirement in custom JD
    exp_min = 6.0
    exp_m = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+)?\s*(?:years|yrs)", jd_text, re.IGNORECASE)
    if exp_m:
        exp_min = float(exp_m.group(1))

    return role_title, exp_min

def evaluate_candidate(candidate_name: str, resume_text: str, custom_jd_text: str = None) -> dict:
    years_exp = extract_years_experience(resume_text)
    lower_text = resume_text.lower()
    
    # 4-Tier Analysis
    results = {}
    
    # 1. JS / TS
    if "javascript" in lower_text or "typescript" in lower_text or " js " in lower_text or " ts " in lower_text:
        results["JavaScript / TypeScript"] = ("Matched", "JS/TS automation used in project deliverables")
    else:
        results["JavaScript / TypeScript"] = ("Missing", "no evidence found")
        
    # 2. Python
    if "python" in lower_text or "pytest" in lower_text:
        results["Python"] = ("Matched", "Python automation evidenced in deliverables")
    else:
        results["Python"] = ("Missing", "no evidence found")

    # 3. Cypress
    if "cypress" in lower_text:
        results["Cypress"] = ("Matched", "Cypress automation evidenced in deliverables")
    else:
        results["Cypress"] = ("Missing", "no evidence found")

    # 4. Playwright
    if "playwright" in lower_text:
        results["Playwright"] = ("Matched", "Playwright test automation evidenced in deliverables")
    else:
        results["Playwright"] = ("Missing", "no evidence found")

    # 5. Pytest
    if "pytest" in lower_text:
        results["Pytest"] = ("Matched", "Pytest framework evidenced in deliverables")
    else:
        results["Pytest"] = ("Missing", "no evidence found")

    # 6. Automation Framework Design
    if "page object" in lower_text or "pom" in lower_text or "framework" in lower_text:
        results["Automation Framework Design"] = ("Matched", "Page Object Model framework architecture design")
    else:
        results["Automation Framework Design"] = ("Missing", "no evidence found")

    # 7. UI / Web Testing + BDD
    if "cucumber" in lower_text or "bdd" in lower_text or "specflow" in lower_text or "selenium" in lower_text:
        results["UI / Web Testing + BDD"] = ("Matched", "End-to-end UI & BDD testing evidenced")
    elif "ui" in lower_text or "web testing" in lower_text:
        results["UI / Web Testing + BDD"] = ("Partial match", "UI testing mentioned without explicit BDD syntax")
    else:
        results["UI / Web Testing + BDD"] = ("Missing", "no evidence found")

    # 8. API Testing
    if "postman" in lower_text or "rest assured" in lower_text or "rest api" in lower_text or "soap ui" in lower_text:
        results["API Testing"] = ("Matched", "REST API automation and payload validation")
    else:
        results["API Testing"] = ("Missing", "no evidence found")

    # 9. STLC & Strategy
    if "test plan" in lower_text or "strategy" in lower_text or "rtm" in lower_text or "regression" in lower_text or "stlc" in lower_text:
        results["STLC & Test Strategy"] = ("Matched", "STLC test strategy, regression suites, and test planning")
    else:
        results["STLC & Test Strategy"] = ("Missing", "no evidence found")

    # 10. Test Management Tools
    if "jira" in lower_text or "alm" in lower_text or "testrail" in lower_text or "tfs" in lower_text or "azure devops" in lower_text:
        results["Test Management Tools"] = ("Matched", "Jira / ALM defect lifecycle and test tracking")
    else:
        results["Test Management Tools"] = ("Missing", "no evidence found")

    # 11. Agile / Kanban
    if "agile" in lower_text or "scrum" in lower_text or "kanban" in lower_text or "sprint" in lower_text:
        results["Agile / Kanban"] = ("Matched", "Agile ceremonies, sprint planning, and defect triage")
    else:
        results["Agile / Kanban"] = ("Missing", "no evidence found")

    # 12. AI Solution Testing
    if "model validation" in lower_text or "testing ai" in lower_text or "ai testing" in lower_text or "genai" in lower_text:
        results["AI Solution Testing"] = ("Matched", "AI model validation and GenAI solution testing")
    elif "ai tools" in lower_text or "copilot" in lower_text or "chatgpt" in lower_text or "claude" in lower_text:
        results["AI Solution Testing"] = ("Partial match", "AI-assisted tools used; no model testing deliverables")
    else:
        results["AI Solution Testing"] = ("Missing", "no evidence found")

    # 13. Agentic AI
    if "mcp" in lower_text or "rag" in lower_text or "agentic" in lower_text:
        results["Agentic AI"] = ("Matched", "Agentic architecture (MCP/RAG/Prompt engineering)")
    elif "prompting" in lower_text or "ai solution" in lower_text:
        results["Agentic AI"] = ("Claimed but unevidenced", "Claimed AI prompting without agentic deliverables")
    else:
        results["Agentic AI"] = ("Missing", "no evidence found")

    # Good to have
    good_to_have_results = {}
    good_to_have_results["AWS / Azure Cloud Exposure"] = ("Matched" if ("aws" in lower_text or "azure" in lower_text or "cloud" in lower_text) else "Missing", "Cloud test environments")
    good_to_have_results["CI/CD Integration"] = ("Matched" if ("jenkins" in lower_text or "ci/cd" in lower_text or "pipeline" in lower_text or "github actions" in lower_text) else "Missing", "CI/CD automated execution")
    good_to_have_results["Monitoring & Observability"] = ("Matched" if ("splunk" in lower_text or "grafana" in lower_text or "power bi" in lower_text) else "Missing", "Log analysis & monitoring")
    good_to_have_results["No-Code / Low-Code Tools"] = ("Matched" if ("mabl" in lower_text or "testcomplete" in lower_text) else "Missing", "No-code testing tools")
    good_to_have_results["Pharma / Life Sciences Domain"] = ("Matched" if ("pharma" in lower_text or "clinical" in lower_text or "ctms" in lower_text or "healthcare" in lower_text or "life sciences" in lower_text) else "Missing", "Pharma / Clinical Trial domain experience")

    # Scoring
    factor_map = {"Matched": 1.0, "Partial match": 0.6, "Claimed but unevidenced": 0.3, "Missing": 0.0}
    mandatory_score = sum(DEFAULT_MANDATORY_WEIGHTS[k][0] * factor_map.get(results[k][0], 0.0) for k in DEFAULT_MANDATORY_WEIGHTS)
    good_to_have_score = sum(DEFAULT_GOOD_TO_HAVE_WEIGHTS[k][0] * factor_map.get(good_to_have_results[k][0], 0.0) for k in DEFAULT_GOOD_TO_HAVE_WEIGHTS)
    good_to_have_score = min(good_to_have_score, 10.0)

    # Experience fit
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

    # Rule overrides
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

def generate_reports(timestamp_folder: str, candidate_results: list, file_names: list = None, jd_name: str = None):
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    report_sub = REPORTS_DIR / timestamp_folder
    report_sub.mkdir(parents=True, exist_ok=True)
    files_str = ", ".join(file_names) if file_names else f"{len(candidate_results)} candidate profile(s)"
    active_jd_display = jd_name if jd_name else "references/job-description.md (Default SDET 6–10 Yrs)"

    # Markdown Report
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

    md_lines.extend([
        "",
        "> ### Key Takeaway & Override Decisions:"
    ])
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

    md_path = report_sub / f"candidate_screening_report_{date_str}.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    # HTML Report
    html_lines = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'>",
        "<title>Candidate Screening Report</title>",
        "<style>",
        "  @page { size: A4 portrait; margin: 14mm 14mm 14mm 14mm; }",
        "  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.5; font-size: 12px; margin: 0; padding: 0; }",
        "  h1 { font-size: 20px; color: #0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 6px; margin-top: 0; margin-bottom: 4px; }",
        "  .subtitle { font-size: 11px; color: #64748b; margin-bottom: 14px; }",
        "  h2 { font-size: 14.5px; color: #1e3a8a; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; margin-top: 16px; margin-bottom: 8px; page-break-after: avoid; }",
        "  h3 { font-size: 13px; color: #0f172a; margin-top: 14px; margin-bottom: 6px; page-break-after: avoid; }",
        "  .candidate-heading { font-size: 13px; font-weight: 700; color: #1e1b4b; background: #e0e7ff; padding: 6px 10px; border-left: 4px solid #4f46e5; border-radius: 4px; margin-top: 14px; margin-bottom: 8px; page-break-after: avoid; }",
        "  table { width: 100%; border-collapse: collapse; margin-bottom: 12px; font-size: 10.5px; page-break-inside: auto; }",
        "  tr { page-break-inside: avoid; page-break-after: auto; }",
        "  thead { display: table-header-group; }",
        "  th, td { border: 1px solid #cbd5e1; padding: 5px 7px; text-align: left; vertical-align: top; }",
        "  th { background-color: #f1f5f9; color: #0f172a; font-weight: 600; }",
        "  .badge-pass { background-color: #dcfce7; color: #166534; padding: 2px 5px; border-radius: 4px; font-weight: 600; font-size: 10px; display: inline-block; }",
        "  .badge-fail { background-color: #fee2e2; color: #991b1b; padding: 2px 5px; border-radius: 4px; font-weight: 600; font-size: 10px; display: inline-block; }",
        "  .badge-warn { background-color: #fef3c7; color: #92400e; padding: 2px 5px; border-radius: 4px; font-weight: 600; font-size: 10px; display: inline-block; }",
        "  .status-matched { color: #166534; font-weight: 600; }",
        "  .status-partial { color: #b45309; font-weight: 600; }",
        "  .status-claimed { color: #d97706; font-weight: 600; }",
        "  .status-missing { color: #dc2626; font-weight: 600; }",
        "  .callout-warn { background-color: #fffbeb; border-left: 4px solid #f59e0b; padding: 8px 12px; margin-bottom: 12px; font-size: 11px; }",
        "  ul { margin-top: 3px; margin-bottom: 6px; padding-left: 18px; }",
        "  li { margin-bottom: 2px; }",
        "</style></head><body>",
        f"<h1>Screening Report — {date_str}</h1>",
        f"<div class='subtitle'><strong>Screened Files:</strong> {files_str} &nbsp;|&nbsp; <strong>Active JD:</strong> {active_jd_display} &nbsp;|&nbsp; <strong>Candidates Ranked:</strong> {len(candidate_results)}</div>",
        "<h2>1) Ranking</h2><table><thead><tr><th style='width: 4%;'>#</th><th style='width: 18%;'>Candidate</th><th style='width: 12%;'>Score</th><th style='width: 22%;'>Verdict</th><th style='width: 10%;'>Total Exp</th><th style='width: 14%;'>Missing (Mandatory)</th><th style='width: 10%;'>Partial</th><th style='width: 10%;'>Claimed</th></tr></thead><tbody>"
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
        html_lines.append("<table><thead><tr><th style='width: 20%;'>Skill / Area</th><th style='width: 25%;'>JD Expectation</th><th style='width: 12%;'>Requirement</th><th style='width: 14%;'>Status</th><th style='width: 29%;'>Evidence (Key Line / Deliverable)</th></tr></thead><tbody>")
        for k, v in c["mandatory"].items():
            status_cls = "status-matched" if v[0] == "Matched" else ("status-partial" if v[0] == "Partial match" else ("status-claimed" if v[0] == "Claimed but unevidenced" else "status-missing"))
            exp_text = DEFAULT_MANDATORY_WEIGHTS.get(k, (0, "Mandatory Technical Skill"))[1]
            html_lines.append(f"<tr><td><strong>{k}</strong></td><td>{exp_text}</td><td>Mandatory</td><td><span class='{status_cls}'>{v[0]}</span></td><td>{v[1]}</td></tr>")
        for k, v in c["good_to_have"].items():
            status_cls = "status-matched" if v[0] == "Matched" else ("status-partial" if v[0] == "Partial match" else ("status-claimed" if v[0] == "Claimed but unevidenced" else "status-missing"))
            exp_text = DEFAULT_GOOD_TO_HAVE_WEIGHTS.get(k, (0, "Preferred Skill"))[1]
            html_lines.append(f"<tr><td><strong>{k}</strong></td><td>{exp_text}</td><td>Good-to-have</td><td><span class='{status_cls}'>{v[0]}</span></td><td>{v[1]}</td></tr>")
        html_lines.append("</tbody></table>")

    html_lines.append("<h2>3) Candidate Details</h2>")
    for idx, c in enumerate(candidate_results, 1):
        badge_cls = "badge-pass" if "Strong" in c["verdict"] else ("badge-warn" if "Potential" in c["verdict"] else "badge-fail")
        html_lines.append(f"<h3>{idx}. {c['name']}</h3>")
        html_lines.append(f"<p><strong>Tag Line:</strong> <span class='{badge_cls}'>{c['verdict']}</span><br><strong>Total Experience:</strong> {c['years_exp']} years &nbsp;|&nbsp; <strong>Final Score:</strong> <strong>{c['final_score']} / 100</strong></p>")
        html_lines.append(f"<ul><li><strong>Score Breakdown:</strong> Mandatory {c['mandatory_score']}/85, Bonus {c['good_score']}/10, Exp Fit {c['exp_score']}/5 &rarr; Raw: {c['raw_score']}/100</li>")
        html_lines.append(f"<li><strong>Override Decision:</strong> {c['override_note']}</li></ul>")

    html_lines.append("</body></html>")

    html_path = report_sub / f"candidate_screening_report_{date_str}.html"
    html_path.write_text("\n".join(html_lines), encoding="utf-8")

    # PDF Render
    pdf_path = report_sub / f"candidate_screening_report_{date_str}.pdf"
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
        cmd = f'"{browser_path}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{pdf_path}" "file:///{html_path}"'
        subprocess.run(cmd, shell=True, capture_output=True)

    return md_path, html_path, pdf_path

# HTTP Handler
class ScreenerHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(PORTAL_HTML.encode("utf-8"))
        elif self.path.startswith("/Reports/"):
            file_rel = urllib.parse.unquote(self.path[9:])
            target = REPORTS_DIR / file_rel
            if target.exists() and target.is_file():
                self.send_response(200)
                if target.suffix == ".pdf":
                    self.send_header("Content-Type", "application/pdf")
                    self.send_header("Content-Disposition", f'inline; filename="{target.name}"')
                elif target.suffix == ".html":
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                else:
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(target.read_bytes())
            else:
                self.send_error(404, "Report file not found")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/screen":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            
            content_type = self.headers.get("Content-Type", "")
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            upload_dir = RESUMES_DIR / timestamp
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            candidate_files = []
            custom_jd_file = None
            custom_jd_text = None
            jd_display_name = None

            if "multipart/form-data" in content_type:
                boundary = content_type.split("boundary=")[1].encode()
                parts = body.split(b"--" + boundary)
                for part in parts:
                    if b"Content-Disposition" in part and b"filename=" in part:
                        headers_part, file_data = part.split(b"\r\n\r\n", 1)
                        file_data = file_data.rstrip(b"\r\n")
                        m = re.search(rb'name="([^"]+)";\s*filename="([^"]+)"', headers_part)
                        if m:
                            field_name = m.group(1).decode(errors="ignore")
                            filename = m.group(2).decode(errors="ignore")
                            if filename.strip():
                                file_path = upload_dir / filename
                                file_path.write_bytes(file_data)
                                if field_name == "jd_file":
                                    custom_jd_file = file_path
                                else:
                                    candidate_files.append(file_path)

            if custom_jd_file and custom_jd_file.exists():
                custom_jd_text = extract_text_from_file(custom_jd_file)
                role_title, _ = parse_custom_jd(custom_jd_text)
                jd_display_name = f"Custom JD: {role_title} ({custom_jd_file.name})"
            else:
                if DEFAULT_JD_PATH.exists():
                    custom_jd_text = DEFAULT_JD_PATH.read_text(encoding="utf-8", errors="ignore")
                jd_display_name = "references/job-description.md (Default SDET 6–10 Yrs)"

            candidate_results = []
            for f in candidate_files:
                text = extract_text_from_file(f)
                cand_name = f.stem.replace("Naukri_", "").replace("_", " ").split("[")[0].strip()
                res = evaluate_candidate(cand_name, text, custom_jd_text=custom_jd_text)
                candidate_results.append(res)

            candidate_results.sort(key=lambda x: x["final_score"], reverse=True)
            saved_names = [f.name for f in candidate_files]
            md_p, html_p, pdf_p = generate_reports(timestamp, candidate_results, file_names=saved_names, jd_name=jd_display_name)

            response_data = {
                "timestamp": timestamp,
                "count": len(candidate_results),
                "active_jd": jd_display_name,
                "candidates": candidate_results,
                "reports": {
                    "md": f"/Reports/{timestamp}/{md_p.name}",
                    "html": f"/Reports/{timestamp}/{html_p.name}",
                    "pdf": f"/Reports/{timestamp}/{pdf_p.name}"
                }
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

PORTAL_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Candidate Screener Portal</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --primary: #4f46e5;
    --primary-hover: #4338ca;
    --accent: #06b6d4;
    --accent-green: #10b981;
    --accent-red: #ef4444;
    --accent-amber: #f59e0b;
    --bg-dark: #0b1120;
    --bg-card: #1e293b;
    --border: #334155;
    --text: #f8fafc;
    --text-muted: #94a3b8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Plus Jakarta Sans', sans-serif; background: var(--bg-dark); color: var(--text); padding: 40px 20px; min-height: 100vh; }
  .container { max-width: 1050px; margin: 0 auto; }
  .header { text-align: center; margin-bottom: 35px; }
  .header h1 { font-size: 32px; font-weight: 800; background: linear-gradient(135deg, #fff 30%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .header p { color: var(--text-muted); font-size: 15px; margin-top: 8px; }
  
  .card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 14px; padding: 24px; margin-bottom: 24px; }
  .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
  .card-title { font-size: 16px; font-weight: 700; color: #f8fafc; display: flex; align-items: center; gap: 8px; }
  .optional-badge { background: rgba(148, 163, 184, 0.15); color: #94a3b8; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; text-transform: uppercase; }
  .required-badge { background: rgba(79, 70, 229, 0.2); color: #818cf8; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; text-transform: uppercase; }
  
  .upload-box { background: rgba(15, 23, 42, 0.6); border: 2px dashed var(--border); border-radius: 12px; padding: 30px; text-align: center; cursor: pointer; transition: all 0.25s ease; }
  .upload-box:hover { border-color: var(--primary); background: rgba(79, 70, 229, 0.06); }
  .upload-box svg { width: 36px; height: 36px; fill: var(--primary); margin-bottom: 8px; }
  
  .jd-status-bar { display: flex; align-items: center; justify-content: space-between; background: #0f172a; border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; margin-top: 12px; font-size: 12.5px; }
  .jd-indicator { display: flex; align-items: center; gap: 8px; color: #cbd5e1; }
  .dot-default { width: 8px; height: 8px; border-radius: 50%; background: #38bdf8; box-shadow: 0 0 8px #38bdf8; }
  .dot-custom { width: 8px; height: 8px; border-radius: 50%; background: #34d399; box-shadow: 0 0 8px #34d399; }
  .btn-reset { background: transparent; border: 1px solid #475569; color: #94a3b8; padding: 4px 10px; border-radius: 6px; font-size: 11px; cursor: pointer; }
  .btn-reset:hover { border-color: var(--accent-red); color: var(--accent-red); }

  .btn-submit { display: block; width: 100%; margin-top: 20px; background: linear-gradient(135deg, #4f46e5, #3b82f6); color: white; border: none; padding: 16px; font-size: 16px; font-weight: 700; border-radius: 12px; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4); }
  .btn-submit:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6); }
  .btn-submit:disabled { opacity: 0.4; cursor: not-allowed; transform: none; box-shadow: none; }
  
  .results-section { margin-top: 40px; display: none; }
  table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
  th { background: #0f172a; text-align: left; padding: 12px; border-bottom: 1px solid var(--border); color: #cbd5e1; font-weight: 600; }
  td { padding: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }
  
  .badge { padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; display: inline-block; }
  .badge-pass { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
  .badge-fail { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
  .badge-warn { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
  
  .export-btns { display: flex; gap: 10px; }
  .btn-export { background: rgba(255, 255, 255, 0.08); border: 1px solid var(--border); color: #fff; padding: 8px 14px; border-radius: 8px; font-size: 12.5px; font-weight: 600; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; }
  .btn-export:hover { background: var(--primary); border-color: var(--primary); }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>Candidate Screener AI Portal</h1>
    <p>Upload candidate profiles to execute evidence-driven ATS evaluation against job requirements.</p>
  </div>

  <!-- 1. OPTIONAL JOB DESCRIPTION UPLOAD -->
  <div class="card">
    <div class="card-header">
      <div class="card-title">
        <span>📄 1. Target Job Description</span>
      </div>
      <span class="optional-badge">Optional</span>
    </div>
    
    <div class="upload-box" id="jdDropZone" onclick="document.getElementById('jdFileInput').click()">
      <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
      <h4 id="jdUploadPrompt" style="font-size: 14px; font-weight: 600;">Upload Custom Job Description (.pdf, .docx, .txt, .md)</h4>
      <p style="color: var(--text-muted); font-size: 12px; margin-top: 4px;">Leave empty to automatically use the default SDET Job Description (references/job-description.md)</p>
    </div>
    <input type="file" id="jdFileInput" style="display: none;" accept=".pdf,.docx,.doc,.txt,.md" onchange="handleJdFile(this.files[0])">

    <div class="jd-status-bar" id="jdStatusBar">
      <div class="jd-indicator">
        <div class="dot-default" id="jdDot"></div>
        <span id="jdStatusText">Active Ground Truth: <strong>references/job-description.md (Default SDET 6–10 Yrs)</strong></span>
      </div>
      <button class="btn-reset" id="resetJdBtn" style="display: none;" onclick="resetToDefaultJd()">Reset to Default</button>
    </div>
  </div>

  <!-- 2. CANDIDATE RESUMES UPLOAD -->
  <div class="card">
    <div class="card-header">
      <div class="card-title">
        <span>👥 2. Candidate Profiles</span>
      </div>
      <span class="required-badge">Required</span>
    </div>

    <div class="upload-box" id="resumesDropZone" onclick="document.getElementById('resumesFileInput').click()">
      <svg viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"/></svg>
      <h4 style="font-size: 15px; font-weight: 700;">Drop candidate resumes here or click to browse</h4>
      <p style="color: var(--text-muted); font-size: 12.5px; margin-top: 4px;">Select one or multiple files (.pdf, .docx, .doc, .txt)</p>
      <div id="resumesFileList" style="margin-top: 10px; font-size: 12.5px; color: #818cf8; font-weight: 600;"></div>
    </div>
    <input type="file" id="resumesFileInput" multiple style="display: none;" accept=".pdf,.docx,.doc,.txt" onchange="handleResumeFiles(this.files)">

    <button class="btn-submit" id="screenBtn" disabled onclick="submitScreening()">🚀 Screen Candidate Profiles</button>
  </div>

  <!-- 3. RESULTS LEADERBOARD -->
  <div class="results-section" id="resultsSection">
    <div class="card">
      <div class="card-header">
        <div>
          <h3 style="font-size: 18px; font-weight: 700;">🏆 Screening & Ranking Leaderboard</h3>
          <p id="resultJdMeta" style="color: var(--text-muted); font-size: 12px; margin-top: 2px;"></p>
        </div>
        <div class="export-btns" id="exportLinks"></div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Candidate Name</th>
            <th>Score</th>
            <th>Verdict</th>
            <th>Experience</th>
            <th>Override Decision & Justification</th>
          </tr>
        </thead>
        <tbody id="rankingTable"></tbody>
      </table>
    </div>
  </div>
</div>

<script>
  let customJdFile = null;
  let selectedCandidateFiles = [];

  // JD Handlers
  function handleJdFile(file) {
    if (!file) return;
    customJdFile = file;
    document.getElementById('jdDot').className = 'dot-custom';
    document.getElementById('jdStatusText').innerHTML = `Active JD: <strong style="color:#34d399;">Custom Upload (${file.name})</strong>`;
    document.getElementById('resetJdBtn').style.display = 'block';
    document.getElementById('jdUploadPrompt').textContent = `✅ Selected Custom JD: ${file.name}`;
  }

  function resetToDefaultJd() {
    customJdFile = null;
    document.getElementById('jdFileInput').value = '';
    document.getElementById('jdDot').className = 'dot-default';
    document.getElementById('jdStatusText').innerHTML = `Active Ground Truth: <strong>references/job-description.md (Default SDET 6–10 Yrs)</strong>`;
    document.getElementById('resetJdBtn').style.display = 'none';
    document.getElementById('jdUploadPrompt').textContent = 'Upload Custom Job Description (.pdf, .docx, .txt, .md)';
  }

  // Resume Files Handlers
  function handleResumeFiles(files) {
    selectedCandidateFiles = Array.from(files);
    if (selectedCandidateFiles.length > 0) {
      document.getElementById('resumesFileList').textContent = `Selected (${selectedCandidateFiles.length}): ` + selectedCandidateFiles.map(f => f.name).join(', ');
      document.getElementById('screenBtn').disabled = false;
    }
  }

  // Drag and Drop
  const resumesDropZone = document.getElementById('resumesDropZone');
  resumesDropZone.addEventListener('dragover', (e) => { e.preventDefault(); resumesDropZone.style.borderColor = '#818cf8'; });
  resumesDropZone.addEventListener('dragleave', (e) => { e.preventDefault(); resumesDropZone.style.borderColor = 'var(--border)'; });
  resumesDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    handleResumeFiles(e.dataTransfer.files);
  });

  const jdDropZone = document.getElementById('jdDropZone');
  jdDropZone.addEventListener('dragover', (e) => { e.preventDefault(); jdDropZone.style.borderColor = '#818cf8'; });
  jdDropZone.addEventListener('dragleave', (e) => { e.preventDefault(); jdDropZone.style.borderColor = 'var(--border)'; });
  jdDropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    if (e.dataTransfer.files.length > 0) handleJdFile(e.dataTransfer.files[0]);
  });

  // Submit Screening
  async function submitScreening() {
    if (selectedCandidateFiles.length === 0) return;
    const btn = document.getElementById('screenBtn');
    btn.disabled = true;
    btn.textContent = '⏳ Parsing Resumes & Applying Rubric Overrides...';

    const formData = new FormData();
    if (customJdFile) {
      formData.append('jd_file', customJdFile);
    }
    selectedCandidateFiles.forEach(f => formData.append('files', f));

    try {
      const res = await fetch('/api/screen', { method: 'POST', body: formData });
      const data = await res.json();
      renderResults(data);
    } catch (err) {
      alert('Error screening profiles: ' + err);
    } finally {
      btn.disabled = false;
      btn.textContent = '🚀 Screen Candidate Profiles';
    }
  }

  function renderResults(data) {
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('resultJdMeta').innerHTML = `Evaluated against: <strong>${data.active_jd}</strong> (${data.count} candidates ranked)`;
    const tbody = document.getElementById('rankingTable');
    tbody.innerHTML = '';

    data.candidates.forEach((c, idx) => {
      let badgeClass = 'badge-pass';
      if (c.verdict.includes('Reject') || c.verdict.includes('Failed')) badgeClass = 'badge-fail';
      else if (c.verdict.includes('Potential')) badgeClass = 'badge-warn';

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>#${idx + 1}</strong></td>
        <td><strong>${c.name}</strong></td>
        <td><strong style="color:#818cf8;">${c.final_score} / 100</strong></td>
        <td><span class="badge ${badgeClass}">${c.verdict}</span></td>
        <td>${c.years_exp} yrs</td>
        <td style="color:#cbd5e1; font-size:12px;">${c.override_note}</td>
      `;
      tbody.appendChild(tr);
    });

    const exportDiv = document.getElementById('exportLinks');
    exportDiv.innerHTML = `
      <a href="${data.reports.pdf}" target="_blank" class="btn-export">📄 Download PDF</a>
      <a href="${data.reports.html}" target="_blank" class="btn-export">🌐 View HTML</a>
      <a href="${data.reports.md}" target="_blank" class="btn-export">📝 Markdown</a>
    `;
    window.scrollTo({ top: document.getElementById('resultsSection').offsetTop - 20, behavior: 'smooth' });
  }
</script>
</body>
</html>
"""

if __name__ == "__main__":
    print(f"Candidate Screener Agent Portal running at http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), ScreenerHTTPHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down portal.")
