import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# Page Margins
for s in doc.sections:
    s.top_margin = Inches(0.8)
    s.bottom_margin = Inches(0.8)
    s.left_margin = Inches(0.8)
    s.right_margin = Inches(0.8)

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_header_banner(doc, title, subtitle):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "0F172A")
    set_cell_margins(cell, top=220, bottom=220, left=250, right=250)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run1 = p.add_run(title + "\n")
    run1.font.name = "Segoe UI"
    run1.font.size = Pt(20)
    run1.font.bold = True
    run1.font.color.rgb = RGBColor(248, 250, 252)
    
    run2 = p.add_run(subtitle)
    run2.font.name = "Segoe UI"
    run2.font.size = Pt(11)
    run2.font.color.rgb = RGBColor(148, 163, 184)

def add_callout(doc, title, text, bg_hex="F1F5F9"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p = cell.paragraphs[0]
    r_title = p.add_run(f"{title}\n")
    r_title.font.name = "Segoe UI"
    r_title.font.bold = True
    r_title.font.size = Pt(11)
    r_title.font.color.rgb = RGBColor(30, 58, 138)
    
    r_text = p.add_run(text)
    r_text.font.name = "Segoe UI"
    r_text.font.size = Pt(10)
    r_text.font.color.rgb = RGBColor(51, 65, 85)

def style_heading_1(p, text):
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = "Segoe UI"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)

def style_heading_2(p, text):
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.name = "Segoe UI"
    r.font.size = Pt(12.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(30, 58, 138)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "1E293B")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    p = cell.paragraphs[0]
    r = p.add_run(code_text)
    r.font.name = "Consolas"
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(241, 245, 249)

# Document Building
add_header_banner(
    doc,
    "AI CANDIDATE SCREENER — TEAM PLAYBOOK",
    "Step-by-Step Guide for Screening Candidate Profiles via Web Portal & Cloudflare MCP Server"
)

doc.add_paragraph()

# 1. Overview
p = doc.add_paragraph()
style_heading_1(p, "1. Executive Summary & Purpose")

p_intro = doc.add_paragraph()
p_intro.paragraph_format.space_after = Pt(8)
r = p_intro.add_run(
    "The AI Candidate Screener is an evidence-driven ATS evaluation system designed to eliminate resume keyword inflation. "
    "It evaluates candidate profiles purely by comparing verified project deliverables against Job Description requirements, computing an objective 100-point capacity score with automatic override rules.\n\n"
    "Our team can access and run the screening system in two flexible ways:"
)
r.font.name = "Segoe UI"
r.font.size = Pt(10.5)

p_ways = doc.add_paragraph()
p_ways.paragraph_format.left_indent = Inches(0.2)
p_ways.paragraph_format.space_after = Pt(4)
r1 = p_ways.add_run("• Pathway 1 — Streamlit Web Portal (Zero Installation): ")
r1.font.bold = True
r1.font.color.rgb = RGBColor(37, 99, 235)
p_ways.add_run("Interactive browser portal for HR, Recruiters, and Hiring Managers to upload resumes, review gap matrices, and export audit-ready PDF/HTML reports.")

p_ways2 = doc.add_paragraph()
p_ways2.paragraph_format.left_indent = Inches(0.2)
p_ways2.paragraph_format.space_after = Pt(12)
r2 = p_ways2.add_run("• Pathway 2 — Cloudflare MCP Server (AI-Native IDEs & Chat): ")
r2.font.bold = True
r2.font.color.rgb = RGBColor(79, 70, 229)
p_ways2.add_run("Public Model Context Protocol (MCP) server that connects directly to Antigravity IDE, VS Code, and Claude Desktop to screen candidates in conversational chat.")

# 2. Pathway 1: Web Portal
p = doc.add_paragraph()
style_heading_1(p, "2. Pathway 1: Screening via Streamlit Web Portal")

add_callout(
    doc,
    "🌐 Live Web Portal URL",
    "https://candidate-screener-agent.streamlit.app/\n(Accessible from any web browser on desktop, tablet, or mobile. No installation required.)",
    bg_hex="EFF6FF"
)

doc.add_paragraph()
p = doc.add_paragraph()
style_heading_2(p, "Step-by-Step Instructions:")

