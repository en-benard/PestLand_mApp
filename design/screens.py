"""PestLand screen mockups.

Each function returns the inner HTML of one phone screen. `render.py` wraps them in
design/base.css and screenshots them to docs/images/screens/*.png.
Example content uses the Hawai'i region pack (Kona coffee / coffee berry borer).
"""

# ---------- icons (stroke icons, 24px grid) ----------
IC = {
    "back": '<path d="M15 18l-6-6 6-6"/>',
    "pin": '<path d="M12 21s-7-6.1-7-11a7 7 0 0114 0c0 4.9-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19l7-7"/>',
    "bug": '<rect x="8" y="7" width="8" height="12" rx="4"/><path d="M12 7V5M9 4l1.5 2M15 4l-1.5 2M4 11h4M16 11h4M4 16h4M16 16h4"/>',
    "cam": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "map": '<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "ai": '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
    "cloud": '<path d="M7 18a4 4 0 010-8 6 6 0 0111.3 1.5A3.5 3.5 0 0118 18z"/>',
    "rain": '<path d="M7 14a4 4 0 010-8 6 6 0 0111.3 1.5A3.5 3.5 0 0118 14z"/><path d="M8 17l-1 3M12 17l-1 3M16 17l-1 3"/>',
    "alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.01"/>',
    "home": '<path d="M3 11l9-8 9 8v10H3z"/><path d="M9 21v-6h6v6"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4.5-6 8-6s7 2 8 6"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',
    "gps": '<circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="2.5"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>',
    "send": '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>',
    "download": '<path d="M12 4v11M7 10l5 5 5-5M4 20h16"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>',
    "area": '<path d="M4 7l6-3 10 4-2 11-9 1z"/><circle cx="4" cy="7" r="1.5"/><circle cx="10" cy="4" r="1.5"/><circle cx="20" cy="8" r="1.5"/>',
    "wifi": '<path d="M2 8.5a15 15 0 0120 0M5 12a10 10 0 0114 0M8.5 15.5a5 5 0 017 0M12 19h.01"/>',
    "sync": '<path d="M20 11a8 8 0 00-14.9-3M4 13a8 8 0 0014.9 3"/><path d="M4 4v4h4M20 20v-4h-4"/>',
}


def ic(name, size=20, color=None):
    style = f' style="width:{size}px;height:{size}px;{"color:" + color if color else ""}"'
    return f'<svg class="i" viewBox="0 0 24 24"{style}>{IC[name]}</svg>'


import random as _r
_rnd = _r.Random(7)
TRAP_INSECTS = [(_rnd.uniform(8, 92), _rnd.uniform(8, 92)) for _ in range(15)]  # 14 CBB + 1 other insect

