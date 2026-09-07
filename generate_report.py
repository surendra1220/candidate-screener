import pathlib, subprocess

md_content = """# Screening Report — SDET — 05 Sep 2026
screened: Naukri_Tarunkumarkillamsetty[9y_6m].pdf · JD: references/job-description.md (SDET 6–10 Yrs) · ranked: 1

---

## 1) Ranking

| # | Candidate | Score | Verdict | Years of Exp | Missing (Mandatory) | Partial (any) | Claimed but unevidenced |
|---|---|---|---|---|---|---|---|
| 1 | **Tarun Killamsetty** | **59.0 / 100** *(Capped from 67.0)* | **Screening Failed · Weak fit (AI Hard Gap)** ❌ | 9.5+ yrs | Python, Cypress, Pytest, AI Solution Testing, Agentic AI | — | — |

> **Note on Ranking & Overrides:**
> - **Tarun Killamsetty** passes the experience gate (9.5+ yrs), demonstrates strong Playwright + JS/TS automation and extensive API test automation in Oracle CTMS (Clinical Trial Management Systems / Pharma domain).
> - However, the candidate has a **total absence of AI-driven and Agentic testing** (Rubric Rule #3 forces score cap < 60 and downgrade to Weak fit / Screening Failed).

---

## 2) Gap Matrix

### Candidate: Tarun Killamsetty

| Skill / Area | JD Expectation | Requirement | Status | Evidence (Key Line / Deliverable) |
|---|---|---|---|---|
| **JavaScript / TypeScript** | Proficient in JS/TS for building automation | Mandatory | **Matched** | Built UI automation using Playwright; JavaScript listed in core skills *(Oracle)* |
| **Python** | Proficient in Python for building automation | Mandatory | **Missing** | *no evidence found* |
| **Cypress** | Hands-on modern E2E automation tool | Mandatory | **Missing** | *no evidence found* |
| **Playwright** | Hands-on Playwright modern framework experience | Mandatory | **Matched** | Worked with Playwright locators, assertions, page objects, CI execution *(Oracle)* |
| **Pytest** | Hands-on Pytest test runner & fixtures | Mandatory | **Missing** | *no evidence found* |
| **Framework Design (E2E)** | Build, scale, and maintain POM frameworks end-to-end | Mandatory | **Matched** | Designed and maintained reusable Page Object Model (POM) components *(Oracle)* |
| **UI / Web Testing + BDD** | UI/Web testing with BDD (Cucumber / SpecFlow / MABL) | Mandatory | **Matched** | Automated end-to-end payroll workflows using Selenium with Cucumber *(Paychex)* |
| **API Testing (REST / Postman)** | REST APIs with Postman / Insomnia / Mocha | Mandatory | **Matched** | Performed API Automation using Rest Assured, Postman & SOAP UI *(Oracle)* |
| **STLC & Test Strategy** | Functional & non-functional testing strategy, RTM, metrics | Mandatory | **Matched** | Review requirements, finalize test strategies, build regression suites, Jira logging |
| **Test Management (Jira/ALM)** | Hands-on Jira, HP ALM / QC, TestRail | Mandatory | **Matched** | Reported defects with detailed logs in Jira; HP ALM, TFS listed in skills |
| **Agile / Kanban** | Agile Scrum ceremonies, sprint planning, defect triage | Mandatory | **Matched** | Participated in sprint planning, Agile ceremonies, and QA mentoring *(Oracle)* |
| **AI Solution Testing** | Experience testing AI-powered solutions / ML models | Mandatory | **Missing** | *no evidence found* |
| **Agentic AI (MCP/RAG/Prompting)** | Agentic AI (MCP, RAG, Prompting; test/dev solutions) | Mandatory | **Missing** | *no evidence found* |
| **AWS / Azure Cloud Exposure** | Cloud services relevant to test environments | Good-to-have | **Missing** | *no evidence found* |
| **CI/CD Integration** | Integrates test suites into CI/CD pipelines | Good-to-have | **Matched** | Integrated automated test suites into CI pipelines *(Oracle)*; Jenkins *(Paychex)* |
| **Monitoring / Distributed Debugging** | Splunk, Grafana, Power BI monitoring | Good-to-have | **Missing** | *no evidence found* |
| **No-Code / Low-Code Tools** | MABL, Test Complete | Good-to-have | **Missing** | *no evidence found* |
| **Pharma / Life Sciences Domain** | Pharma, healthcare, or clinical trial background | Good-to-have | **Matched** | 5+ yrs at Oracle CTMS (eClinical platform for biotech, pharma, and CROs) |

---

## 3) Candidate details

### Candidate — Tarun Killamsetty
**Verdict:** Screening Failed · Weak fit (AI Hard Gap) ❌ *(Capped at 59.0 / 100)*  
**Experience Fit:** 9.5+ years (June 2016 – Present) — **Passed Experience Gate** (6–10 yr band, 5/5 pts)  
**Profile Location:** `Resumes/2026-09-05_21-54-37/Naukri_Tarunkumarkillamsetty[9y_6m].txt`

#### Score Breakdown
- **Mandatory Skills (85 pts max):**
  - JavaScript / TypeScript: 6.0 / 6 (Matched — 1.00×)
  - Python: 0.0 / 6 (Missing)
  - Cypress: 0.0 / 6 (Missing)
  - Playwright: 6.0 / 6 (Matched — 1.00×)
  - Pytest: 0.0 / 6 (Missing)
  - Framework Design: 8.0 / 8 (Matched — 1.00×)
  - UI/Web Testing + BDD: 9.0 / 9 (Matched — 1.00×)
  - API Testing: 9.0 / 9 (Matched — 1.00×)
  - STLC & Test Strategy: 7.0 / 7 (Matched — 1.00×)
  - Test Management Tools: 6.0 / 6 (Matched — 1.00×)
  - Agile / Kanban: 6.0 / 6 (Matched — 1.00×)
  - AI Solution Testing: 0.0 / 6 (Missing)
  - Agentic AI (MCP/RAG): 0.0 / 4 (Missing)
  - *Subtotal Mandatory:* **57.0 / 85.0**
- **Good-to-Have Bonus (10 pts max):**
  - CI/CD Integration: +3.0 / 3 (Matched — 1.00×)
  - Pharma / Life Sciences Domain: +2.0 / 2 (Matched — 1.00×)
  - AWS/Azure Cloud: 0.0 / 2 (Missing)
  - Monitoring (Splunk/Grafana): 0.0 / 2 (Missing)
  - No-Code Tools: 0.0 / 1 (Missing)
  - *Subtotal Bonus:* **5.0 / 10.0**
- **Experience Fit (5 pts max):** **5.0 / 5.0** (9.5+ years)
- **Raw Calculated Score:** **67.0 / 100**
- **Override Applied:** **Rule #3 (AI Hard Gap)** — Candidate has zero evidenced experience in AI testing (#12) and Agentic AI (#13). Score capped at `< 60` (59.0) and verdict downgraded from Potential fit to Weak fit.
- **Final Adjusted Score:** **59.0 / 100**

#### Key Strengths
1. **Strong Modern Web Automation (Playwright + POM):** Hands-on with Playwright locators, assertions, reusable page object components, and CI execution at Oracle.
2. **Robust API Automation:** Comprehensive API testing using Rest Assured, Postman, and SOAP UI.
3. **Deep Pharma / eClinical Domain:** 5+ years building and automating tests for Oracle Clinical Trial Management Systems (CTMS).
4. **Solid BDD & CI/CD Foundations:** Cucumber BDD implementation at Paychex, Jenkins pipeline integration, and Jira defect lifecycle tracking.

#### Critical Gaps & Red Flags
1. **AI & Agentic AI Deficit (Hard Blocker for AI SDET):** No exposure to LLM evaluation, AI model validation, Prompt Engineering, RAG architectures, or Model Context Protocol (MCP).
2. **Missing Python & Pytest Stack:** Experience is strictly focused on Java and JavaScript ecosystems.
3. **No Cloud Infrastructure Mention:** AWS/Azure cloud test environment management is not evidenced.

#### Recommended Interview Questions / Probes (If considered for Traditional SDET)
1. *"Can you explain how you structured your Playwright Page Object Model framework at Oracle, specifically handling parallel execution and fixture management?"*
2. *"How did you validate complex REST API payloads and token-based authentication using Rest Assured vs. Postman?"*
3. *"Have you used AI tools (like Copilot, Claude, Cursor) in your automation workflow, or validated non-deterministic AI outputs in QA?"*
"""

