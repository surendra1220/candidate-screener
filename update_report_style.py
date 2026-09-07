import pathlib
import subprocess

report_0905_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Candidate Screening Report — SDET</title>
<style>
  @page {
    size: A4 portrait;
    margin: 14mm 14mm 14mm 14mm;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    line-height: 1.5;
    font-size: 12px;
    margin: 0;
    padding: 0;
  }
  h1 {
    font-size: 20px;
    color: #0f172a;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 6px;
    margin-top: 0;
    margin-bottom: 4px;
  }
  .subtitle {
    font-size: 11px;
    color: #64748b;
    margin-bottom: 14px;
  }
  h2 {
    font-size: 14.5px;
    color: #1e3a8a;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 16px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }
  h3 {
    font-size: 13px;
    color: #0f172a;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }
  .candidate-heading {
    font-size: 13px;
    font-weight: 700;
    color: #1e1b4b;
    background: #e0e7ff;
    padding: 6px 10px;
    border-left: 4px solid #4f46e5;
    border-radius: 4px;
    margin-top: 14px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 12px;
    font-size: 10.5px;
    page-break-inside: auto;
  }
  tr {
    page-break-inside: avoid;
    page-break-after: auto;
  }
  thead {
    display: table-header-group;
  }
  th, td {
    border: 1px solid #cbd5e1;
    padding: 5px 7px;
    text-align: left;
    vertical-align: top;
  }
  th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
  }
  .badge-pass {
    background-color: #dcfce7;
    color: #166534;
    padding: 2px 5px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 10px;
    display: inline-block;
  }
  .badge-fail {
    background-color: #fee2e2;
    color: #991b1b;
    padding: 2px 5px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 10px;
    display: inline-block;
  }
  .badge-warn {
    background-color: #fef3c7;
    color: #92400e;
    padding: 2px 5px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 10px;
    display: inline-block;
  }
  .status-matched {
    color: #166534;
    font-weight: 600;
  }
  .status-partial {
    color: #b45309;
    font-weight: 600;
  }
  .status-claimed {
    color: #d97706;
    font-weight: 600;
  }
  .status-missing {
    color: #dc2626;
    font-weight: 600;
  }
  .callout-warn {
    background-color: #fffbeb;
    border-left: 4px solid #f59e0b;
    padding: 8px 12px;
    margin-bottom: 12px;
    font-size: 11px;
  }
  ul {
    margin-top: 3px;
    margin-bottom: 6px;
    padding-left: 18px;
  }
  li {
    margin-bottom: 2px;
  }
</style>
</head>
<body>

<h1>Screening Report — SDET — 05 Sep 2026</h1>
<div class="subtitle"><strong>Screened Files:</strong> Naukri_Tarunkumarkillamsetty[9y_6m].pdf &nbsp;|&nbsp; <strong>Active JD:</strong> references/job-description.md (SDET 6–10 Yrs) &nbsp;|&nbsp; <strong>Candidates Ranked:</strong> 1</div>

<h2>1) Ranking</h2>
<table>
  <thead>
    <tr>
      <th style="width: 4%;">#</th>
      <th style="width: 18%;">Candidate</th>
      <th style="width: 12%;">Score</th>
      <th style="width: 22%;">Verdict</th>
      <th style="width: 10%;">Total Exp</th>
      <th style="width: 14%;">Missing (Mandatory)</th>
      <th style="width: 10%;">Partial</th>
      <th style="width: 10%;">Claimed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td><strong>Tarun Killamsetty</strong></td>
      <td><strong>59.0 / 100</strong> <small><em>(Capped from 67)</em></small></td>
      <td><span class="badge-fail">Screening Failed</span> <span class="badge-fail">Weak fit (AI Hard Gap) ❌</span></td>
      <td>9.5+ yrs</td>
      <td>Python, Cypress, Pytest, AI Test, Agentic AI</td>
      <td>—</td>
      <td>—</td>
    </tr>
  </tbody>
</table>

<div class="callout-warn">
  <strong>Key Takeaway &amp; Override Decisions:</strong><br>
  • <strong>Tarun Killamsetty:</strong> Strong traditional Senior QA Automation Engineer with 9.5+ yrs experience, robust Playwright UI automation, Page Object Model design, and Rest Assured API testing across Oracle CTMS Life Sciences.<br>
  • However, triggered <strong>Rubric Rule #3 (AI-driven testing completely missing)</strong> due to zero exposure in AI solution testing (#12) and Agentic AI (#13), capping the score at &lt; 60 (59.0) and downgrading the verdict to Weak fit / Screening Failed.
</div>