# ---------- illustrations (stand-ins for field photographs) ----------
def art(kind):
    """Small SVG 'photographs' so the mockups need no copyrighted images."""
    bg = {"berry": "#3f6b2f", "egg": "#5a3b22", "larva": "#6b4a2a", "pupa": "#6b4a2a", "adult": "#7a5a32",
          "field": "#6f9a45", "leaf": "#2f5d2a", "trap": "#f3e14a", "damage": "#44652d"}[kind]
    s = f'<svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice" style="width:100%;height:100%;display:block;background:{bg}">'
    if kind == "berry":
        s += ('<circle cx="30" cy="40" r="18" fill="#5e9a3a"/><circle cx="62" cy="55" r="20" fill="#78b04a"/>'
              '<circle cx="45" cy="78" r="15" fill="#4d8a2e"/><circle cx="66" cy="44" r="2.8" fill="#2a1a0c"/>'
              '<circle cx="62" cy="55" r="20" fill="none" stroke="#fff" stroke-opacity=".25"/>')
    elif kind == "egg":
        s += '<ellipse cx="50" cy="50" rx="34" ry="26" fill="#cfa77a"/>' + "".join(
            f'<ellipse cx="{x}" cy="{y}" rx="4" ry="5.5" fill="#fbf6e9" stroke="#d9cdb0"/>'
            for x, y in [(38, 44), (47, 50), (56, 44), (44, 58), (54, 57), (62, 51)])
    elif kind == "larva":
        s += ('<ellipse cx="50" cy="50" rx="36" ry="28" fill="#cfa77a"/>'
              '<path d="M34 58c0-14 10-22 22-20s16 12 10 20" stroke="#fbf3df" stroke-width="11" fill="none" stroke-linecap="round"/>'
              '<circle cx="66" cy="58" r="5" fill="#a0612e"/>')
    elif kind == "pupa":
        s += '<ellipse cx="50" cy="50" rx="36" ry="28" fill="#cfa77a"/><ellipse cx="50" cy="52" rx="10" ry="17" fill="#f1e6cc"/>'
    elif kind == "adult":
        s += ('<ellipse cx="50" cy="50" rx="38" ry="30" fill="#cfa77a"/>'
              '<ellipse cx="52" cy="54" rx="11" ry="17" fill="#241510"/><circle cx="52" cy="35" r="7" fill="#2e1c14"/>'
              '<path d="M42 48l-9-4M42 56l-10 1M42 63l-8 6M62 48l9-4M62 56l10 1M62 63l8 6" stroke="#241510" stroke-width="2"/>'
              '<ellipse cx="48" cy="48" rx="3" ry="7" fill="#fff" opacity=".18"/>')
    elif kind == "field":
        s += ('<rect y="0" width="100" height="38" fill="#a9d4ef"/><path d="M0 40q25-10 50 0t50 0v60H0z" fill="#5f8f3a"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in
                        [(15, 55, 11, "#3f6f2a"), (40, 52, 12, "#8b7a3a"), (65, 56, 11, "#3f6f2a"), (88, 53, 12, "#9a7d3c"),
                         (25, 80, 14, "#476f2c"), (55, 82, 15, "#a38a45"), (85, 84, 14, "#3f6f2a")]))
    elif kind == "leaf":
        s += ('<path d="M50 8C22 30 18 68 50 94C82 68 78 30 50 8z" fill="#6fa84a"/><path d="M50 14v78" stroke="#4d7f30" stroke-width="2"/>'
              '<circle cx="40" cy="34" r="3" fill="#c9b45a"/><circle cx="60" cy="50" r="7" fill="#8a5a2a" stroke="#e0cf6a" stroke-width="2.5"/>'
              '<circle cx="42" cy="68" r="11" fill="#5a3a1a" stroke="#d8c25a" stroke-width="3"/>')
    elif kind == "damage":
        s += ('<ellipse cx="50" cy="52" rx="30" ry="24" fill="#6a4a2a"/><ellipse cx="50" cy="52" rx="24" ry="18" fill="#c9b27f"/>'
              '<path d="M50 36v32" stroke="#8a6a3a" stroke-width="2"/><circle cx="42" cy="48" r="5" fill="#3a2410"/><circle cx="58" cy="58" r="4" fill="#3a2410"/>')
    elif kind == "trap":
        for i, (x, y) in enumerate(TRAP_INSECTS):
            s += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{2.4 if i == 14 else 1.4}" ry="{3.4 if i == 14 else 2.2}" fill="{"#6a3a1a" if i == 14 else "#2a1a10"}" transform="rotate({(i * 37) % 180} {x:.1f} {y:.1f})"/>'
        s += '<path d="M0 25h100M0 50h100M0 75h100M25 0v100M50 0v100M75 0v100" stroke="#b8a92a" stroke-width=".5"/>'
    return s + "</svg>"


def photo(kind, cap, done=True):
    return f'<div class="photo">{art(kind)}<div class="cap">{cap}</div>{"<div class=badge>✓</div>" if done else ""}</div>'


# ---------- chrome ----------
def status(dark=True):
    return f'<div class="notch"></div><div class="status {"dark" if dark else ""}"><span>9:41</span><span>●●● ▮</span></div>'


def appbar(title, sub="", step=None, region="Hawaiʻi"):
    bars = ""
    if step is not None:
        cells = []
        for i in range(1, 8):
            cls = ("an " if i > 5 else "") + ("done" if i < step else "now" if i == step else "")
            cells.append(f'<i class="{cls}"></i>')
            if i == 5:
                cells.append("<b></b>")
        lab = f"Click {step} of 5 · Collect" if step <= 5 else f"Click {step - 5} of 2 · Analyse"
        bars = f'<div class="clicks">{"".join(cells)}</div><div class="clicklabel"><span>{lab}</span><span>Collect ▸ Analyse</span></div>'
    return f'''<div class="appbar"><div class="row">{ic("back", 22)}<div style="flex:1"><h1>{title}</h1>
      {f'<div class="sub">{sub}</div>' if sub else ""}</div><span class="region-pill">{ic("globe", 12)} {region}</span></div>{bars}</div>'''


