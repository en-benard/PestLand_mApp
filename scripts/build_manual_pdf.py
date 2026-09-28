"""Build docs/PestLand_User_Manual.pdf from the Markdown manual (Chromium print)."""
import glob
import os
import pathlib

import markdown
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
FONTS = (ROOT / "design" / "fonts").as_uri()

md = (DOCS / "PestLand_User_Manual.md").read_text(encoding="utf-8")
body = markdown.markdown(md, extensions=["tables", "toc", "sane_lists"])

css = f"""
@font-face {{ font-family: Inter; font-weight: 400; src: url({FONTS}/inter-latin-400-normal.woff2); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url({FONTS}/inter-latin-600-normal.woff2); }}
@font-face {{ font-family: Inter; font-weight: 800; src: url({FONTS}/inter-latin-800-normal.woff2); }}
@page {{ size: A4; margin: 16mm 14mm 18mm; }}
body {{ font-family: Inter, 'DejaVu Sans', sans-serif; font-size: 10.5pt; line-height: 1.5; color: #10201a; }}
h1 {{ font-size: 28pt; color: #0b3b2e; margin: 0 0 4pt; }}
h2 {{ font-size: 17pt; color: #0b3b2e; border-bottom: 2px solid #1c9a72; padding-bottom: 3pt; margin-top: 22pt; break-before: page; }}
h2:first-of-type {{ break-before: avoid; }}
h3 {{ font-size: 12.5pt; color: #11624a; margin-top: 14pt; }}
img {{ max-width: 100%; max-height: 190mm; display: block; margin: 8pt auto; break-inside: avoid; }}
img[src*="screens/0"] {{ max-height: 112mm; }}
h3 {{ break-after: avoid; }}
table {{ border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9pt; break-inside: auto; }}
th {{ background: #dff3ea; text-align: left; }}
th, td {{ border: 1px solid #d5ded9; padding: 4pt 6pt; vertical-align: top; }}
tr {{ break-inside: avoid; }}
blockquote {{ background: #f0faf5; border-left: 4px solid #1c9a72; margin: 8pt 0; padding: 6pt 10pt; }}
code {{ background: #eef1ef; padding: 0 3pt; border-radius: 3px; }}
hr {{ border: none; }}
a {{ color: #11624a; text-decoration: none; }}
"""
html = f'<!doctype html><html><head><meta charset="utf-8"><base href="{DOCS.as_uri()}/"><style>{css}</style></head><body>{body}</body></html>'
tmp = DOCS / "_manual.html"
tmp.write_text(html, encoding="utf-8")

exe = os.environ.get("PLAYWRIGHT_CHROMIUM") or (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = b.new_page()
    pg.goto(tmp.as_uri())
    pg.wait_for_load_state("networkidle")
    pg.pdf(path=str(DOCS / "PestLand_User_Manual.pdf"), format="A4", print_background=True,
           display_header_footer=True, header_template="<span></span>",
           footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#85928c">PestLand User Manual · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
           margin={"top": "16mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
    b.close()
tmp.unlink()
print("wrote docs/PestLand_User_Manual.pdf")
