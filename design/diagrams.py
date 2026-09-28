"""Explanatory diagrams for the PestLand manual (HTML -> PNG via render.py)."""
from screens import art, ic

CSS = """
<style>
.dg{background:#fff;border-radius:22px;padding:30px 34px;font-family:Inter,sans-serif;color:#10201a;width:100%}
.dg h2{font-size:26px;font-weight:800;color:#0b3b2e}.dg .lead{font-size:14px;color:#4a5a53;margin:6px 0 22px}
.lane{display:flex;align-items:stretch;gap:10px;margin-bottom:16px}
.lane .who{width:150px;flex:none;font-weight:800;font-size:15px;display:flex;flex-direction:column;justify-content:center}
.lane .who span{font-size:12px;font-weight:500;color:#85928c}
.step{flex:1;border-radius:14px;padding:12px;font-size:12.5px;line-height:1.35;border:1px solid #e3e8e5;background:#f6f8f7}
.step b{display:block;font-size:13.5px;margin-bottom:4px}
.step.pl{background:#dff3ea;border-color:#9fd8bf}.step.an{background:#fff3d6;border-color:#f2d08a}
.arrow{align-self:center;color:#85928c;font-size:18px}
.box{border-radius:16px;padding:14px 16px;border:1px solid #e3e8e5;background:#f6f8f7}
.box h4{font-size:15px;font-weight:800;margin-bottom:6px;display:flex;gap:8px;align-items:center}
.box ul{margin-left:16px;font-size:12.5px;line-height:1.5;color:#4a5a53}
.cols{display:grid;gap:14px}
.k{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#85928c;margin-bottom:6px}
</style>"""


def workflow():
    cp = [("Report type", "pop-up: Pest/Disease or Weed"), ("Location", "GPS + County, Sub-county, Ward, Village"),
          ("Crop", "crop, variety, stage, 2 dates, age"), ("Pest", "pest, stage, part, symptoms, control, level, pesticide"),
          ("Photos", "1 close-up + 1 field photo"), ("More info", "rainfall, vegetation, yield loss, notes"),
          ("Area", "manual or map (OSM + Google aerial)"), ("Submit", "online or pending")]
    pl = [("1 · Where", "GPS auto-fills all admin levels from offline boundaries; pick report type"),
          ("2 · Host plant", "any plant sector; stage list follows the plant; age auto-computed"),
          ("3 · Identify", "on-device AI suggests; confirm; tick life stages, part, symptoms"),
          ("4 · Level & photos", "count → level from region thresholds; one photo per confirmed stage + damage"),
          ("5 · Act & send", "control, auto weather, area, review, submit / queue offline")]
    an = [("6 · Risk map", "H3 hex risk index, trends, alerts, export"), ("7 · AI Lab", "identify, count traps, % damage, expert queue")]
    lane = lambda items, cls: '<span class="arrow">›</span>'.join(f'<div class="step {cls}"><b>{a}</b>{b}</div>' for a, b in items)
    return CSS + f'''<div class="dg"><h2>From 8 CropProtect pages to 5 + 2 PestLand clicks</h2>
    <div class="lead">Same backbone (where → plant → problem → evidence → context → area → submit), fewer screens, more automation, and two new analysis clicks.</div>
    <div class="lane"><div class="who">CropProtect<span>8 pages · ~30 fields · Kenya only</span></div>{lane(cp, "")}</div>
    <div class="lane"><div class="who">PestLand · collect<span>5 clicks · ~12 typed/tapped inputs</span></div>{lane(pl, "pl")}</div>
    <div class="lane"><div class="who">PestLand · analyse<span>2 clicks</span></div>{lane(an, "an")}<div style="flex:2.6"></div></div></div>'''