def footer(text, n=None, style=""):
    dot = f'<span class="tapdot">{n}</span>' if n else ""
    return f'<div class="footer"><div class="btn {style}">{dot}{text}</div></div>'


def phone(inner):
    return f'<div class="phone"><div class="screen">{inner}</div></div>'


# ---------- screens ----------
def s_region():
    packs = [("Hawaiʻi, USA", "State › Island › County › District", "EN · ʻŌlelo Hawaiʻi · Ilocano", "46 MB", True),
             ("Guam", "Territory › Village (19)", "EN · CHamoru", "18 MB", False),
             ("Australia", "State/Territory › LGA › Locality", "EN", "212 MB", False),
             ("Papua New Guinea", "Province › District › LLG › Ward", "EN · Tok Pisin · Hiri Motu", "64 MB", False),
             ("Kenya", "County › Sub-county › Ward", "EN · Kiswahili", "71 MB", False),
             ("USA mainland (50 states)", "State › County (FIPS)", "EN · ES", "per state", False)]
    rows = ""
    for name, adm, lang, size, on in packs:
        rows += f'''<div class="card" style="padding:11px 13px;{'border:2px solid var(--brand-600);background:var(--brand-50)' if on else ''}">
          <div class="row between"><b style="font-size:14.5px">{name}</b><span class="tiny">{size}</span></div>
          <div class="tiny" style="margin-top:3px">{adm}</div><div class="tiny">{lang}</div>
          {'<div class="row" style="margin-top:6px;gap:6px"><span class="tag auto">Detected from GPS</span><span class="tag reg">HDOA rules</span></div>' if on else ''}</div>'''
    return status() + appbar("Choose region pack", "Everything in the app follows this region", None) + f'''
    <div class="body">
      <div class="note info">{ic("gps", 18)}<div>You are at <b>19.62° N, 155.95° W</b>. PestLand matched this to the <b>Hawaiʻi</b> pack. Lists, maps, units, laws, languages and AI model will follow Hawaiʻi.</div></div>
      {rows}
      <div class="row small" style="justify-content:center;gap:6px">{ic("plus", 16)} Import a region pack (.plpack) · Build one in Admin</div>
    </div>''' + footer(f'{ic("download")} Download &amp; use Hawaiʻi pack')


def s_home():
    stat = lambda n, t, c, icn: f'<div class="card" style="padding:11px;background:{c};border:none"><div class="row small">{ic(icn, 16)}{t}</div><div class="big">{n}</div></div>'
    rec = lambda t, s, st, cls: f'''<div class="row" style="padding:9px 0;border-top:1px solid var(--line)"><div style="width:42px;height:42px;border-radius:10px;overflow:hidden">{art(cls)}</div>
       <div style="flex:1"><div style="font-size:13.5px;font-weight:600">{t}</div><div class="tiny">{s}</div></div>{st}</div>'''
    return status() + f'''<div class="appbar"><div class="row"><div style="width:34px;height:34px;border-radius:10px;background:#fff;color:var(--brand-700);display:flex;align-items:center;justify-content:center">{ic("bug", 22)}</div>
      <div style="flex:1"><h1>PestLand</h1><div class="sub">Plant health surveillance</div></div><span class="region-pill">{ic("globe", 12)} Hawaiʻi · v2026.09</span></div></div>
    <div class="body">
      <div class="btn" style="padding:18px;font-size:17px">{ic("plus", 22)} Report new incident <span class="tag" style="background:rgba(255,255,255,.18)">5 clicks</span></div>
      <div class="grid2"><div class="btn ghost" style="font-size:14px;padding:12px">{ic("map", 18)} Risk map</div><div class="btn ghost" style="font-size:14px;padding:12px">{ic("ai", 18)} AI Lab</div></div>
      <div class="grid2">{stat(1, "Drafts", "#fff3d6", "list")}{stat(2, "Ready to send", "#e3effc", "check")}{stat(3, "Pending sync", "#efe9ff", "sync")}{stat(6, "Sent today", "#e6f6e6", "send")}</div>
      <div class="note warn">{ic("alert", 18)}<div><b>Regional alert (sample):</b> watch for coconut rhinoceros beetle damage (V-cuts in palm fronds). Report every sighting — PestLand forwards it to the Hawaiʻi Pest Hotline.</div></div>
      <div class="card" style="padding:4px 14px 6px"><div class="row between" style="padding:8px 0"><b style="font-size:14px">Recent reports</b><span class="tiny">View all</span></div>
        {rec("Coffee berry borer · Coffee", "North Kona · 20 Sep 2026", '<span class="tag auto">Sent</span>', "adult")}
        {rec("Little fire ant · Banana", "Hilo · 19 Sep 2026", '<span class="tag info">Pending</span>', "trap")}
        {rec("Unknown leaf spot · Anthurium", "Puna · 18 Sep 2026", '<span class="tag reg">Needs ID</span>', "damage")}
      </div>
    </div>
    <div class="tabbar"><div class="on">{ic("home")}Home</div><div>{ic("list")}Reports</div><div>{ic("map")}Map</div><div>{ic("ai")}AI Lab</div><div>{ic("user")}Profile</div></div>'''