<h2>2) Gap Matrix</h2>

<div class="candidate-heading">Candidate: Tarun Killamsetty</div>
<table>
  <thead>
    <tr>
      <th style="width: 20%;">Skill / Area</th>
      <th style="width: 25%;">JD Expectation</th>
      <th style="width: 12%;">Requirement</th>
      <th style="width: 14%;">Status</th>
      <th style="width: 29%;">Evidence (Key Line / Deliverable)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>JavaScript / TypeScript</strong></td>
      <td>Proficient in JS/TS for building automation</td>
      <td>Mandatory</td>
      <td><span class="status-matched">Matched</span></td>
      <td>Built UI automation using Playwright; JavaScript listed in core skills (Oracle)</td>
    </tr>
    <tr>
      <td><strong>Python</strong></td>
      <td>Proficient in Python for building automation</td>
      <td>Mandatory</td>
      <td><span class="status-missing">Missing</span></td>
      <td>no evidence found</td>
    </tr>
    <tr>
      <td><strong>Cypress</strong></td>
      <td>Hands-on modern E2E automation tool</td>
      <td>Mandatory</td>
      <td><span class="status-missing">Missing</span></td>
      <td>no evidence found</td>
    </tr>
    <tr>
      <td><strong>Playwright</strong></td>
      <td>Hands-on Playwright modern framework experience</td>
      <td>Mandatory</td>
      <td><span class="status-matched">Matched</span></td>
      <td>Worked with Playwright locators, assertions, reusable page objects, CI execution (Oracle)</td>
    </tr>
    <tr>
      <td><strong>Pytest</strong></td>
      <td>Hands-on Pytest test runner &amp; fixtures</td>
      <td>Mandatory</td>
      <td><span class="status-missing">Missing</span></td>
      <td>no evidence found</td>
    </tr>
    <tr>
      <td><strong>Framework Design (E2E)</strong></td>
      <td>Build, scale, and maintain POM frameworks end-to-end</td>
      <td>Mandatory</td>
      <td><span class="status-matched">Matched</span></td>
      <td>Designed and maintained reusable Page Object Model (POM) components (Oracle)</td>
    </tr>
    <tr>
      <td><strong>UI / Web Testing + BDD</strong></td>
      <td>UI/Web testing with BDD (Cucumber / SpecFlow / MABL)</td>
      <td>Mandatory</td>
      <td><span class="status-matched">Matched</span></td>
      <td>Automated end-to-end payroll workflows using Selenium with Cucumber (Paychex)</td>
    </tr>
    <tr>
      <td><strong>API Testing (REST / Postman)</strong></td>
      <td>REST APIs with Postman / Insomnia / Mocha</td>
      <td>Mandatory</td>
      <td><span class="status-matched">Matched</span></td>
      <td>Performed API Automation and validation using Rest Assured, Postman &amp; SOAP UI (Oracle)</td>
    </tr>
    <tr>
      <td><strong>STLC &amp; Test Strategy</strong></td>
      <td>Functional &amp; non-functional testing strategy, RTM, metrics</td>
      <td>Mandatory</td>
      <td><span class="status-matched">Matched</span></td>
      <td>Review requirements, finalize test strategies, build regression suites, Jira logging</td>
    </tr>
    <tr>
      <td><strong>Test Management (Jira/ALM)</strong></td>
      <td>Hands-on Jira, HP ALM / QC, TestRail</td>
      <td>Mandatory</td>
      <td><span class="status-matched">Matched</span></td>
      <td>Reported defects with detailed logs in Jira; HP ALM, TFS listed in skills</td>
    </tr>
    <tr>
      <td><strong>Agile / Kanban</strong></td>
      <td>Agile Scrum ceremonies, sprint planning, defect triage</td>
      <td>Mandatory</td>
      <td><span class="status-matched">Matched</span></td>
      <td>Participated in sprint planning, Agile ceremonies, and QA mentoring (Oracle)</td>
    </tr>
    <tr>
      <td><strong>AI Solution Testing</strong></td>
      <td>Experience testing AI-powered solutions / ML models</td>
      <td>Mandatory</td>
      <td><span class="status-missing">Missing</span></td>
      <td>no evidence found</td>
    </tr>
    <tr>
      <td><strong>Agentic AI (MCP/RAG/Prompting)</strong></td>
      <td>Agentic AI (MCP, RAG, Prompting; test/dev solutions)</td>
      <td>Mandatory</td>
      <td><span class="status-missing">Missing</span></td>
      <td>no evidence found</td>
    </tr>
    <tr>
      <td><strong>AWS / Azure Cloud Exposure</strong></td>
      <td>Cloud services relevant to test environments</td>
      <td>Good-to-have</td>
      <td><span class="status-missing">Missing</span></td>
      <td>no evidence found</td>
    </tr>
    <tr>
      <td><strong>CI/CD Integration</strong></td>
      <td>Integrates test suites into CI/CD pipelines</td>
      <td>Good-to-have</td>
      <td><span class="status-matched">Matched</span></td>
      <td>Integrated automated test suites into CI pipelines; Jenkins integration (Paychex)</td>
    </tr>
    <tr>
      <td><strong>Monitoring / Distributed Debugging</strong></td>
      <td>Splunk, Grafana, Power BI monitoring</td>
      <td>Good-to-have</td>
      <td><span class="status-missing">Missing</span></td>
      <td>no evidence found</td>
    </tr>
    <tr>
      <td><strong>No-Code / Low-Code Tools</strong></td>
      <td>MABL, Test Complete</td>
      <td>Good-to-have</td>
      <td><span class="status-missing">Missing</span></td>
      <td>no evidence found</td>
    </tr>
    <tr>
      <td><strong>Pharma / Life Sciences Domain</strong></td>
      <td>Pharma, healthcare, or clinical trial background</td>
      <td>Good-to-have</td>
      <td><span class="status-matched">Matched</span></td>
      <td>5+ yrs on Oracle Clinical Trial Management Systems (CTMS) for pharma &amp; biotech</td>
    </tr>
  </tbody>
