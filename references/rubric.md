# Scoring Rubric — Candidate Screener (SDET 3–12 Yrs)

## Capacity
**Total = MandatorySkills (max 85) + GoodToHaveBonus (max 10) + ExperienceFit (max 5) = 100**

Per-skill status points (applied same way to mandatory and good-to-have skills):

| Status | Weight Factor | Color Standard (UI / Reports) |
|---|---|---|
| **Matched** (evidenced in deliverables) | **1.00 × weight** | **Bold Green** (`#16a34a` / `rgb(22, 163, 74)`) |
| **Partial match** (adjacent / minimal use) | **0.60 × weight** | **Bold Orange** (`#ea580c` / `rgb(234, 88, 12)`) |
| **Claimed but unevidenced** (keyword list only) | **0.30 × weight** | **Bold Blue** (`#2563eb` / `rgb(37, 99, 235)`) |
| **Missing** (not evidenced) | **0.00 × weight** | **Bold Red** (`#dc2626` / `rgb(220, 38, 38)`) |

---

## Mandatory skills & weights (sums to 85)

| # | Mandatory skill | Weight | JD Expectation |
|---|---|---|---|
| 1 | **Life Sciences / Pharma Domain Experience** | 9 | Working experience in Life Sciences, Pharma, Clinical, Regulatory, or Foundry in projects (Healthcare domain bonus). |
| 2 | **JavaScript / TypeScript (Core Language)** | 6 | Proficient in JS/TS for building automation solutions (proficient in either JS/TS or Python counts as Matched). |
| 3 | **Python (Core Language)** | 6 | Proficient in Python for building automation solutions (proficient in either JS/TS or Python counts as Matched). |
| 4 | **Playwright / Modern Framework** | 7 | Hands-on experience with Playwright modern test automation framework. |
| 5 | **Cypress / Pytest / Selenium Frameworks** | 6 | Experience with Cypress, Pytest, Selenium or equivalent modern automation tools. |
| 6 | **Automation Framework Design** | 8 | Ability to build, scale, and maintain automation frameworks end-to-end (Page Object Model / Modular). |
| 7 | **UI / Web Testing + BDD** | 8 | UI/Web testing with BDD frameworks like Cucumber, SpecFlow, or equivalent. |
| 8 | **API Testing** | 8 | REST APIs along with Playwright API, RestAssured, Postman, Insomnia, or Mocha. |
| 9 | **STLC & Testing Strategies** | 6 | Well-versed with all STLC phases, test strategy/planning, functional and non-functional tests. |
| 10 | **Test Management Tools** | 5 | Hands-on working knowledge of Jira, HP ALM / QC, TestRail. |
| 11 | **Project Methodology (Agile / Kanban)** | 5 | Working knowledge of Agile Scrum ceremonies, sprint planning, Kanban defect triage. |
| 12 | **AI Solutions & AI Testing** | 6 | Creating AI solutions to reduce manual effort & testing AI-powered solutions (Playwright agents / MCPs). |
| 13 | **Agentic AI (MCP, RAG, Prompting)** | 5 | Experience or knowledge with Agentic solutions (MCP, RAG, Prompting), testing & developing solutions. |

---

## Good-to-have bonus (max 10)

| Skill | Weight | JD Expectation |
|---|---|---|
| **AWS / Azure Cloud Exposure** | 2 | Cloud services relevant to test environments. |
| **CI/CD Integration** | 3 | Integrates test suites into CI/CD pipelines (Jenkins, GitHub Actions, GitLab CI). |
| **Distributed Debugging & Log Analysis** | 2 | Power BI, Splunk, Grafana or monitoring/reporting tools. |
| **Root Cause Analysis** | 2 | Multi-system diagnostics, tracing failures across services, logs, and data layers. |
| **No-Code / Low-Code Tools** | 1 | Knowledge of MABL, Test Complete, etc. |

---

## Experience fit (max 5)

*Evaluated based on 3–12 years target experience range without automatic rejection or cutoffs for less years.*

| Total Years of Experience | Points | Evaluation |
|---|---|---|
| 3.0 – 12.0 years | 5.0 | Target core experience range |
| > 12.0 years | 4.0 | Senior / Lead track |
| 1.0 – 2.9 years | 3.0 | Early career (evaluated purely on skill deliverables) |
| < 1.0 year | 2.0 | Entry level |

---

## Verdict mapping
| Score | Verdict | Screening Result |
|---|---|---|
| ≥ 80 | **Strong fit** | **Screening Passed** |
| 60–79 | **Potential fit** | **Screening Passed** (interview probes recommended) |
| 40–59 | **Weak fit** | **Screening Failed** |
| < 40 | **Reject** | **Screening Failed** |

---

## Content Overrides & Flags
1. **Core Language Gate:** If neither JavaScript/TypeScript nor Python is evidenced in project deliverables $\rightarrow$ **Weak Fit / Reject**.
2. **AI Hard Gap (Rule #3):** If both AI Solutions/Testing (#12) and Agentic AI (#13) are Missing $\rightarrow$ Cap score at $< 60$ and downgrade verdict tier.
3. **Domain Alignment Probe:** If Life Sciences / Pharma Domain is Missing, note as major candidate gap for role domain alignment.