REGIONS = {
    "hawaii": dict(name="Hawaiʻi", coords="19.6214° N, 155.9489° W", levels=[("State", "Hawaiʻi"), ("Island", "Hawaiʻi Island"), ("County", "Hawaiʻi County"), ("District", "North Kona")],
                   place="Hōlualoa", agency="HDOA Plant Quarantine", units="acres · °F · mm"),
    "guam": dict(name="Guam", coords="13.4745° N, 144.7505° E", levels=[("Territory", "Guam"), ("Village", "Yigo"), ("Region", "Northern"), ("Area", "Upi")],
                 place="Route 3A farms", agency="Guam Dept. of Agriculture", units="acres · °F · mm"),
    "australia": dict(name="Australia", coords="16.9186° S, 145.7781° E", levels=[("State", "Queensland"), ("LGA", "Cairns Regional"), ("Locality", "Gordonvale"), ("Biosecurity zone", "Far North QLD")],
                      place="Mulgrave Rd farm", agency="Exotic Plant Pest Hotline", units="hectares · °C · mm"),
    "png": dict(name="Papua New Guinea", short="PNG", coords="6.0829° S, 145.3869° E", levels=[("Province", "Eastern Highlands"), ("District", "Goroka"), ("LLG", "Goroka Urban"), ("Ward", "Ward 4")],
                place="Kama village", agency="NAQIA", units="hectares · °C · mm"),
    "kenya": dict(name="Kenya", coords="3.6309° S, 39.8499° E", levels=[("County", "Kilifi"), ("Sub-county", "Ganze"), ("Ward", "Ganze"), ("Village", "Bandari")],
                  place="Bandari", agency="County plant-protection office", units="acres · °C · mm"),
}


def s_click1(region="hawaii"):
    r = REGIONS[region]
    rows = "".join(f'<div><div class="tiny" style="margin-bottom:3px">{k}</div><div class="field auto" style="font-size:13px">{v}<span class="ok">✓</span></div></div>' for k, v in r["levels"])
    thumb = ('<svg viewBox="0 0 120 80" style="width:112px;height:76px;border-radius:10px;flex:none;background:#cfe6f5">'
             '<path d="M0 50 Q20 30 45 38 T90 30 T120 40 V80 H0z" fill="#b9d7a3"/><path d="M10 80 Q40 55 70 62 T120 58" stroke="#e8dfc8" stroke-width="3" fill="none"/>'
             '<circle cx="60" cy="42" r="13" fill="#2a78d6" fill-opacity=".18"/><circle cx="60" cy="42" r="4.5" fill="#2a78d6" stroke="#fff" stroke-width="2"/></svg>')
    return status() + appbar("Where & what type", "Location is filled for you", 1, r.get("short", r["name"])) + f'''
    <div class="body">
      <div class="card"><div class="row" style="align-items:flex-start">{thumb}
        <div style="flex:1"><div class="label" style="margin:0">GPS <span class="tag auto">auto</span></div><div style="font-size:14px;font-weight:700">{r["coords"]}</div>
        <div class="row" style="gap:6px;margin-top:6px"><span class="tag" style="background:#e6f6e6;color:#155c15">● ±4 m · Good</span></div>
        <div class="tiny" style="margin-top:5px">Static snapshot, no live map</div></div></div></div>
      <div class="card"><div class="label">Admin areas <span class="tag auto">from offline boundaries</span></div><div class="grid2">{rows}</div>
        <div class="tiny" style="margin:9px 0 3px">Place / farm name (optional)</div><div class="field">{r["place"]}</div>
        <div class="note good" style="margin-top:10px">{ic("check", 16)}<div>GPS point is inside the selected boundaries.</div></div></div>
      <div class="card"><div class="label">What are you reporting? <span class="req">*</span></div>
        <div class="grid2"><div class="chip on" style="justify-content:center">{ic("bug", 15)} Insect / mite</div><div class="chip" style="justify-content:center">{ic("leaf", 15)} Disease</div>
        <div class="chip" style="justify-content:center">🌿 Weed</div><div class="chip" style="justify-content:center">? Not sure</div></div></div>
      <div class="tiny" style="text-align:center">Reports go to: {r["agency"]} · Units: {r["units"]}</div>
    </div>''' + footer("Next: plant", 1)