steps = [
    ("Step 1: Open the Portal", "Navigate to https://candidate-screener-agent.streamlit.app/ in Google Chrome, Microsoft Edge, Safari, or Firefox."),
    ("Step 2: Select or Upload Target Job Description (Mandatory)", 
     "In Column 1, choose your JD configuration:\n"
     "• Active Default SDET JD: Uses our pre-calibrated SDET requirements (3-12 yrs, Life Sciences/Pharma must-have, JS/TS or Python, Playwright/Cypress/Pytest, AI & Agentic testing).\n"
     "• Upload Custom JD: Upload a role-specific job description file (.pdf, .docx, .txt, .md). The system dynamically parses mandatory requirements and bonuses."),
    ("Step 3: Upload Candidate Resume Files (Mandatory)", 
     "In Column 2, click 'Browse files' or drag-and-drop one or multiple candidate profiles (.pdf, .docx, .doc, .txt). The portal confirms the total selected file count."),
    ("Step 4: Execute Candidate Screening", 
     "Click the primary button '🚀 Screen Candidate Profiles'. The engine processes multi-format text, compares deliverables against JD skills, enforces rubric weights, and checks override gates."),
    ("Step 5: Review Results & Export Audit Reports", 
     "Review the on-screen results and download standardized reports:\n"
     "1. Ranking Leaderboard: Ranked candidate table with Scores, Verdicts, Experience, and Missing skills.\n"
     "2. Key Takeaways: Executive summary of individual strengths and override decisions.\n"
     "3. 4-Tier Evidence Gap Matrix: Deep per-skill evidence audit with designated bold status colors.\n"
     "4. 1-Click Export Buttons: Download Vector PDF Report, HTML Twin, or Markdown Report.")
]

for s_title, s_desc in steps:
    p_step = doc.add_paragraph()
    p_step.paragraph_format.left_indent = Inches(0.2)
    p_step.paragraph_format.space_after = Pt(6)
    r_st = p_step.add_run(f"✔ {s_title}\n")
    r_st.font.bold = True
    r_st.font.size = Pt(10.5)
    r_st.font.color.rgb = RGBColor(15, 23, 42)
    r_sd = p_step.add_run(s_desc)
    r_sd.font.size = Pt(10)
    r_sd.font.color.rgb = RGBColor(71, 85, 105)

# Gap Matrix Color Standards Table
doc.add_paragraph()
p = doc.add_paragraph()
style_heading_2(p, "Gap Matrix Status Color Standards:")

tbl_colors = doc.add_table(rows=5, cols=3)
tbl_colors.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Status Tier", "Weight Factor", "Criteria & Visual Styling"]
col_widths = [Inches(2.2), Inches(1.3), Inches(3.3)]

for c_idx, h in enumerate(headers):
    cell = tbl_colors.cell(0, c_idx)
    cell.width = col_widths[c_idx]
    set_cell_background(cell, "1E293B")
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    p = cell.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

color_rows = [
    ("Matched (M)", "1.00× weight", "Bold Green (#16A34A) — Evidenced in ≥1 concrete project deliverable.", "DCFCE7", RGBColor(22, 101, 52)),
    ("Partial Match (P)", "0.60× weight", "Bold Orange (#EA580C) — Adjacent tech or minimal exposure.", "FFEDD5", RGBColor(154, 52, 18)),
    ("Claimed not evidenced (C)", "0.30× weight", "Bold Blue (#2563EB) — Listed in summary without project deliverables.", "DBEAFE", RGBColor(30, 64, 175)),
    ("Missing ((U))", "0.00× weight", "Bold Red (#DC2626) — Not found in profile text or synonyms.", "FEE2E2", RGBColor(153, 27, 27))
]

for r_idx, (st_name, st_wt, st_crit, bg_h, fg_rgb) in enumerate(color_rows, start=1):
    c0 = tbl_colors.cell(r_idx, 0)
    c1 = tbl_colors.cell(r_idx, 1)
    c2 = tbl_colors.cell(r_idx, 2)
    for c, w in zip([c0, c1, c2], col_widths):
        c.width = w
        set_cell_margins(c, top=60, bottom=60, left=100, right=100)
    set_cell_background(c0, bg_h)
    
    p0 = c0.paragraphs[0]
    r0 = p0.add_run(st_name)
    r0.font.bold = True
    r0.font.size = Pt(9)
    r0.font.color.rgb = fg_rgb
    
    p1 = c1.paragraphs[0]
    p1.add_run(st_wt).font.size = Pt(9)
    
    p2 = c2.paragraphs[0]
    p2.add_run(st_crit).font.size = Pt(9)

