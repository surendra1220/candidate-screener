import pathlib, subprocess, pypdf

html_file = pathlib.Path("presentation_deck.html")
content = html_file.read_text(encoding="utf-8")

old_print_start = "/* Print"
print_idx = content.find(old_print_start)
if print_idx != -1:
    end_style_idx = content.find("</style>", print_idx)
    new_print_css = """/* Print & PDF Export Styles */
  @media print {
    @page {
      size: 11in 6.1875in;
      margin: 0;
    }
    *, *::before, *::after {
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    html, body {
      width: 100% !important;
      height: auto !important;
      min-height: 100% !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: visible !important;
      background: #0f172a !important;
      color: #f8fafc !important;
      display: block !important;
    }
    .deck-nav, .progress-container {
      display: none !important;
    }
    .deck-container {
      display: block !important;
      height: auto !important;
      width: 100% !important;
      position: static !important;
      overflow: visible !important;
    }
    .slide, .slide.active {
      display: flex !important;
      position: relative !important;
      top: 0 !important;
      left: 0 !important;
      opacity: 1 !important;
      transform: none !important;
      width: 11in !important;
      height: 6.1875in !important;
      max-height: 6.1875in !important;
      min-height: 6.1875in !important;
      padding: 35px 50px !important;
      box-sizing: border-box !important;
      page-break-after: always !important;
      break-after: page !important;
      page-break-inside: avoid !important;
      break-inside: avoid !important;
      color: #f8fafc !important;
      background: radial-gradient(circle at 20% 20%, #1e1b4b 0%, #0f172a 60%, #020617 100%) !important;
    }
    .card {
      background: rgba(30, 41, 59, 0.85) !important;
      border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    .slide-table {
      background: rgba(15, 23, 42, 0.85) !important;
    }
    .slide-table th {
      background: rgba(30, 41, 59, 0.95) !important;
      color: #ffffff !important;
    }
    .slide-title {
      background: linear-gradient(135deg, #ffffff 30%, #cbd5e1 100%) !important;
      -webkit-background-clip: text !important;
      -webkit-text-fill-color: transparent !important;
    }
    .hero-title {
      background: linear-gradient(135deg, #ffffff 20%, #93c5fd 60%, #c084fc 100%) !important;
      -webkit-background-clip: text !important;
      -webkit-text-fill-color: transparent !important;
    }
  }
"""
    content = content[:print_idx] + new_print_css + content[end_style_idx:]
    html_file.write_text(content, encoding="utf-8")
    print("Updated presentation_deck.html with 16:9 print styles.")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
html_abs = html_file.resolve()
pdf_abs = pathlib.Path("presentation_deck.pdf").resolve()

cmd = f'"{edge_path}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{pdf_abs}" "file:///{html_abs}"'
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)

reader = pypdf.PdfReader(pdf_abs)
print(f"PDF generated successfully! Total pages: {len(reader.pages)}, Size: {pdf_abs.stat().st_size} bytes")