def s_click2():
    sectors = [("Field crops", 0), ("Fruit &amp; veg", 0), ("Tree crops", 1), ("Ornamental &amp; nursery", 0), ("Forest &amp; native", 0), ("Turf &amp; pasture", 0)]
    plants = [("Coffee", "Coffea arabica", 1), ("Macadamia", "Macadamia integrifolia", 0), ("Cacao", "Theobroma cacao", 0),
              ("ʻŌhiʻa lehua", "Metrosideros polymorpha", 0)]
    pc = "".join(f'''<div class="card" style="padding:9px;{'border:2px solid var(--brand-600);background:var(--brand-50)' if on else ''}">
        <div style="font-size:13px;font-weight:700">{n}</div><div class="tiny" style="font-style:italic">{sci}</div></div>''' for n, sci, on in plants)
    stages = [("Flowering", 0), ("Green berry", 1), ("Ripening", 0), ("Harvest", 0), ("Dormant / pruned", 0)]
    return status() + appbar("Host plant", "Agricultural · horticultural · ornamental · forest", 2) + f'''
    <div class="body">
      <div class="chips">{"".join(f'<span class="chip {"on" if on else ""}">{s}</span>' for s, on in sectors)}</div>
      <div class="field" style="color:var(--muted)">{ic("search", 16)}<span style="flex:1;margin-left:8px">Search 1,240 plants in the Hawaiʻi list</span></div>
      <div class="grid3" style="grid-template-columns:1fr 1fr">{pc}</div>
      <div class="card">
        <div class="grid2"><div><div class="label">Variety</div><div class="field">Kona Typica</div></div>
        <div><div class="label">Planted <span class="req">*</span></div><div class="field">Mar 2019</div></div></div>
        <div class="label" style="margin-top:10px">Growth stage <span class="tag info">Coffee stages only</span></div>
        <div class="chips">{"".join(f'<span class="chip {"on" if on else ""}">{s}</span>' for s, on in stages)}</div>
        <div class="grid2" style="margin-top:10px"><div><div class="label">First seen</div><div class="field">20 Sep 2026</div></div>
        <div><div class="label">Plant age <span class="tag auto">auto</span></div><div class="field auto">7 y 6 m</div></div></div>
      </div>
    </div>''' + footer("Next: problem", 2)


def s_click3():
    stages = [("Egg", 1), ("Larva", 1), ("Pupa", 0), ("Adult ♀", 1)]
    return status() + appbar("Identify the problem", "AI suggests · you confirm", 3) + f'''
    <div class="body">
      <div class="card" style="padding:12px"><div class="row" style="align-items:flex-start">
        <div style="width:92px;flex:none">{photo("berry", "Snap to identify", False)}</div>
        <div style="flex:1"><div class="row" style="gap:6px;margin-bottom:6px"><span class="tag ai">{ic("ai", 11)} On-device AI</span><span class="tiny">offline · 0.2 s</span></div>
          <div class="row between"><div><b style="font-size:14px">Coffee berry borer</b><div class="tiny" style="font-style:italic">Hypothenemus hampei</div></div><b style="color:var(--brand-700)">94%</b></div>
          <div style="height:5px;border-radius:3px;background:var(--line);margin:5px 0 7px"><div style="width:94%;height:100%;border-radius:3px;background:var(--brand-600)"></div></div>
          <div class="row between tiny"><span>Tropical nut borer</span><span>4%</span></div><div class="row between tiny"><span>Other / unknown</span><span>2%</span></div></div></div>
        <div class="row" style="gap:8px;margin-top:10px"><div class="chip on" style="flex:1;justify-content:center">{ic("check", 14)} Confirm</div><div class="chip" style="flex:1;justify-content:center">Pick from list</div><div class="chip" style="flex:1;justify-content:center">Send to expert</div></div>
      </div>
      <div class="note info" style="padding:8px 11px">{ic("shield", 16)}<div>Established pest in Hawaiʻi · list filtered to <b>Coffee × Hawaiʻi</b> (38 pests, 21 diseases)</div></div>
      <div class="card"><div class="label">Life stages seen <span class="req">* each one needs a photo next</span></div>
        <div class="grid2" style="grid-template-columns:repeat(4,1fr)">{"".join(f'<span class="chip {"on" if on else ""}" style="justify-content:center;padding:7px 4px">{s}</span>' for s, on in stages)}</div>
        <div class="label" style="margin-top:12px">Part affected</div>
        <div class="chips"><span class="chip on">Berries</span><span class="chip">Leaves</span><span class="chip">Branches</span><span class="chip">Roots</span></div>
        <div class="label" style="margin-top:12px">Signs &amp; symptoms <span class="tag info">for this pest</span></div>
        <div class="chips"><span class="chip on">Hole at berry tip</span><span class="chip on">Bean tunnels</span><span class="chip">Berry drop</span><span class="chip">Frass</span></div>
      </div>
    </div>''' + footer("Next: level &amp; photos", 3)


