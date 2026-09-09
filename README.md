# 🎯 AI Candidate Screener — Model Context Protocol (MCP) Server

[![MCP Standard](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-8A2BE2.svg)](https://modelcontextprotocol.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastMCP](https://img.shields.io/badge/Framework-FastMCP-green.svg)](https://github.com/jlowin/fastmcp)

An autonomous, evidence-driven **Model Context Protocol (MCP) Server** for technical recruitment and ATS resume screening (default: Senior SDET / QA Automation, extensible to any Job Description).

Connect this MCP server to **Google Antigravity IDE**, **VS Code (GitHub Copilot / Cline / Cursor / Roo-Code)**, or **Claude Desktop** to empower your AI assistant to parse multi-format resumes, eliminate keyword inflation, and generate audit-ready gap matrices.

---

## ✨ Features & Capabilities

- **Strict "No-Skill-Inflation" 4-Tier Verification Engine:**
  - 🟢 **Matched (1.00× weight):** Verified in $\ge 1$ concrete project deliverable.
  - 🟠 **Partial Match (0.60× weight):** Adjacent tech or minimal exposure.
  - 🔵 **Claimed not evidenced (0.30× weight):** Keyword list only, no proof.
  - 🔴 **Missing (0.00× weight):** Not found in resume.
- **100-Point Capacity Rubric:** Evaluates candidates across Mandatory Skills (85 pts), Good-to-Have Bonus (10 pts), and Experience Fit (5 pts).
- **Hard-Fail Rule Overrides:** Automatically catches core language gaps and AI/Agentic testing gaps.
- **Multi-Transport Support:** Runs as a local **`stdio`** server or remote **`sse`** (Server-Sent Events) HTTP service.
- **Cross-Platform Compatibility:** Works on Windows, macOS, Linux, and Cloud (Render, Docker, Cloudflare, Hugging Face).

---

## 🛠️ MCP Tools, Resources & Prompts

### 🧰 Tools
| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `screen_candidate` | `candidate_name`, `resume_text`, `custom_jd_text` *(optional)* | Evaluates a single candidate resume against the active JD. Returns 100-pt score breakdown, Gap Matrix, red flags, and final verdict. |
| `screen_batch_resumes` | `resumes` *(list of {name, text})*, `custom_jd_text` *(optional)* | Batch screens multiple profiles and produces a ranked leaderboard. |
| `get_job_description` | *None* | Retrieves the active ground-truth Job Description requirements. |
| `get_scoring_rubric` | *None* | Retrieves the 100-point capacity scoring model and weight matrix. |

### 📚 Resources
| URI | Description |
| :--- | :--- |
| `screener://job-description` | The active ground-truth Job Description requirements. |
| `screener://rubric` | The active 100-point scoring model and weight allocations. |

### 💬 Prompts
| Prompt Name | Parameters | Description |
| :--- | :--- | :--- |
| `screen_candidate_prompt` | `candidate_name`, `resume_text` | Generates a structured prompt instructing the LLM to screen a candidate using the 4-tier engine. |

---

## 🚀 Quick Setup Guide

### 1. Installation

Clone this repository and install dependencies:
```bash
git clone https://github.com/surendra1220/candidate-screener-mcp.git
cd candidate-screener-mcp
pip install -r requirements.txt
```

---

## 🔌 How to Add to Your AI Tools

### A. Google Antigravity IDE
Add to your Antigravity configuration file (`~/.gemini/config/mcp_config.json`):

```json
{
  "mcpServers": {
    "candidate-screener": {
      "command": "python",
      "args": [
        "/path/to/candidate-screener-mcp/mcp_server.py"
      ]
    }
  }
}
```
*(On Windows, use `py` with args `["-3", "C:\\path\\to\\candidate-screener-mcp\\mcp_server.py"]`)*

Alternatively, in Antigravity IDE:
1. Click **Additional Options (`...`)** in the top right.
2. Select **MCP Servers** $\rightarrow$ **Add Server**.
3. Paste the configuration above.

---

### B. Visual Studio Code (Copilot Agent Mode / Cline / Roo-Code / Cursor)
Add to your project's `.vscode/mcp.json`:

```json
{
  "mcpServers": {
    "candidate-screener": {
      "command": "python",
      "args": [
        "${workspaceFolder}/mcp_server.py"
      ]
    }
  }
}
```

---

### C. Claude Desktop
Add to your Claude Desktop configuration file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "candidate-screener": {
      "command": "python",
      "args": [
        "C:\\path\\to\\candidate-screener-mcp\\mcp_server.py"
      ]
    }
  }
}
```

---

## 🌐 Running as a Public / Remote SSE Server

You can also host the MCP server as a public HTTP SSE endpoint for team use:

### Run Locally / Cloud Server:
```bash
python mcp_server.py --transport sse --host 0.0.0.0 --port 8000
```

### Connect via Remote SSE in any MCP Client:
```json
{
  "mcpServers": {
    "candidate-screener-remote": {
      "serverUrl": "https://your-domain.com/sse"
    }
  }
}
```

---

## 💡 Example Prompts to Ask Your AI Assistant

Once connected, you can interact with the Candidate Screener naturally:

1. **Screen an uploaded candidate:**
   > *"Using candidate-screener, screen the attached resume against our default SDET job description."*

2. **Screen with a custom role:**
   > *"Evaluate this candidate against the custom JD provided in this prompt using the 4-tier no-inflation engine."*

3. **Inspect the active rubric:**
   > *"What are the mandatory skill weights and AI hard-fail override rules in the active rubric?"*

---

## 📦 Project Structure

```
candidate-screener-mcp/
├── mcp_server.py             # Main FastMCP Server (Tools, Resources, Prompts)
├── requirements.txt          # Python dependencies (mcp, pypdf, python-docx, fpdf2)
├── references/
│   ├── job-description.md    # Ground-truth SDET Job Description
│   └── rubric.md             # 100-point capacity scoring model & rules
├── .vscode/
│   └── mcp.json              # VS Code MCP configuration
├── antigravity_mcp_config.json # Antigravity IDE configuration
├── Dockerfile                # Container deployment configuration
└── README.md                 # Public documentation
```

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