</table>

<h2>3) Candidate Details</h2>

<h3>1. Tarun Killamsetty</h3>
<p><strong>Tag Line:</strong> <span class="badge-fail">Screening Failed</span> <span class="badge-fail">Weak fit (AI Hard Gap) ❌</span><br>
<em>Solid Senior Automation Engineer with 9.5+ years in Playwright UI &amp; REST API automation within Oracle CTMS Life Sciences, but lacks any AI testing or Agentic AI experience.</em></p>

<ul>
  <li><strong>Score Breakdown:</strong> Mandatory <strong>57.0 / 85</strong>, Bonus <strong>5.0 / 10</strong>, Experience <strong>5.0 / 5</strong> &rarr; Raw: 67.0 / 100 &rarr; <strong>Capped Score (Rule #3): 59.0 / 100</strong></li>
  <li><strong>Mandatory Skills Breakdown:</strong>
    <ul>
      <li><strong>Matched:</strong> JS/TS (6.0), Playwright (6.0), Framework Design (8.0), UI/Web + BDD (9.0), API Testing (9.0), STLC (7.0), Test Management (6.0), Agile (6.0).</li>
      <li><strong>Missing:</strong> AI Solution Testing (0.0), Agentic AI (0.0), Python (0.0), Cypress (0.0), Pytest (0.0).</li>
    </ul>
  </li>
  <li><strong>Good-to-Have Bonus (5.0 / 10):</strong> CI/CD Integration (3.0), Pharma Domain (2.0) <em>(Oracle CTMS Clinical Trials)</em>.</li>
  <li><strong>Override Rules &amp; Red Flags:</strong> <strong>Triggered Rubric Rule #3</strong> (AI-driven testing completely missing) &rarr; score capped &lt; 60 and downgraded to Weak fit.</li>
  <li><strong>Final Call:</strong> <strong>Screening Failed · Weak fit ❌</strong></li>
</ul>

<h2>4) Recommendation &amp; Next Steps</h2>
<ol>
  <li><strong>Classical SDET Consideration:</strong> Strong candidate for standard Web UI + API Automation roles (Playwright, Rest Assured, Oracle CTMS).</li>
  <li><strong>AI-SDET Position:</strong> Unqualified for AI-focused opening unless provided comprehensive onboarding on LLM evaluation, RAG architecture, and MCP protocols.</li>
</ol>

</body>
</html>
"""

# Write to file locations
p_sub = pathlib.Path("Reports/2026-09-05_22-03-20/candidate_screening_report_2026-09-05.html")
p_sub.write_text(report_0905_html, encoding="utf-8")
p_root = pathlib.Path("candidate_screening_report_2026-09-05.html")
p_root.write_text(report_0905_html, encoding="utf-8")

# Convert to PDF
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for f in [p_sub, p_root]:
    pdf_out = f.with_suffix(".pdf")
    cmd = f'"{edge_path}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{pdf_out.resolve()}" "file:///{f.resolve()}"'
    subprocess.run(cmd, shell=True, capture_output=True)
    print(f"Generated {pdf_out.name}: {pdf_out.stat().st_size} bytes")

print("All reports updated with exact styling!")