def s_click4():
    return status() + appbar("Level & stage photos", "Pick the level, then photograph every stage", 4) + f'''
    <div class="body">
      <div class="card"><div class="label">Infestation level <span class="tag ai">{ic("ai", 11)} counted</span></div>
        <div class="row" style="gap:6px;margin-bottom:8px"><span class="small">Sampled</span><div class="field" style="padding:5px 9px;font-weight:700">100</div><span class="small">berries · bored</span><div class="field auto" style="padding:5px 9px;font-weight:700">23</div><span class="small">= 23%</span></div>
        <div class="grid3">
          <div class="chip" style="justify-content:center;flex-direction:column;gap:1px;padding:7px 4px">Low<span class="tiny">&lt; 5%</span></div>
          <div class="chip" style="justify-content:center;flex-direction:column;gap:1px;padding:7px 4px">Medium<span class="tiny">5–20%</span></div>
          <div class="chip on" style="justify-content:center;flex-direction:column;gap:1px;padding:7px 4px;background:var(--lava);border-color:var(--lava)">High<span style="font-size:10.5px;opacity:.9">&gt; 20%</span></div></div>
        <div class="tiny" style="margin-top:6px">Thresholds come from the Hawaiʻi pack for Coffee × CBB. You can override with a reason.</div></div>
      <div class="card"><div class="label">Photo for every stage you confirmed <span class="ok">3 / 3</span></div>
        <div class="grid3">{photo("egg", "Egg")}{photo("larva", "Larva")}{photo("adult", "Adult ♀ · 14 counted")}</div>
        <div class="label" style="margin-top:12px">Damage evidence <span class="ok">2 / 2</span></div>
        <div class="grid3">{photo("damage", "Close-up")}{photo("field", "Field view")}<div class="photo empty">{ic("cam", 22)}Add more</div></div>
        <div class="note ai" style="margin-top:10px;padding:8px 10px">{ic("ai", 16)}<div>Quality check passed: in focus · good light · stage matches · GPS + time stamped</div></div></div>
    </div>''' + footer("Next: action, area &amp; send", 4)