# 3. Pathway 2: Cloudflare MCP Server
doc.add_paragraph()
p = doc.add_paragraph()
style_heading_1(p, "3. Pathway 2: Screening via Cloudflare MCP Server")

add_callout(
    doc,
    "⚡ Live Public MCP SSE Endpoint",
    "Endpoint URL: https://obtaining-euro-substantial-unnecessary.trycloudflare.com/sse\n"
    "Public GitHub Repository: https://github.com/surendra1220/candidate-screener-mcp",
    bg_hex="EEF2FF"
)

doc.add_paragraph()
p = doc.add_paragraph()
style_heading_2(p, "How to Configure in Antigravity IDE, VS Code, and Claude Desktop:")

p_ide = doc.add_paragraph()
p_ide.paragraph_format.space_after = Pt(4)
r = p_ide.add_run("A. Google Antigravity IDE Configuration:")
r.font.bold = True
p_ide.add_run("\nAdd the following snippet to your global configuration file: ")
p_ide.add_run("~/.gemini/config/mcp_config.json").font.bold = True
p_ide.add_run(" (or use Additional Options > MCP Servers > Add Server in the IDE UI):")

add_code_block(
    doc,
    '{\n'
    '  "mcpServers": {\n'
    '    "candidate-screener-cloud": {\n'
    '      "serverUrl": "https://obtaining-euro-substantial-unnecessary.trycloudflare.com/sse"\n'
    '    }\n'
    '  }\n'
    '}'
)

doc.add_paragraph()
p_vscode = doc.add_paragraph()
p_vscode.paragraph_format.space_after = Pt(4)
r = p_vscode.add_run("B. Visual Studio Code Configuration (Copilot / Cline / Cursor):")
r.font.bold = True
p_vscode.add_run("\nAdd to your workspace file: ")
p_vscode.add_run(".vscode/mcp.json").font.bold = True
p_vscode.add_run(":")

add_code_block(
    doc,
    '{\n'
    '  "mcpServers": {\n'
    '    "candidate-screener-cloud": {\n'
    '      "serverUrl": "https://obtaining-euro-substantial-unnecessary.trycloudflare.com/sse"\n'
    '    }\n'
    '  }\n'
    '}'
)

doc.add_paragraph()
p_claude = doc.add_paragraph()
p_claude.paragraph_format.space_after = Pt(4)
r = p_claude.add_run("C. Claude Desktop Configuration:")
r.font.bold = True
p_claude.add_run("\nAdd to your claude_desktop_config.json (%APPDATA%\\Claude\\claude_desktop_config.json on Windows):")

add_code_block(
    doc,
    '{\n'
    '  "mcpServers": {\n'
    '    "candidate-screener-cloud": {\n'
    '      "serverUrl": "https://obtaining-euro-substantial-unnecessary.trycloudflare.com/sse"\n'
    '    }\n'
    '  }\n'
    '}'
)

# MCP Tools Catalog
doc.add_paragraph()
p = doc.add_paragraph()
style_heading_2(p, "Available MCP Tools & Catalog:")

tbl_tools = doc.add_table(rows=5, cols=3)
tbl_tools.alignment = WD_TABLE_ALIGNMENT.CENTER
t_col_w = [Inches(2.0), Inches(2.3), Inches(2.5)]
t_headers = ["Tool / Resource Name", "Parameters", "Purpose & Output"]

for c_idx, h in enumerate(t_headers):
    cell = tbl_tools.cell(0, c_idx)
    cell.width = t_col_w[c_idx]
    set_cell_background(cell, "1E293B")
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    p = cell.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

tool_rows = [
    ("screen_candidate", "candidate_name, resume_text, custom_jd_text (optional)", "Screens a single resume text against JD and returns 100-pt score, Gap Matrix, and override verdict."),
    ("screen_batch_resumes", "resumes (list of {name, text}), custom_jd_text (optional)", "Batch screens multiple profiles and produces ranked leaderboard."),
    ("get_job_description", "None", "Retrieves active technical JD requirements."),
    ("get_scoring_rubric", "None", "Retrieves 100-pt capacity rubric & override rules.")
]

