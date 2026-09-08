---
title: Candidate Screener MCP Server
emoji: 🎯
colorFrom: indigo
colorTo: cyan
sdk: docker
app_port: 7860
pinned: false
---

# 🤖 Candidate Screener AI Agent & MCP Server

> **An autonomous, evidence-driven AI screening agent for technical engineering recruitment (SDET, QA, Full-Stack, & AI Engineers).**  
> Eliminates resume keyword padding through strict deliverable verification, mathematical 100-point capacity scoring, and automated audit-ready PDF/HTML reporting.

---

## 🚀 Quickstart for Team Members

### Method 1: Using the Standalone Web Portal (Zero-Code UI)
1. Double-click [`run_screener_portal.bat`](file:///c:/Users/suren/.claude/skills/candidate-screener/run_screener_portal.bat) (or run `python app.py`).
2. Browser opens at **`http://localhost:8080`**.
3. **Target Job Description (Optional):**
   - Upload a custom JD file (`.pdf`, `.docx`, `.txt`, `.md`).
   - If omitted, the portal automatically uses the default SDET Job Description (`references/job-description.md`).
4. **Candidate Profiles (Required):**
   - Drag & drop candidate resumes (`.pdf`, `.docx`, `.txt`).
   - Click **"🚀 Screen Candidate Profiles"**.
5. **Instant Results:**
   - Real-time Leaderboard with Scores and Overrides.
   - 1-Click download buttons for **PDF**, **HTML**, and **Markdown** reports containing all 7 core sections.

### Method 2: Using in Chat / IDE (Antigravity, Claude Code, Gemini CLI, Cursor)
Simply open this workspace and ask the AI agent naturally in the chat window:
- *"Screen the attached candidate resumes."* (uses default SDET JD)
- *"Screen this candidate against this attached custom JD."* (uses custom JD)

The workspace is pre-configured with [`AGENTS.md`](file:///c:/Users/suren/.claude/skills/candidate-screener/AGENTS.md) and [`.agents/skills/candidate-screener/SKILL.md`](file:///c:/Users/suren/.claude/skills/candidate-screener/.agents/skills/candidate-screener/SKILL.md). The agent automatically:
1. Ingests and organizes resumes into `Resumes/<YYYY-MM-DD_HH-MM-SS>/`.
2. Reads multi-format documents (PDF, DOCX, DOC, TXT, OCR).
3. Evaluates evidence against [`references/job-description.md`](file:///c:/Users/suren/.claude/skills/candidate-screener/references/job-description.md) and [`references/rubric.md`](file:///c:/Users/suren/.claude/skills/candidate-screener/references/rubric.md).
4. Generates audit-ready Markdown, HTML, and PDF reports directly inside `Reports/<YYYY-MM-DD_HH-MM-SS>/`, including all 7 mandatory sections:
   - **Screened Files:** Listed input files
   - **Active JD:** Ground truth JD used
   - **Candidates Ranked:** Total candidate count
   - **1) Ranking Table:** Sorted candidates with Score, Verdict, Total Exp, Missing Mandatory, Partial, Claimed
   - **Key Takeaway & Override Decisions:** Callout box detailing individual overrides and fit
   - **2) Gap Matrix:** Candidate heading banners with `Skill / Area | JD Expectation | Requirement | Status | Evidence`
   - **3) Candidate Details:** Deep arithmetic score breakdown and status factor audit

---

## 📁 Repository Architecture

```
candidate-screener/
│
├── AGENTS.md                                             # Workspace Agent Instructions & System Prompt
├── GEMINI.md                                             # Cross-Platform Instructions
├── SKILL.md                                              # Agent Skill Definition & Workflow
│
├── references/                                           # Ground Truth Reference Data
│   ├── job-description.md                                # Active Technical Job Description
│   └── rubric.md                                         # 100-Point Mathematical Rubric & Overrides
│
├── Resumes/                                              # Dedicated Candidate Resumes Root
│   └── <YYYY-MM-DD_HH-MM-SS>/                            # Timestamped upload folder per batch
│
├── Reports/                                              # Dedicated Screening Reports Root
│   └── <YYYY-MM-DD_HH-MM-SS>/                            # Generated Markdown, HTML, and PDF reports
│
├── presentation_deck.html                                # Interactive 9-Slide Presentation Deck
├── presentation_deck.pdf                                 # Exported 16:9 Landscape Slide Deck PDF
├── CANDIDATE_SCREENER_PROJECT_GUIDE.md                   # Comprehensive Architecture & Playbook Guide
└── Candidate_Screener_Agent_Architecture_and_Tech_Stack.docx # Formatted Word Document Guide
```

---

## ⚖️ How the Screener Evaluates Resumes

### 1. The 4-Tier "No-Skill-Inflation" Engine
- **Matched (`M`, 1.00× weight):** Demonstrable evidence in $\ge 1$ project deliverable or quantifiable outcome.
- **Partial Match (`P`, 0.60× weight):** Adjacent technology or passing mention without direct framework ownership.
- **Claimed (`C`, 0.30× weight):** Listed only in a summary/skills list without project evidence. Automatically flagged for interview probe.
- **Missing (`(U)`, 0.00× weight):** Not present in the resume.

### 2. 100-Point Capacity Model & Hard Gates
- **Mandatory Skills (85 Pts):** Core languages, frameworks (Playwright, Cypress, Pytest), API testing, BDD, STLC, AI Testing, and Agentic AI.
- **Good-to-Have Bonus (10 Pts):** Cloud (AWS/Azure), CI/CD pipelines, Healthcare/Pharma domain, and monitoring tools.
- **Experience Fit (5 Pts):** 6–10 Yrs (5 pts), 11–12 Yrs (3 pts), >12 Yrs (2 pts), < 6 Yrs (0 pts / Gate Fail).

### 3. Hard-Fail Overrides
1. **Experience Gate (< 6.0 Yrs):** Immediate Disqualification & Screening Failed prior to scoring.
2. **Core Language Gate:** Neither JS/TS nor Python evidenced $\rightarrow$ Hard Fail.
3. **Rule #3 AI Gap:** AI Solution Testing & Agentic AI missing $\rightarrow$ Score capped at $< 60$ and verdict downgraded.

---

## 🛠️ How to Customize for Other Roles

To screen candidates for a different engineering role (e.g. Frontend Architect, Backend Python, DevOps):
1. **Update the Job Description:** Edit [`references/job-description.md`](file:///c:/Users/suren/.claude/skills/candidate-screener/references/job-description.md) with your target skills and must-haves.
2. **Update the Scoring Rubric:** Adjust weights in [`references/rubric.md`](file:///c:/Users/suren/.claude/skills/candidate-screener/references/rubric.md).
3. Drop resumes into the chat or `Resumes/` folder and start screening!

---

*Authored by **Surendra Bharadwaj** · Candidate Screener AI Agent*