def s_click5():
    return status() + appbar("Action, area & send", "Context is pre-filled — just check it", 5) + f'''
    <div class="body" style="gap:10px">
      <div class="card" style="padding:12px"><div class="label">Control already done</div>
        <div class="chips"><span class="chip on">Cultural · strip-picking</span><span class="chip on">Biological</span><span class="chip">Chemical</span><span class="chip">None</span></div>
        <div class="field" style="margin-top:8px;font-size:13px">Beauveria bassiana (strain GHA)<span class="tag reg">registered in HI</span></div></div>
      <div class="card" style="padding:12px"><div class="label">Context <span class="tag auto">auto · edit if wrong</span></div>
        <div class="grid3">
          <div class="field auto" style="flex-direction:column;align-items:flex-start;padding:7px 9px"><span class="tiny">Rain 7 d</span><b style="font-size:13px">38 mm</b></div>
          <div class="field auto" style="flex-direction:column;align-items:flex-start;padding:7px 9px"><span class="tiny">Vegetation</span><b style="font-size:13px">Green</b></div>
          <div class="field" style="flex-direction:column;align-items:flex-start;padding:7px 9px"><span class="tiny">Yield loss</span><b style="font-size:13px">15 %</b></div></div></div>
      <div class="card" style="padding:12px"><div class="label">Affected area</div>
        <div class="grid3"><span class="chip on" style="justify-content:center">Type it</span><span class="chip" style="justify-content:center">Walk edge</span><span class="chip" style="justify-content:center">Draw</span></div>
        <div class="row" style="margin-top:8px"><div class="field" style="flex:1;font-weight:700">0.8</div><span class="small">acres = 0.32 ha</span></div></div>
      <div class="card" style="padding:12px;background:var(--brand-50);border-color:#bfe6d4"><div class="label">Review <span class="tiny">tap any line to edit</span></div>
        <div class="small" style="line-height:1.6">{ic("pin", 13)} North Kona, Hawaiʻi Island · ±4 m<br>{ic("leaf", 13)} Coffee · Kona Typica · green berry<br>{ic("bug", 13)} Coffee berry borer · egg, larva, adult<br>{ic("alert", 13)} <b style="color:var(--lava)">High · 23%</b> · 5 photos · 0.8 ac</div>
        <div class="row tiny" style="margin-top:8px;gap:5px"><span class="tag auto">Draft</span>›<span class="tag auto">Ready</span>›<span class="tag info">Pending sync</span>›<span class="tag" style="background:#e6f6e6;color:#155c15">Sent</span></div></div>
    </div>''' + footer(f'{ic("send")} Submit report', 5, "")


def big_island_hexes():
    """Stylised Hawai'i Island with H3-like hex risk cells (illustrative, not real data)."""
    import math
    outline = "M150 40 L205 60 L250 95 L300 150 L318 205 L290 250 L240 300 L185 340 L140 372 L105 360 L90 320 L70 270 L55 215 L62 160 L85 110 L115 65 Z"
    risk = {(3, 6): 4, (3, 7): 4, (2, 7): 3, (4, 7): 3, (3, 8): 3, (2, 8): 4, (2, 9): 3, (3, 9): 2, (2, 10): 2, (3, 5): 3, (4, 5): 2,
            (4, 6): 2, (2, 6): 2, (5, 4): 1, (6, 4): 1, (7, 5): 2, (8, 6): 1, (7, 3): 1, (8, 4): 1, (6, 8): 1, (5, 9): 1, (4, 10): 2,
            (3, 10): 3, (4, 11): 1, (5, 7): 1, (8, 8): 2, (9, 7): 1, (6, 2): 1, (5, 2): 2, (4, 3): 2, (4, 4): 1}
    cols = {1: "var(--risk-1)", 2: "var(--risk-2)", 3: "var(--risk-3)", 4: "var(--risk-4)"}
    r = 15
    hexes = ""
    for (c, rw), v in risk.items():
        cx = 40 + c * r * 1.5 + 10
        cy = 30 + rw * r * math.sqrt(3) + (c % 2) * r * math.sqrt(3) / 2
        pts = " ".join(f"{cx + (r - 1) * math.cos(math.radians(60 * k)):.1f},{cy + (r - 1) * math.sin(math.radians(60 * k)):.1f}" for k in range(6))
        hexes += f'<polygon points="{pts}" fill="{cols[v]}" fill-opacity=".92" stroke="#fff" stroke-width="1.5"/>'
    return (f'<svg viewBox="0 0 360 400" style="width:100%;height:100%;display:block;background:#cfe3f1">'
            f'<defs><clipPath id="isl"><path d="{outline}"/></clipPath></defs>'
            f'<path d="{outline}" fill="#eef1e6" stroke="#b9c4b0" stroke-width="2"/><g clip-path="url(#isl)">{hexes}</g>'
            '<text x="70" y="235" font-size="11" fill="#4a5a53" font-family="Inter">KONA</text><text x="232" y="150" font-size="11" fill="#4a5a53" font-family="Inter">HILO</text>'
            '<text x="210" y="300" font-size="11" fill="#4a5a53" font-family="Inter">PUNA</text><text x="120" y="110" font-size="11" fill="#4a5a53" font-family="Inter">KOHALA</text>'
            '<circle cx="95" cy="222" r="7" fill="none" stroke="#10201a" stroke-width="2"/></svg>')


