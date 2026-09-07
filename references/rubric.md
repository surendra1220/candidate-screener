# Scoring Rubric — SDET Screener

## Capacity
**Total = MandatorySkills (max 85) + GoodToHaveBonus (max 10) + ExperienceFit (max 5) = 100**
Per-skill status points (applied same way to mandatory and good-to-have skill):

| Status | Points (× weight) |
|---|---|
| Matched (evidenced) | 1.00 × weight |
| Partial match | 0.60 × weight |
| Claimed but unevidenced | 0.30 × weight |
| Missing | 0 |

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

**Note on languages/frameworks:** the JD says "JavaScript **or** Python" and "Cypress/Playwright/Pytest **or equivalent**" — a candidate is strong if ≥1 core language is evidenced and at least one of the three frameworks is evidenced. A second language/framework is a bonus, not a double requirement. Still, score each individual skill honestly via its own weight+status.

## Good-to-have bonus (max 10)

| Skill | Weight |
|---|---|
| AWS / Azure cloud exposure | 2 |
| CI/CD integration (Jenkins, GitHub Actions, GitLab CI) | 3 |
| Monitoring / log analysis — Splunk, Grafana, Power BI | 2 |
| No-code / low-code tools (MABL, Test Complete) | 1 |
| Pharma / domain industry experience | 2 |

## Experience fit (max 5)

| Years (total experience per resume) | Points | Note |
|---|---|---|
| < 6 | **HARD FAIL → Screening Failed** | Under-senior for a 6–10 yr role; applied before scoring |
| 6–10 | 5 | Sweet spot |
| 11–12 | 3 | Upper edge — passes on experience |
| > 12 | 2 | Over-qualified flag — still passes on experience |

## Verdict mapping
| Score | Verdict | Screening result |
|---|---|---|
| ≥ 80 | **Strong fit** | **Screening Passed** |
| 60–79 | **Potential fit** | **Screening Passed** (conditional) |
| 40–59 | **Weak fit** | **Screening Failed** |
| < 40 | **Reject** | **Screening Failed** |

Any hard-fail / override rule (below) forces **Screening Failed** regardless of score.

## Hard-fail / override rules (apply FIRST; these can down-rank a Pass score, or flag even a high score)
1. **No evidenced core language** — neither JavaScript/TypeScript nor Python is evidenced anywhere → hard-fail → **Reject**, regardless of score.
2. **No test-automation framework evidence at all** — none of Cypress/Playwright/Pytest appears in any project/role → **Reject**.
3. **AI-driven testing entirely missing** (both #12 and #13 = Missing or Claimed-unevidenced) → cap < 60 AND downgrade one verdict tier (Strong→Potential, Potential→Weak). AI / Agentic is a headline & Must-Have of this role.
4. **Critical mandatory single-component Missing**: UI+API automation both missing → cap at 50.
5. **Years of experience < 6** (total per resume) → **hard fail → Screening Failed**, applied BEFORE scoring; no score can override. Mention "under-senior for 6–10 yr SDET role".
6. **Skills padding** — if a candidate lists ≥ 2 major mandatory skills only as claims (no project support), add 1 red flag each; these go in the "claimed but unevidenced" column and drop the verdict one tier if Claimed-count ≥ 3 mandatory skills.

Engine-fit of these rules on each candidate must be shown in section 3 under "Red flags & interview-killers."