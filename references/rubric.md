# Scoring Rubric — Candidate Screener

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

| # | Mandatory skill | Weight |
|---|---|---|
| 1 | JavaScript / TypeScript (core automation language) | 6 |
| 2 | Python (core automation language) | 6 |
| 3 | Cypress | 6 |
| 4 | Playwright | 6 |
| 5 | Pytest | 6 |
| 6 | Automation framework design — build, scale, and maintain end-to-end | 8 |
| 7 | UI / Web testing + BDD (Cucumber / SpecFlow, MABL) | 9 |
| 8 | API testing (REST APIs; Postman / Insomnia / Mocha) | 9 |
| 9 | STLC + test strategy — functional & non-functional testing | 7 |
| 10 | Test management tools (Jira, TestRail, ALM) | 6 |
| 11 | Agile / Kanban methodology | 6 |
| 12 | AI-powered solution testing (testing AI solutions) | 6 |
| 13 | Agentic AI (MCP, RAG, Prompting; building & testing solutions) | 4 |

**Note on languages/frameworks:** Candidates are evaluated directly on evidenced skills matching the JD. A candidate is strong if ≥1 core language is evidenced and at least one primary framework is evidenced.

---

## Good-to-have bonus (max 10)

| Skill | Weight |
|---|---|
| AWS / Azure cloud exposure | 2 |
| CI/CD integration (Jenkins, GitHub Actions, GitLab CI) | 3 |
| Monitoring / log analysis — Splunk, Grafana, Power BI | 2 |
| No-code / low-code tools (MABL, Test Complete) | 1 |
| Pharma / domain industry experience | 2 |

---

## Experience fit (max 5)

*Evaluated based on overall seniority alignment without hard-failing or disqualifying candidates with fewer years.*

| Total Years of Experience | Points | Seniority Evaluation |
|---|---|---|
| < 4 years | 3 | Developing / Early-career (evaluated purely on skill deliverables) |
| 4–6 years | 4 | Mid-Senior track |
| 6–10 years | 5 | Target sweet spot |
| 11–12 years | 3 | Upper seniority |
| > 12 years | 2 | Extensive leadership / architect track |

---

## Verdict mapping
| Score | Verdict | Screening Result |
|---|---|---|
| ≥ 80 | **Strong fit** | **Screening Passed** |
| 60–79 | **Potential fit** | **Screening Passed** (probes recommended) |
| 40–59 | **Weak fit** | **Screening Failed** |
| < 40 | **Reject** | **Screening Failed** |

---

## Content Overrides & Flags (Content-Driven)
1. **No evidenced core language:** Neither JavaScript/TypeScript nor Python is evidenced in project deliverables $\rightarrow$ **Weak Fit / Reject**.
2. **No test-automation framework evidence:** None of the required automation frameworks appear in deliverables $\rightarrow$ **Reject**.
3. **AI-driven testing entirely missing (Rule #3):** Both AI Solution Testing (#12) and Agentic AI (#13) are Missing or Claimed $\rightarrow$ Cap score at $< 60$ and downgrade verdict tier.
4. **Critical mandatory single-component Missing:** UI + API automation both missing $\rightarrow$ Cap score at 50.
5. **Skills padding:** If a candidate lists $\ge 2$ mandatory skills only in summary/keywords without deliverable evidence, flag them under Claimed (0.30×) and recommend targeted interview probing.