for r_idx, (t_name, t_param, t_purp) in enumerate(tool_rows, start=1):
    c0 = tbl_tools.cell(r_idx, 0)
    c1 = tbl_tools.cell(r_idx, 1)
    c2 = tbl_tools.cell(r_idx, 2)
    for c, w in zip([c0, c1, c2], t_col_w):
        c.width = w
        set_cell_margins(c, top=60, bottom=60, left=100, right=100)
    if r_idx % 2 == 1:
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_background(c2, "F8FAFC")
    
    p0 = c0.paragraphs[0]
    r0 = p0.add_run(t_name)
    r0.font.bold = True
    r0.font.size = Pt(9)
    r0.font.color.rgb = RGBColor(30, 58, 138)
    
    p1 = c1.paragraphs[0]
    p1.add_run(t_param).font.size = Pt(8.5)
    
    p2 = c2.paragraphs[0]
    p2.add_run(t_purp).font.size = Pt(8.5)

# Example Chat Prompts
doc.add_paragraph()
p_prompts = doc.add_paragraph()
style_heading_2(p_prompts, "Example Conversational Prompts for Team Members:")

chat_examples = [
    ("Single Candidate Screening:", '"Using the candidate-screener tool, screen the attached resume for \'Tarun Killamsetty\' against our default SDET job description and show me the 4-tier Gap Matrix and final score."'),
    ("Batch Candidate Screening:", '"Please screen all 4 candidate resumes in my Resumes/ folder against the active SDET JD and generate a comparative leaderboard with override notes."'),
    ("Custom JD Screening:", '"Here is a custom Job Description for a Lead Automation Engineer: [paste JD text]. Evaluate candidate \'Shushil Koppu\' against this custom JD using candidate-screener."')
]

for ex_title, ex_prompt in chat_examples:
    p_ex = doc.add_paragraph()
    p_ex.paragraph_format.left_indent = Inches(0.2)
    p_ex.paragraph_format.space_after = Pt(4)
    r1 = p_ex.add_run(f"💬 {ex_title}\n")
    r1.font.bold = True
    r1.font.size = Pt(10)
    r1.font.color.rgb = RGBColor(30, 58, 138)
    r2 = p_ex.add_run(ex_prompt)
    r2.font.italic = True
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = RGBColor(51, 65, 85)

# 4. Feature Comparison Matrix
doc.add_paragraph()
p = doc.add_paragraph()
style_heading_1(p, "4. Feature Comparison: When to Use Which Pathway")

tbl_comp = doc.add_table(rows=7, cols=3)
tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
comp_widths = [Inches(2.5), Inches(2.1), Inches(2.2)]
comp_headers = ["Feature / Capability", "🌐 Streamlit Web Portal", "⚡ Cloudflare MCP Server"]

for c_idx, h in enumerate(comp_headers):
    cell = tbl_comp.cell(0, c_idx)
    cell.width = comp_widths[c_idx]
    set_cell_background(cell, "0F172A")
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
    p = cell.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

comp_data = [
    ("Target Audience", "Recruiters, HR, Hiring Managers", "Developers, Tech Leads, AI Agents"),
    ("Access Method", "Web browser URL (Zero install)", "Antigravity / VS Code / Claude chat"),
    ("Input Formats", "Upload PDF, DOCX, DOC, TXT", "Text in chat, file attachments, JSON"),
    ("Downloadable PDF/HTML", "1-click instant browser download", "Saved locally to workspace"),
    ("Conversational Q&A", "Static interactive dashboard", "Dynamic chat probes & follow-ups"),
    ("Custom JD Support", "1-click custom file uploader", "Pass custom JD text in prompt")
]

for r_idx, (f_name, w_val, m_val) in enumerate(comp_data, start=1):
    c0 = tbl_comp.cell(r_idx, 0)
    c1 = tbl_comp.cell(r_idx, 1)
    c2 = tbl_comp.cell(r_idx, 2)
    for c, w in zip([c0, c1, c2], comp_widths):
        c.width = w
        set_cell_margins(c, top=60, bottom=60, left=100, right=100)
    if r_idx % 2 == 1:
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_background(c2, "F8FAFC")
    
    c0.paragraphs[0].add_run(f_name).font.bold = True
    c1.paragraphs[0].add_run(w_val)
    c2.paragraphs[0].add_run(m_val)

output_filename = "Candidate_Screening_Guide_Web_and_MCP.docx"
doc.save(output_filename)
print(f"Successfully generated DOCX guide: {output_filename}")