def architecture():
    col = lambda title, icon, items, bg: f'<div class="box" style="background:{bg}"><h4>{ic(icon, 18)}{title}</h4><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div>'
    return CSS + f'''<div class="dg"><h2>PestLand architecture — PERN + on-device C++ AI</h2>
    <div class="lead">One codebase for Android/iOS, offline-first, one map library, region packs loaded at runtime.</div>
    <div class="cols" style="grid-template-columns:1.1fr 1fr 1fr 1fr">
      <div><div class="k">Phone (field)</div>
        {col("React Native + Expo", "home", ["TypeScript, Expo Router", "NativeWind = Tailwind classes", "Zustand state, React Hook Form + Zod", "SQLite (op-sqlite) offline store + outbox"], "#dff3ea")}
        <div style="height:10px"></div>
        {col("Native C++ modules (JSI)", "ai", ["ONNX Runtime Mobile / LiteRT (TFLite)", "YOLO-family detector: ID + counting", "Image quality check (blur, light)", "H3 cell index, point-in-polygon"], "#efe9ff")}
        <div style="height:10px"></div>
        {col("One map: MapLibre Native", "map", ["Offline PMTiles vector basemap", "Used only in Area-draw + Risk map", "No Google Maps, no Leaflet WebView"], "#e3effc")}</div>
      <div><div class="k">API (Node)</div>
        {col("Express 5 · Node 22 LTS", "sync", ["REST + OpenAPI; JWT auth + roles", "Idempotent sync (client UUIDs)", "Resumable photo upload (tus) → S3/MinIO", "Region-pack builder &amp; signer"], "#f6f8f7")}
        <div style="height:10px"></div>
        {col("Workers", "chart", ["BullMQ jobs: risk index, alerts", "Weather enrichment (Open-Meteo)", "Model retraining export (COCO)", "Email / SMS / push alerts"], "#f6f8f7")}</div>
      <div><div class="k">Data</div>
        {col("PostgreSQL 17 + PostGIS", "shield", ["Incidents, photos, stages, counts", "Admin boundaries per region", "h3-pg extension for hex risk", "Row-level security per region/org"], "#fff3d6")}
        <div style="height:10px"></div>
        {col("Object storage", "cam", ["Original + web-sized photos", "EXIF GPS/time kept for audit", "Signed URLs only"], "#f6f8f7")}</div>
      <div><div class="k">Web (office)</div>
        {col("React 19 + Vite + Tailwind v4", "chart", ["Review &amp; approve queue (ODK Central-style)", "Expert ID + box correction", "Dashboards, risk maps, exports (CSV, GeoJSON, Shapefile)", "Form &amp; region-pack editor"], "#f6f8f7")}</div>
    </div></div>'''


def region_pack():
    items = [("globe", "Boundaries", "Admin levels + names + GeoJSON, e.g. Hawaiʻi: State › Island › County › District"),
             ("leaf", "Host plants", "Plants grown/present in the region, grouped by sector, with their growth stages"),
             ("bug", "Pests, diseases, weeds", "Filtered per host; status: established · regulated · quarantine · new-to-region"),
             ("chart", "Severity rules", "Count/sample methods and Low/Medium/High thresholds per host × pest"),
             ("shield", "Rules &amp; products", "Agency to notify, reportable list, registered control products"),
             ("ai", "AI model", "Detector trained on that region's species list + label map"),
             ("map", "Offline map", "Clipped PMTiles basemap for the region (the only map data on the phone)"),
             ("user", "Language &amp; units", "Translations, acres/hectares, °F/°C, date format, time zone")]
    cards = "".join(f'<div class="box"><h4>{ic(i, 18)}{t}</h4><div style="font-size:12.5px;color:#4a5a53;line-height:1.45">{d}</div></div>' for i, t, d in items)
    return CSS + f'''<div class="dg"><h2>What a region pack contains</h2>
    <div class="lead">Selecting a region (or letting GPS pick it) swaps all eight layers at once, so every list, rule and map is confined to that region. New region = new pack, not new code.</div>
    <div class="cols" style="grid-template-columns:repeat(4,1fr)">{cards}</div>
    <div class="lead" style="margin:18px 0 0">Packs shipped at launch: <b>Hawaiʻi</b> · <b>Guam</b> · <b>USA states</b> · <b>Australia</b> · <b>Papua New Guinea</b> · <b>Kenya</b> (migrated from CropProtect). Packs are signed JSON + GeoJSON + PMTiles + model, versioned like v2026.09.</div></div>'''