pathlib.Path("candidate_screening_report_2026-09-05.md").write_text(md_content, encoding="utf-8")
print("Written MD report.")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Screening Report — SDET — Tarun Killamsetty</title>
<style>
  @page { size: A4 portrait; margin: 15mm 12mm 15mm 12mm; }
  body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif; color: #1e293b; background: #f8fafc; margin: 0; padding: 20px; line-height: 1.5; font-size: 13px; }
  .container { max-width: 900px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
  h1 { font-size: 22px; color: #0f172a; margin-top: 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
  h2 { font-size: 16px; color: #1e293b; margin-top: 25px; margin-bottom: 12px; border-left: 4px solid #3b82f6; padding-left: 10px; }
  h3 { font-size: 14px; color: #334155; margin-top: 18px; margin-bottom: 8px; }
  h4 { font-size: 13px; color: #475569; margin-top: 14px; margin-bottom: 6px; }
  .meta-bar { background: #f1f5f9; padding: 10px 14px; border-radius: 6px; font-size: 12px; color: #475569; margin-bottom: 20px; }
  table { width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 12px; page-break-inside: auto; }
  tr { page-break-inside: avoid; page-break-after: auto; }
  thead { display: table-header-group; }
  th { background: #0f172a; color: #ffffff; font-weight: 600; text-align: left; padding: 8px 10px; border: 1px solid #cbd5e1; }
  td { padding: 7px 10px; border: 1px solid #cbd5e1; vertical-align: top; }
  tr:nth-child(even) { background: #f8fafc; }
  .badge-pass { background: #dcfce7; color: #15803d; font-weight: 600; padding: 2px 6px; border-radius: 4px; display: inline-block; }
  .badge-fail { background: #fee2e2; color: #b91c1c; font-weight: 600; padding: 2px 6px; border-radius: 4px; display: inline-block; }
  .callout { background: #eff6ff; border-left: 4px solid #3b82f6; padding: 12px 16px; border-radius: 0 6px 6px 0; margin-bottom: 20px; font-size: 12px; }
  ul { margin: 6px 0; padding-left: 20px; }
  li { margin-bottom: 4px; }
</style>
</head>
<body>
<div class="container">
  <h1>Screening Report — SDET — 05 Sep 2026</h1>
  <div class="meta-bar">
    <strong>Screened Profile:</strong> Naukri_Tarunkumarkillamsetty[9y_6m].pdf &nbsp;|&nbsp; 
    <strong>Target Role:</strong> SDET (6–10 Yrs) &nbsp;|&nbsp; 
    <strong>Active JD:</strong> references/job-description.md
  </div>

  <h2>1) Candidate Ranking</h2>
  <table>
    <thead>
      <tr>
        <th>#</th>
        <th>Candidate</th>
        <th>Score</th>
        <th>Verdict</th>
        <th>Experience</th>
        <th>Missing (Mandatory)</th>
        <th>Partial</th>
        <th>Claimed (Unevidenced)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>1</td>
        <td><strong>Tarun Killamsetty</strong></td>
        <td><strong>59.0 / 100</strong><br><small style="color:#64748b;">(Capped from 67.0)</small></td>
        <td><span class="badge-fail">Screening Failed · Weak fit (AI Hard Gap) ❌</span></td>
        <td>9.5+ yrs</td>
        <td>Python, Cypress, Pytest, AI Solution Testing, Agentic AI</td>
        <td>—</td>
        <td>—</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <strong>Executive Screening Summary:</strong><br>
    Tarun Killamsetty demonstrates solid traditional SDET capabilities with 9.5+ years of experience, strong hands-on Playwright UI automation, Page Object Model design, Rest Assured API testing, and 5+ years of Clinical Trial Management Systems (CTMS) pharma domain knowledge at Oracle.<br><br>
    However, due to a <strong>total absence of AI-powered solution testing and Agentic AI (MCP/RAG) experience</strong>, Rubric Rule #3 is triggered, enforcing an automatic score ceiling of &lt; 60 (59.0) and downgrading the verdict to <strong>Screening Failed (Weak fit)</strong> for this AI-focused SDET position.
  </div>

  <h2>2) Gap Matrix</h2>
  <h3>Candidate: Tarun Killamsetty</h3>
  <table>
    <thead>
      <tr>
        <th>Skill / Area</th>
        <th>JD Expectation</th>
        <th>Requirement</th>
        <th>Status</th>
        <th>Evidence (Key Line / Deliverable)</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>JavaScript / TypeScript</strong></td><td>Proficient in JS/TS for building automation</td><td>Mandatory</td><td><span class="badge-pass">Matched</span></td><td>Built UI automation using Playwright; JavaScript listed in core skills <em>(Oracle)</em></td></tr>
      <tr><td><strong>Python</strong></td><td>Proficient in Python for building automation</td><td>Mandatory</td><td><span class="badge-fail">Missing</span></td><td><em>no evidence found</em></td></tr>
      <tr><td><strong>Cypress</strong></td><td>Hands-on modern E2E automation tool</td><td>Mandatory</td><td><span class="badge-fail">Missing</span></td><td><em>no evidence found</em></td></tr>
      <tr><td><strong>Playwright</strong></td><td>Hands-on Playwright modern framework experience</td><td>Mandatory</td><td><span class="badge-pass">Matched</span></td><td>Worked with Playwright locators, assertions, page objects, CI execution <em>(Oracle)</em></td></tr>
      <tr><td><strong>Pytest</strong></td><td>Hands-on Pytest test runner & fixtures</td><td>Mandatory</td><td><span class="badge-fail">Missing</span></td><td><em>no evidence found</em></td></tr>
      <tr><td><strong>Framework Design (E2E)</strong></td><td>Build, scale, and maintain POM frameworks end-to-end</td><td>Mandatory</td><td><span class="badge-pass">Matched</span></td><td>Designed and maintained reusable Page Object Model (POM) components <em>(Oracle)</em></td></tr>
      <tr><td><strong>UI / Web Testing + BDD</strong></td><td>UI/Web testing with BDD (Cucumber / SpecFlow / MABL)</td><td>Mandatory</td><td><span class="badge-pass">Matched</span></td><td>Automated end-to-end payroll workflows using Selenium with Cucumber <em>(Paychex)</em></td></tr>
      <tr><td><strong>API Testing (REST / Postman)</strong></td><td>REST APIs with Postman / Insomnia / Mocha</td><td>Mandatory</td><td><span class="badge-pass">Matched</span></td><td>Performed API Automation using Rest Assured, Postman & SOAP UI <em>(Oracle)</em></td></tr>
      <tr><td><strong>STLC & Test Strategy</strong></td><td>Functional & non-functional testing strategy, RTM, metrics</td><td>Mandatory</td><td><span class="badge-pass">Matched</span></td><td>Review requirements, finalize test strategies, build regression suites, Jira logging</td></tr>
      <tr><td><strong>Test Management (Jira/ALM)</strong></td><td>Hands-on Jira, HP ALM / QC, TestRail</td><td>Mandatory</td><td><span class="badge-pass">Matched</span></td><td>Reported defects with detailed logs in Jira; HP ALM, TFS listed in skills</td></tr>
      <tr><td><strong>Agile / Kanban</strong></td><td>Agile Scrum ceremonies, sprint planning, defect triage</td><td>Mandatory</td><td><span class="badge-pass">Matched</span></td><td>Participated in sprint planning, Agile ceremonies, and QA mentoring <em>(Oracle)</em></td></tr>
      <tr><td><strong>AI Solution Testing</strong></td><td>Experience testing AI-powered solutions / ML models</td><td>Mandatory</td><td><span class="badge-fail">Missing</span></td><td><em>no evidence found</em></td></tr>
      <tr><td><strong>Agentic AI (MCP/RAG/Prompting)</strong></td><td>Agentic AI (MCP, RAG, Prompting; test/dev solutions)</td><td>Mandatory</td><td><span class="badge-fail">Missing</span></td><td><em>no evidence found</em></td></tr>
      <tr><td><strong>AWS / Azure Cloud Exposure</strong></td><td>Cloud services relevant to test environments</td><td>Good-to-have</td><td><span class="badge-fail">Missing</span></td><td><em>no evidence found</em></td></tr>
      <tr><td><strong>CI/CD Integration</strong></td><td>Integrates test suites into CI/CD pipelines</td><td>Good-to-have</td><td><span class="badge-pass">Matched</span></td><td>Integrated automated test suites into CI pipelines <em>(Oracle)</em>; Jenkins <em>(Paychex)</em></td></tr>
      <tr><td><strong>Monitoring / Distributed Debugging</strong></td><td>Splunk, Grafana, Power BI monitoring</td><td>Good-to-have</td><td><span class="badge-fail">Missing</span></td><td><em>no evidence found</em></td></tr>
      <tr><td><strong>No-Code / Low-Code Tools</strong></td><td>MABL, Test Complete</td><td>Good-to-have</td><td><span class="badge-fail">Missing</span></td><td><em>no evidence found</em></td></tr>
      <tr><td><strong>Pharma / Life Sciences Domain</strong></td><td>Pharma, healthcare, or clinical trial background</td><td>Good-to-have</td><td><span class="badge-pass">Matched</span></td><td>5+ yrs at Oracle CTMS (eClinical platform for biotech, pharma, and CROs)</td></tr>
    </tbody>
  </table>

  <h2>3) Detailed Candidate Assessment</h2>
  <h3>Candidate: Tarun Killamsetty</h3>
  <p><strong>Verdict:</strong> <span class="badge-fail">Screening Failed · Weak fit (AI Hard Gap) ❌</span> <em>(Final Adjusted Score: 59.0 / 100)</em><br>
  <strong>Experience Gate:</strong> 9.5+ Years — <strong>Passed</strong> (6–10 Yrs Sweet Spot)<br>
  <strong>Ingested Profile:</strong> <code>Resumes/2026-09-05_21-54-37/Naukri_Tarunkumarkillamsetty[9y_6m].txt</code></p>

  <h4>Score Calculation Breakdown</h4>
  <ul>
    <li><strong>Mandatory Skills:</strong> 57.0 / 85.0</li>
    <li><strong>Good-to-Have Bonus:</strong> 5.0 / 10.0 (CI/CD + Pharma Domain)</li>
    <li><strong>Experience Fit:</strong> 5.0 / 5.0 (9.5+ yrs in 6–10 yr range)</li>
    <li><strong>Raw Total:</strong> 67.0 / 100</li>
    <li><strong>Rule #3 Override:</strong> AI Solution Testing (#12) & Agentic AI (#13) Missing &rarr; <strong>Capped @ 59.0 / 100</strong></li>
  </ul>

  <h4>Key Strengths</h4>
  <ul>
    <li><strong>Modern Playwright Automation:</strong> Hands-on experience with Playwright page objects, locators, assertions, and CI execution.</li>
    <li><strong>Comprehensive API Automation:</strong> Proven REST API automation using Rest Assured and Postman at Oracle.</li>
    <li><strong>Pharma / CTMS Domain Expertise:</strong> 5+ years supporting Oracle Clinical Trial Management Systems.</li>
  </ul>

  <h4>Gaps & Interview Probes</h4>
  <ul>
    <li><strong>AI / Agentic Testing Deficit:</strong> Zero exposure to LLM testing, AI agents, MCP, RAG, or prompting.</li>
    <li><strong>Python & Pytest Absence:</strong> Experience is centered entirely around JS/TS and Java.</li>
  </ul>
</div>
</body>
</html>
"""

pathlib.Path("candidate_screening_report_2026-09-05.html").write_text(html_content, encoding="utf-8")
print("Written HTML report.")

# Headless Edge PDF generation
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
html_abs = pathlib.Path("candidate_screening_report_2026-09-05.html").resolve()
pdf_abs = pathlib.Path("candidate_screening_report_2026-09-05.pdf").resolve()

cmd = f'"{edge_path}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{pdf_abs}" "file:///{html_abs}"'
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print("PDF generated:", pdf_abs.exists(), pdf_abs.stat().st_size if pdf_abs.exists() else 0)