def s_click6():
    legend = "".join(f'<div class="row" style="gap:4px"><i style="width:14px;height:10px;border-radius:2px;background:var(--risk-{i})"></i><span class="tiny">{t}</span></div>'
                     for i, t in enumerate(["Low", "Moderate", "High", "Very high"], 1))
    return status() + appbar("Risk map", "One lightweight map · offline vector tiles", 6) + f'''
    <div style="padding:10px 16px 0" class="chips"><span class="chip on">Coffee berry borer</span><span class="chip">Last 30 days</span><span class="chip">All hosts</span><span class="chip">H3 · 1 km</span></div>
    <div style="flex:1;position:relative;margin:10px 16px 0;border-radius:16px;overflow:hidden;border:1px solid var(--line)">{big_island_hexes()}
      <div style="position:absolute;left:10px;top:10px;background:#fff;border-radius:10px;padding:7px 9px;display:flex;flex-direction:column;gap:3px">{legend}</div>
      <div style="position:absolute;right:10px;top:10px;display:flex;flex-direction:column;gap:6px"><div class="chip" style="padding:6px">{ic("gps", 16)}</div><div class="chip" style="padding:6px">{ic("list", 16)}</div></div></div>
    <div class="card" style="margin:10px 16px 0;padding:12px"><div class="row between"><b>North Kona</b><span class="tag" style="background:var(--risk-4);color:#fff">Very high · PRI 81</span></div>
      <div class="grid3" style="margin-top:8px"><div><div class="big" style="font-size:18px">42</div><div class="tiny">reports</div></div><div><div class="big" style="font-size:18px">▲ 18%</div><div class="tiny">vs last month</div></div><div><div class="big" style="font-size:18px">23%</div><div class="tiny">median infest.</div></div></div>
      <div class="row" style="gap:8px;margin-top:10px"><span class="chip" style="flex:1;justify-content:center">{ic("chart", 14)} Trend</span><span class="chip" style="flex:1;justify-content:center">{ic("download", 14)} Export</span><span class="chip on" style="flex:1;justify-content:center">{ic("alert", 14)} Alert</span></div></div>
    ''' + footer(f'{ic("ai")} Next: AI Lab', 6, "sun")


def s_click7():
    boxes = ""
    for i, (x, y) in enumerate(TRAP_INSECTS):
        c, w = ("#d9542f", 10) if i == 14 else ("#5b3fc4", 7)
        boxes += f'<rect x="{x - w / 2:.1f}" y="{y - w / 2:.1f}" width="{w}" height="{w}" fill="none" stroke="{c}" stroke-width=".9"/><rect x="{x - w / 2:.1f}" y="{y - w / 2 - 2.6:.1f}" width="{w}" height="2.6" fill="{c}"/>'
    img = art("trap").replace("</svg>", boxes + "</svg>")
    return status() + appbar("AI Lab", "Identify · count · measure", 7) + f'''
    <div class="body">
      <div class="chips"><span class="chip">Identify</span><span class="chip on">Count</span><span class="chip">% leaf damage</span><span class="chip">Batch</span></div>
      <div style="border-radius:16px;overflow:hidden;aspect-ratio:1.05;position:relative">{img}
        <div style="position:absolute;left:10px;bottom:10px;background:rgba(16,32,26,.8);color:#fff;border-radius:10px;padding:6px 10px;font-size:12px">Yellow sticky trap · Kona-07</div></div>
      <div class="card"><div class="row between"><div><div class="tiny">Coffee berry borer adults</div><div class="big">14</div></div>
        <div><div class="tiny">Other insects</div><div class="big" style="color:var(--lava)">1</div></div><div><div class="tiny">Mean confidence</div><div class="big">0.91</div></div></div>
        <div class="tiny" style="margin-top:6px">Model: Hawaiʻi pack · detector v3 (412 classes) · runs on phone in C++ (ONNX Runtime / TFLite) · 180 ms</div></div>
      <div class="grid2"><div class="btn ghost" style="font-size:14px;padding:12px">Fix a box</div><div class="btn ghost" style="font-size:14px;padding:12px">Send to expert</div></div>
    </div>''' + footer(f'{ic("check")} Attach count to report', 7, "sun")


SCREENS = {
    "00_region_pack": s_region, "01_home": s_home, "02_click1_where": s_click1, "03_click2_host": s_click2,
    "04_click3_problem": s_click3, "05_click4_level_photos": s_click4, "06_click5_action_area_submit": s_click5,
    "07_click6_risk_map": s_click6, "08_click7_ai_lab": s_click7,
}