def photo_guide():
    tile = lambda k, t, d: f'<div><div style="border-radius:14px;overflow:hidden;aspect-ratio:1">{art(k)}</div><b style="display:block;margin-top:8px;font-size:14px">{t}</b><div style="font-size:12px;color:#4a5a53;line-height:1.4">{d}</div></div>'
    return CSS + f'''<div class="dg"><h2>Stage photo guide — one photo per confirmed stage</h2>
    <div class="lead">After choosing the infestation level (Click 4) PestLand opens one camera slot for every stage you ticked in Click 3. A report cannot be sent until each ticked stage has a passing photo.</div>
    <div class="k">Insects &amp; mites</div>
    <div class="cols" style="grid-template-columns:repeat(4,1fr)">
      {tile("egg", "Egg", "Macro distance (5–10 cm). Include the leaf/berry surface they sit on.")}
      {tile("larva", "Larva / nymph", "Whole body in frame, side view if possible. Do not squash it.")}
      {tile("pupa", "Pupa", "Show the case/cocoon and where it was found (soil, fold, bark).")}
      {tile("adult", "Adult", "Top view, fill the frame. Add a coin or ruler for scale.")}</div>
    <div class="k" style="margin-top:18px">Damage, disease &amp; weeds</div>
    <div class="cols" style="grid-template-columns:repeat(4,1fr)">
      {tile("damage", "Symptom close-up", "The organ with symptoms; hold phone parallel, no shadow.")}
      {tile("leaf", "Disease stage", "Early (small spot), advancing and late (necrotic) lesions each count as a stage.")}
      {tile("field", "Field view", "Arms braced, phone at chest height, show the affected patch vs healthy.")}
      {tile("trap", "Trap / sample card", "Whole card flat, even light — AI Lab counts it (Click 7).")}</div></div>'''


def feature_sources():
    rows = [("From CropProtect (kept)", "#f6f8f7", ["Crop-first logic, crop-filtered pest lists", "Pest/disease vs weed branch", "Close-up + field photos", "Rainfall, vegetation, yield loss", "Manual or mapped area", "Offline pending queue"]),
            ("From ODK Collect / Central", "#e3effc", ["Draft › Ready › Pending › Sent states", "Constraints, skip logic, calculated fields", "GPS accuracy threshold", "Form &amp; pack versioning, audit log", "Encrypted, idempotent sync", "Review/approve queue on the web"]),
            ("From Plantix", "#efe9ff", ["Photo-first AI identification", "Visual plant &amp; pest cards", "Photo quality coaching", "Multi-language UI", "Weather context", "Approved guidance links (not prescriptions)"]),
            ("From FAO FAMEWS", "#fff3d6", ["Standard scouting/sampling protocol", "Counts → % infestation → level", "Trap monitoring", "Risk / hotspot maps", "Early-warning alerts", "Shared, comparable data across regions"]),
            ("New in PestLand", "#dff3ea", ["Region packs (Hawaiʻi, Guam, AU, PNG, US, KE)", "Any plant: farm, garden, ornamental, forest, native", "Photo for every life stage", "On-device C++ AI counting", "H3 hex risk index", "One lightweight map only"])]
    cols = "".join(f'<div class="box" style="background:{bg}"><h4>{t}</h4><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div>' for t, bg, items in rows)
    return CSS + f'''<div class="dg"><h2>What PestLand takes from each app</h2>
    <div class="lead">CropProtect's surveillance backbone, plus the missing features from ODK Collect, Plantix and FAMEWS.</div>
    <div class="cols" style="grid-template-columns:repeat(5,1fr)">{cols}</div></div>'''


DIAGRAMS = {
    "workflow_comparison": (workflow, 2000),
    "architecture": (architecture, 1700),
    "region_pack": (region_pack, 1700),
    "photo_stage_guide": (photo_guide, 1100),
    "feature_sources": (feature_sources, 1800),
}
