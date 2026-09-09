"""
AI Candidate Screener — Model Context Protocol (MCP) Server
Enables Claude, Visual Studio Code (Copilot / Cline / Roo-Code / Cursor), and any MCP-compliant client
to evaluate candidate resumes with the 4-tier no-inflation engine, 100-point rubric, and hard-fail overrides.

Usage:
  - Local Stdio (Default for Claude Desktop / VS Code):
      python mcp_server.py
  - Public Remote SSE Server (for hosting on Cloud / URL):
      python mcp_server.py --transport sse --host 0.0.0.0 --port 8000
"""

import sys
import os
import re
import json
import pathlib
import datetime
import argparse
from mcp.server.fastmcp import FastMCP

BASE_DIR = pathlib.Path(__file__).parent.resolve()
REFERENCES_DIR = BASE_DIR / "references"
DEFAULT_JD_PATH = REFERENCES_DIR / "job-description.md"
DEFAULT_RUBRIC_PATH = REFERENCES_DIR / "rubric.md"
REPORTS_DIR = BASE_DIR / "Reports"
RESUMES_DIR = BASE_DIR / "Resumes"
REPORTS_DIR.mkdir(exist_ok=True)
RESUMES_DIR.mkdir(exist_ok=True)

# Initialize FastMCP Server
mcp = FastMCP(
    "CandidateScreener",
    instructions="Autonomous AI ATS screening system with 4-tier deliverable verification and 100-point capacity rubric.",
    dependencies=["pypdf", "python-docx", "fpdf2"]
)

# Standard SDET Taxonomy Weights
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

def evaluate_profile(name: str, text: str, custom_jd_text: str = None) -> dict:
    if custom_jd_text:
        role_title, mandatory_weights, good_weights = parse_custom_jd(custom_jd_text)
    else:
        role_title = "Senior SDET / QA Automation"
        mandatory_weights = DEFAULT_MANDATORY_WEIGHTS
        good_weights = DEFAULT_GOOD_TO_HAVE_WEIGHTS

    exp_years = extract_years_experience(text)
    lower_text = text.lower()

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
                status = "Claimed not evidenced"
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

    # Experience fit calculation
    if 6.0 <= exp_years <= 10.0:
        exp_score = 5.0
    elif 4.0 <= exp_years < 6.0:
        exp_score = 4.0
    elif 0.0 < exp_years < 4.0:
        exp_score = 3.0
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

# ================= MCP TOOLS =================

@mcp.tool()
def screen_candidate(candidate_name: str, resume_text: str, custom_jd_text: str = None) -> dict:
    """
    Screen a single candidate's resume text against the active ground truth Job Description (or custom JD).
    Applies the 4-tier no-inflation engine (Matched 1.0x, Partial 0.6x, Claimed 0.3x, Missing 0.0x),
    evaluates against the 100-point rubric, and returns a detailed gap matrix and override verdict.
    """
    return evaluate_profile(candidate_name, resume_text, custom_jd_text=custom_jd_text)

@mcp.tool()
def screen_batch_resumes(resumes: list[dict], custom_jd_text: str = None) -> dict:
    """
    Batch screen multiple candidate resumes and return ranked leaderboard and summary insights.
    Each item in `resumes` should be a dict with `name` and `text`.
    """
    results = []
    for item in resumes:
        name = item.get("name", "Unnamed Candidate")
        text = item.get("text", "")
        res = evaluate_profile(name, text, custom_jd_text=custom_jd_text)
        results.append(res)

    results.sort(key=lambda x: x["final_score"], reverse=True)
    return {
        "active_jd": results[0]["target_role"] if results else "Standard SDET",
        "total_ranked": len(results),
        "candidates": results
    }

@mcp.tool()
def get_job_description() -> str:
    """
    Retrieve the current active ground-truth Job Description requirements and qualification bar.
    """
    if DEFAULT_JD_PATH.exists():
        return DEFAULT_JD_PATH.read_text(encoding="utf-8", errors="ignore")
    return "Job description file not found."

@mcp.tool()
def get_scoring_rubric() -> str:
    """
    Retrieve the 100-point capacity scoring model, weight allocations, and hard-fail gate rules.
    """
    if DEFAULT_RUBRIC_PATH.exists():
        return DEFAULT_RUBRIC_PATH.read_text(encoding="utf-8", errors="ignore")
    return "Scoring rubric file not found."

# ================= MCP RESOURCES =================

@mcp.resource("screener://job-description")
def job_description_resource() -> str:
    """Active ground-truth Job Description"""
    return get_job_description()

@mcp.resource("screener://rubric")
def rubric_resource() -> str:
    """Active 100-point capacity scoring rubric"""
    return get_rubric_resource()

def get_rubric_resource() -> str:
    return get_scoring_rubric()

# ================= MCP PROMPTS =================

@mcp.prompt()
def screen_candidate_prompt(candidate_name: str, resume_text: str) -> str:
    """Generate an evaluation prompt for an LLM to screen a candidate."""
    return f"""Evaluate candidate '{candidate_name}' against the ground-truth Job Description and Rubric:

Candidate Resume:
{resume_text}

Rules:
1. Compare candidate profile evidence directly against the Job Description (no arbitrary experience cutoff).
2. 4-Tier Verification: Matched (1.0x, concrete deliverable), Partial (0.6x), Claimed (0.3x, bare keyword list), Missing (0.0x).
3. Status Color Standard: Missing (Bold Red), Claimed not evidenced (Bold Blue), Partial Match (Bold Orange), Matched (Bold Green).
4. Hard Gap Rule: If both AI Solution Testing & Agentic AI are missing, cap score < 60.
5. Output all 7 standardized sections: Screened Files, Active JD, Candidates Ranked, Ranking Table, Key Takeaways, Gap Matrix, Candidate Details.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Candidate Screener MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio", help="Transport mode: stdio (default) or sse")
    parser.add_argument("--host", default="0.0.0.0", help="Host address for SSE transport (default: 0.0.0.0)")
    default_port = int(os.environ.get("PORT", 8000))
    parser.add_argument("--port", type=int, default=default_port, help=f"Port for SSE transport (default: {default_port})")
    args = parser.parse_args()

    if args.transport == "sse":
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        if hasattr(mcp.settings, "transport_security") and mcp.settings.transport_security:
            mcp.settings.transport_security.enable_dns_rebinding_protection = False
            mcp.settings.transport_security.allowed_hosts = ["*"]
            mcp.settings.transport_security.allowed_origins = ["*"]
        print(f"🚀 Candidate Screener MCP Server listening on http://{args.host}:{args.port}/sse", file=sys.stderr)
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")
