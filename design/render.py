"""Render PestLand mockups and diagrams to PNG.

    python design/render.py            # all
Requires: pip install playwright ; a Chromium (set PLAYWRIGHT_CHROMIUM or use the default).
"""
import glob
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import screens as S  # noqa: E402
import diagrams as D  # noqa: E402

OUT = HERE.parent / "docs" / "images"


def page_html(body, width=None):
    w = f"width:{width}px;" if width else ""
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"></head>'
            f'<body><div class="stage" id="shot" style="{w}">{body}</div></body></html>')


def shoot(pg, html, out, selector="#shot"):
    tmp = HERE / "_tmp.html"
    tmp.write_text(html, encoding="utf-8")
    pg.goto(tmp.as_uri())
    pg.wait_for_timeout(150)
    pg.locator(selector).screenshot(path=str(out))
    print("wrote", out.relative_to(HERE.parent))


def main():
    exe = os.environ.get("PLAYWRIGHT_CHROMIUM") or (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page(viewport={"width": 2400, "height": 1200}, device_scale_factor=2)

        (OUT / "screens").mkdir(parents=True, exist_ok=True)
        for name, fn in S.SCREENS.items():
            shoot(pg, page_html(S.phone(fn())), OUT / "screens" / f"{name}.png")

        # same Click 1 screen under five region packs
        caps = {"hawaii": "Island › County › District", "guam": "Village (19 municipalities)", "australia": "State › LGA › biosecurity zone",
                "png": "Province › District › LLG › Ward", "kenya": "County › Sub-county › Ward (CropProtect origin)"}
        body = "".join(f'<div>{S.phone(S.s_click1(k))}<div class="cap-block"><h3>{S.REGIONS[k]["name"]}</h3><p>{c}</p></div></div>' for k, c in caps.items())
        shoot(pg, page_html(body, 2200), OUT / "screens" / "region_switch_click1.png")

        # the 5 + 2 journey on one sheet
        steps = [("Click 1 · Where", S.s_click1), ("Click 2 · Host plant", S.s_click2), ("Click 3 · Identify", S.s_click3),
                 ("Click 4 · Level & photos", S.s_click4), ("Click 5 · Act & send", S.s_click5), ("Click 6 · Risk map", S.s_click6),
                 ("Click 7 · AI Lab", S.s_click7)]
        body = "".join(f'<div>{S.phone(fn())}<div class="cap-block"><h3>{t}</h3></div></div>' for t, fn in steps)
        shoot(pg, page_html(body, 3200), OUT / "screens" / "journey_5_plus_2.png")

        (OUT / "diagrams").mkdir(parents=True, exist_ok=True)
        for name, (fn, width) in D.DIAGRAMS.items():
            shoot(pg, page_html(fn(), width), OUT / "diagrams" / f"{name}.png")
        b.close()
    (HERE / "_tmp.html").unlink(missing_ok=True)


if __name__ == "__main__":
    main()
