// Build docs/PestLand_User_Manual.docx (Word) from the rendered images.
// Usage: NODE_PATH=<dir with docx installed> node scripts/build_manual_docx.js
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, ImageRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, LevelFormat, PageBreak, TableOfContents, Footer, PageNumber, VerticalAlign,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const IMG = (p) => path.join(ROOT, "docs", "images", p);
const GREEN = "0B3B2E", MID = "11624A", SOFT = "DFF3EA", INK2 = "4A5A53", LINE = "D5DED9", SUN = "FFF3D6";
const PAGE_W = 12240, MARGIN = 1080, CONTENT = PAGE_W - 2 * MARGIN; // US Letter, 0.75" margins

// ---------- helpers ----------
const t = (text, o = {}) => new TextRun({ text, ...o });
const p = (children, o = {}) => new Paragraph({ children: Array.isArray(children) ? children : [t(children)], spacing: { after: 120 }, ...o });
const h1 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [t(text)], pageBreakBefore: true });
const h2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [t(text)] });
const h3 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [t(text)] });
const bullet = (runs) => new Paragraph({ numbering: { reference: "bul", level: 0 }, children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 60 } });
const num = (runs, ref = "num") => new Paragraph({ numbering: { reference: ref, level: 0 }, children: Array.isArray(runs) ? runs : [t(runs)], spacing: { after: 60 } });
const caption = (text) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [t(text, { italics: true, size: 18, color: INK2 })] });

function img(file, widthIn) {
  const buf = fs.readFileSync(IMG(file));
  const w = buf.readUInt32BE(16), hgt = buf.readUInt32BE(20); // PNG IHDR
  const W = Math.round(widthIn * 96), H = Math.round((W * hgt) / w);
  return new ImageRun({ type: "png", data: buf, transformation: { width: W, height: H }, altText: { title: file, description: file, name: file } });
}
const figure = (file, widthIn, cap) => [new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 60 }, children: [img(file, widthIn)] }), caption(cap)];

const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };
const thin = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const thinBorders = { top: thin, bottom: thin, left: thin, right: thin };

function table(headers, rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  const cell = (text, w, head) => new TableCell({
    width: { size: w, type: WidthType.DXA }, borders: thinBorders,
    shading: head ? { type: ShadingType.CLEAR, fill: SOFT, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ children: [t(String(text), { bold: !!head, size: 18 })] })],
  });
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: headers.map((h, i) => cell(h, widths[i], true)) }),
      ...rows.map((r) => new TableRow({ children: r.map((c, i) => cell(c, widths[i], false)) }))],
  });
}

function note(text, fill = SUN) {
  return new Table({
    width: { size: CONTENT, type: WidthType.DXA }, columnWidths: [CONTENT],
    rows: [new TableRow({ children: [new TableCell({
      width: { size: CONTENT, type: WidthType.DXA }, borders: noBorders,
      shading: { type: ShadingType.CLEAR, fill, color: "auto" }, margins: { top: 100, bottom: 100, left: 160, right: 160 },
      children: [new Paragraph({ children: Array.isArray(text) ? text : [t(text, { size: 19 })] })],
    })] })],
  });
}

// Screen on the right, explanation on the left (the CropProtect manual's layout)
function screenBlock(file, cap, leftChildren) {
  const L = 6000, R = CONTENT - L;
  return new Table({
    width: { size: CONTENT, type: WidthType.DXA }, columnWidths: [L, R],
    rows: [new TableRow({ children: [
      new TableCell({ width: { size: L, type: WidthType.DXA }, borders: noBorders, margins: { right: 200 }, children: leftChildren }),
      new TableCell({ width: { size: R, type: WidthType.DXA }, borders: noBorders, verticalAlign: VerticalAlign.TOP,
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [img(file, 2.35)] }), caption(cap)] }),
    ] })],
  });
}

// One field, CropProtect-manual style: name · required · brief description · how to fill it
function field(name, required, brief, how) {
  return [
    new Paragraph({ spacing: { before: 160, after: 40 }, children: [t(name, { bold: true, color: MID, size: 22 }), t(required ? "   Required" : "   Optional", { size: 16, color: required ? "9C3417" : INK2, bold: true })] }),
    new Paragraph({ spacing: { after: 40 }, children: [t("Brief description: ", { bold: true, size: 19 }), t(brief, { size: 19 })] }),
    new Paragraph({ spacing: { after: 80 }, children: [t("How to fill it: ", { bold: true, size: 19 }), t(how, { size: 19 })] }),
  ];
}
const nextTap = (n, label) => p([t(`Tap `, {}), t(`${label}`, { bold: true }), t(` — this is click ${n}.`)], { spacing: { before: 120, after: 200 } });

// ---------- content ----------
const children = [];

// Cover
children.push(
  new Paragraph({ spacing: { before: 600, after: 0 }, children: [t("PESTLAND", { bold: true, size: 72, color: GREEN })] }),
  new Paragraph({ spacing: { after: 120 }, children: [t("APP MANUAL", { bold: true, size: 40, color: MID })] }),
  p([t("Plant health surveillance for any plant, in any region", { size: 26, color: INK2 })]),
  p([t("Version 1.0 · September 2026", { size: 20, color: INK2 })], { spacing: { after: 360 } }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [img("screens/journey_5_plus_2.png", 6.9)] }),
  caption("5 clicks to collect a report, 2 clicks to see the results"),
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({ children: [t("Contents", { bold: true, size: 32, color: GREEN })], spacing: { after: 200 } }),
  new TableOfContents("Contents", { hyperlink: true, headingStyleRange: "1-2" }),
  p([t("Right-click the table and choose Update Field if page numbers are missing.", { italics: true, size: 16, color: INK2 })]),
);

// 1 About
children.push(
  h1("1. About PestLand"),
  p("PestLand is a mobile app for reporting and mapping insect pests, plant diseases and weeds on any plant: field crops, fruit and vegetables, tree crops, ornamentals and nursery stock, forest and native plants, turf and pasture."),
  p("It keeps the backbone of CropProtect (where → plant → problem → evidence → context → area → submit) and adds the features CropProtect was missing from ODK Collect, Plantix and FAO FAMEWS."),
  ...figure("diagrams/feature_sources.png", 6.9, "What PestLand takes from each app"),
  h2("Two design rules"),
  bullet([t("Simple. ", { bold: true }), t("5 screens to collect a report and 2 screens to see results. Anything the phone can work out (place names, plant age, weather, level from a count) is filled in for you.")]),
  bullet([t("Light. ", { bold: true }), t("CropProtect loaded a Google/Leaflet map on several pages. PestLand opens a map only when you draw an area or look at the risk map, and that map uses small offline vector tiles.")]),
);

// 2 Getting started
children.push(
  h1("2. Getting started"),
  h2("2.1 Permissions"),
  p("When PestLand first opens, tap Allow while using the app for each request. These are part of the app's settings and are needed for the fields that fill themselves in."),
  table(["Permission", "Why PestLand needs it"], [
    ["Location", "Fills in GPS and every admin area in Click 1"],
    ["Camera", "Stage photos, damage photos and AI identification"],
    ["Storage / photos", "Keeps reports and photos on the phone until they are sent"],
    ["Notifications (optional)", "Regional alerts and reports that need your attention"],
  ], [3000, CONTENT - 3000]),
  h2("2.2 Sign in"),
  p("Sign in with your email, or the phone number your region uses. Your role (collector, expert, reviewer or region admin) decides what you see."),
  h2("2.3 Choose your region pack"),
  screenBlock("screens/00_region_pack.png", "Choose region pack", [
    p("On first launch PestLand reads your GPS and suggests a region pack, for example Hawaiʻi. Tap Download & use."),
    p("The region pack decides everything that follows:"),
    bullet("admin areas and their names"), bullet("plant, pest, disease and weed lists"), bullet("the legal status of each pest in that region"),
    bullet("severity rules and registered control products"), bullet("the AI model and the offline map"), bullet("language and units (acres or hectares, °F or °C)"),
    p("Choose Hawaiʻi and every list and map stays inside Hawaiʻi. You can hold several packs and switch any time from Profile › Region."),
  ]),
);

// 3 Home
children.push(
  h1("3. Home screen and sync"),
  screenBlock("screens/01_home.png", "Home", [
    ...field("Report new incident", true, "Starts the 5-click report.", "Tap the large green button."),
    ...field("Risk map / AI Lab", false, "Shortcuts to Click 6 and Click 7.", "Tap either button."),
    ...field("Status cards", false, "Drafts, Ready to send, Pending sync and Sent today.", "Tap a card to open that list."),
    ...field("Regional alert", false, "Messages from the region's plant-protection agency.", "Read it; tap to see details."),
    ...field("Recent reports", false, "Your latest reports with tags: Sent, Pending, Needs ID.", "Tap a report to open or finish it."),
  ]),
  h2("Working offline"),
  screenBlock("screens/11_outbox_sync.png", "Reports & sync", [
    p("Every report moves through clear states:"),
    p([t("Draft → Ready → Pending sync → Sent → Approved / Rejected / Needs ID", { bold: true })]),
    bullet("Everything works offline: lists, boundaries, AI, map tiles and photo checks are all in the region pack on your phone."),
    bullet("Each report gets a unique ID on the phone, so a retry never creates a duplicate."),
    bullet("Photos upload in pieces and resume after a dropped connection."),
    bullet("In low-connectivity packs such as PNG, a short text summary can go by SMS and the photos follow later."),
    p("As in the CropProtect manual: send the day's reports right after fieldwork. PestLand reminds you if anything is still Pending at the end of the day."),
  ]),
);

// 4 Overview
children.push(
  h1("4. The 5 + 2 clicks"),
  p("A click means one screen, finished with one Next tap. The yellow numbered dot on each Next button shows which click you are on. The bar at the top shows 5 green segments for collecting and 2 amber ones for analysing."),
  ...figure("diagrams/workflow_comparison.png", 6.9, "From 8 CropProtect pages to 5 + 2 PestLand clicks"),
  table(["Click", "Screen", "You do", "PestLand does for you"], [
    ["1", "Where & what type", "Check location; pick Insect, Disease, Weed or Not sure", "GPS, accuracy, every admin level, boundary check"],
    ["2", "Host plant", "Pick sector, plant, stage, planting date", "Stage list for that plant, plant age"],
    ["3", "Identify", "Snap a photo, confirm the AI answer, tick stages, parts, symptoms", "AI suggestion, lists filtered to this plant in this region, legal status"],
    ["4", "Level & stage photos", "Enter your count, then one photo per stage", "% → level from the region rule, photo quality check, AI count"],
    ["5", "Action, area & send", "Control used, yield loss, area, Submit", "Weather, vegetation, unit conversion, review, offline queue"],
    ["6", "Risk map", "Filter and read", "Hexagon risk index, trend, alerts, export"],
    ["7", "AI Lab", "Photograph a trap or leaf", "Identification, counting, % damage, expert queue"],
  ], [700, 1900, 3600, CONTENT - 6200]),
);

// Click 1
children.push(
  h1("5. Click 1 — Where & what type"),
  screenBlock("screens/02_click1_where.png", "Click 1", [
    ...field("GPS", true, "Latitude and longitude of where you are standing, with an accuracy badge.",
      "Filled in automatically. Good = 10 m or better, Fair = 10–30 m, Poor = over 30 m. If Poor, step into the open and wait a few seconds."),
    ...field("Admin areas", true, "The administrative areas for the report. The levels follow the region: Hawaiʻi uses State › Island › County › District; Kenya uses County › Sub-county › Ward, as in CropProtect.",
      "Filled in automatically from the offline boundaries in your region pack. Tap a level to change it."),
    ...field("Boundary check", true, "Confirms that the GPS point is inside the areas selected.",
      "If a yellow warning appears, check the areas or your GPS. About 1 in 100 CropProtect reports from the three main counties were more than 80 km from their county's centre; this check stops that error."),
    ...field("Place / farm name", false, "A local name, e.g. a village, ahupuaʻa or farm.", "Type the name."),
    ...field("What are you reporting?", true, "Chooses the branch of the form, like CropProtect's Report Type pop-up.",
      "Tap Insect / mite, Disease, Weed or Not sure. Not sure makes photos compulsory and sends the report to an expert."),
  ]),
  nextTap(1, "Next: plant"),
);

// Click 2
children.push(
  h1("6. Click 2 — Host plant"),
  screenBlock("screens/03_click2_host.png", "Click 2", [
    ...field("Sector", true, "The kind of plant: Field crops, Fruit & veg, Tree crops, Ornamental & nursery, Forest & native, Turf & pasture.", "Tap one chip."),
    ...field("Plant", true, "The plant with the problem. Only plants in the region pack are listed.",
      "Tap a card or search. If a plant is missing, type it under Other and the region admin is told."),
    ...field("Variety", false, "The variety or cultivar, e.g. Kona Typica.", "Type it."),
    ...field("Growth stage", true, "The plant's stage when the problem was seen. Only stages of the chosen plant are shown.", "Tap one stage."),
    ...field("Planted / First seen", true, "When the plant was planted and when the problem was first seen.",
      "Pick both dates. PestLand blocks a planting date after the first-seen date. Choose Unknown if the grower doesn't know."),
    ...field("Plant age", true, "Age of the plant at the time of the report.", "Worked out automatically from the planting date."),
  ]),
  nextTap(2, "Next: problem"),
);

// Click 3
children.push(
  h1("7. Click 3 — Identify the problem"),
  screenBlock("screens/04_click3_problem.png", "Click 3 — insect", [
    ...field("Snap to identify", false, "The on-device AI names the problem from a photo, offline, in about 0.2 seconds.",
      "Take one clear photo. The top three answers appear with confidence."),
    ...field("Problem", true, "The pest or disease. The AI only suggests; your choice is what is recorded.",
      "Tap Confirm, Pick from list (filtered to this plant in this region) or Send to expert (saved as Needs ID)."),
    ...field("Status badge", true, "The problem's legal status in your region: Established, Regulated, Quarantine, Exotic or New to region.",
      "Shown automatically. Regulated, quarantine and exotic reports are forwarded to the agency named in the region pack."),
    ...field("Life stages seen", true, "The stages you actually saw: Egg, Larva/Nymph, Pupa, Adult. For diseases: Early, Advancing, Late.",
      "Tick every stage seen. Each ticked stage needs its own photo in Click 4."),
    ...field("Part affected / Signs & symptoms", true, "Where the damage is and what it looks like. Lists are filtered to the chosen problem.", "Tick all that apply."),
  ]),
  h2("Weed branch"),
  screenBlock("screens/09_click3_weed.png", "Click 3 — weed", [
    p("If you picked Weed in Click 1, Click 3 shows weed lists instead. CropProtect had a separate weed form; PestLand uses the same screens."),
    ...field("Weed", true, "The weed or invasive plant, e.g. Miconia in Hawaiʻi.", "Confirm the AI answer, pick from the list or send to an expert."),
    ...field("Growth stages seen", true, "Seedling, Vegetative, Flowering, Seeding.", "Tick every stage seen; each needs a photo in Click 4."),
    ...field("Where is it growing?", true, "In the crop, field edge, pasture, forest/native, waterway.", "Tap one."),
    ...field("Cover", true, "Share of the area covered by the weed. This sets the weed's level.", "Tap a range."),
  ]),
  nextTap(3, "Next: level & photos"),
);

// Click 4
children.push(
  h1("8. Click 4 — Level & stage photos"),
  p("Select the level first. Then take a photo of every stage you confirmed in Click 3."),
  screenBlock("screens/05_click4_level_photos.png", "Click 4 — insect", [
    ...field("Infestation level", true,
      "How bad the problem is. PestLand replaces CropProtect's bare Low/Medium/High with a count, as in FAMEWS.",
      "Enter the number sampled and the number affected (e.g. 100 berries, 23 bored). PestLand works out the % and picks the level from the region's rule. To disagree, tap another level and give a reason."),
    table(["Coffee × coffee berry borer (Hawaiʻi example)", "Low", "Medium", "High"], [["Bored berries per 100", "< 5 %", "5–20 %", "> 20 %"]], [2600, 1000, 1200, 1200]),
    ...field("Stage photos", true, "One photo for every stage ticked in Click 3.",
      "Tap each slot and take the photo. Next stays locked until every stage has a photo that passes the quality check (focus, light, stage visible)."),
    ...field("Damage close-up / Field view", true, "Close-up of the affected part, and a wide shot of the patch.", "Take both. Add more if useful."),
  ]),
  h2("Disease example"),
  screenBlock("screens/10_click4_disease_stages.png", "Click 4 — disease", [
    p("For a disease the stages are symptom stages. In this coffee leaf rust example the collector ticked Early, Advancing and Late in Click 3, so Click 4 opens three stage slots."),
    p("The level comes from leaves checked and leaves with rust (60 checked, 14 with rust = 23 % = Medium under this example rule). The AI also estimates the % of leaf area infected from the photos."),
  ]),
  h2("Photo guide"),
  ...figure("diagrams/photo_stage_guide.png", 5.6, "One photo per confirmed stage"),
  p("Photo tips from the CropProtect manual still apply:"),
  bullet("Hold the phone parallel to the pest or leaf and don't cast a shadow."),
  bullet("Get close enough that the pest fills the frame, without disturbing it."),
  bullet("For the field view, hold the phone at chest height with both hands and brace your elbows against your body."),
  bullet("Use Retry freely. Only accepted photos are kept."),
  nextTap(4, "Next: action, area & send"),
);

// Click 5
children.push(
  h1("9. Click 5 — Action, area & send"),
  screenBlock("screens/06_click5_action_area_submit.png", "Click 5", [
    ...field("Control already done", false, "Actions taken against the problem: Cultural, Physical/mechanical, Biological, Chemical, None.",
      "Tick all that apply. For Chemical or Biological, pick the product from the region's registered list or type it under Other. PestLand records what was done; it does not prescribe."),
    ...field("Rain, last 7 days", true, "Recent rainfall. In CropProtect this was blank in 88 % of reports.",
      "Pre-filled from a weather service when online. Edit it if the grower says otherwise; the source is saved."),
    ...field("Vegetation", true, "State of plants around the field: Green, Greening, Drying, Dry.", "Pre-suggested from the field photo; change if wrong."),
    ...field("Yield loss", true, "Estimated loss, 0–100 %.", "Type the grower's estimate."),
    ...field("Affected area", true, "The size of the affected patch.",
      "Type it (acres or hectares, per region), Walk edge (GPS track) or Draw on the map. Draw is the only data-collection step that opens a map."),
    ...field("Review", true, "A one-card summary of the report.", "Tap any line to go back and edit."),
  ]),
  nextTap(5, "Submit report"),
  note("With a signal the report is sent. Without one it moves to Pending sync and goes automatically later.", SOFT),
);

// Click 6
children.push(
  h1("10. Click 6 — Risk map"),
  screenBlock("screens/07_click6_risk_map.png", "Click 6", [
    p("The risk map is the only analysis map in PestLand. It shows hexagon cells (about 1 km across) coloured by the PestLand Risk Index (PRI)."),
    note([t("PRI = 100 × (average severity − 1) ÷ 2 × confidence. ", { bold: true, size: 19 }),
      t("Severity: Low = 1, Medium = 2, High = 3. Confidence = reports in the cell ÷ 5, up to 1.", { size: 19 })], SOFT),
    p(""),
    table(["PRI", "Class"], [["< 25", "Low"], ["25–50", "Moderate"], ["50–75", "High"], ["75 and over", "Very high"]], [2000, 2000]),
    p(""),
    bullet("Filters: problem, period, host plant, cell size."),
    bullet("Tap a cell or area: number of reports, trend against last month, median infestation."),
    bullet("Trend, Export (CSV, GeoJSON, Shapefile) and Alert (notify the agency)."),
  ]),
  h2("Example from real CropProtect data"),
  p("These charts come from the 38,762 anonymized CropProtect records (March 2024 – February 2026). PestLand produces the same views automatically."),
  ...figure("analysis/risk_map_counties.png", 6.9, "Risk map by hexagon cell, three most-surveyed counties"),
  ...figure("analysis/top_problems_by_level.png", 5.6, "Top 12 pest/disease problems by infestation level"),
  ...figure("analysis/weekly_trend.png", 5.6, "Weekly reports during the June–August 2024 campaign"),
  bullet("Fall armyworm was the most reported problem (4,925 reports, over 1,000 of them High)."),
  bullet("1,458 Unknown disease reports had no route to an expert. In PestLand they become Needs ID."),
  bullet("Most reports came from one June–August 2024 campaign; the trend view makes gaps in surveillance visible."),
);

// Click 7
children.push(
  h1("11. Click 7 — AI Lab"),
  screenBlock("screens/08_click7_ai_lab.png", "Click 7", [
    table(["Mode", "Use it for", "Output"], [
      ["Identify", "Any pest, symptom or weed photo", "Top-3 names with confidence"],
      ["Count", "Sticky traps, pheromone traps, berries, leaves", "A box around each object, totals per species"],
      ["% leaf damage", "Leaf or canopy photos", "% area damaged → suggested level"],
      ["Batch", "A set of trap photos from a route", "Counts per trap"],
    ], [1300, 2300, 2200]),
    p(""),
    bullet("The AI runs on the phone (native C++), so it works offline. The model comes with the region pack."),
    bullet("Fix a box: drag, delete or relabel. Corrections train the next model."),
    bullet("Send to expert puts the photo in the expert queue."),
    bullet("Attach count to report adds the count to the current or a new report."),
  ]),
  nextTap(7, "Attach count to report"),
);

// Regions
children.push(
  h1("12. Taking PestLand to another region"),
  p([t("What if I take it to Australia, Guam or PNG? ", { bold: true }), t("Only the region pack changes. Pick the new region, or let GPS pick it, and every list, rule, map and language switches with it.")]),
  ...figure("screens/region_switch_click1.png", 6.9, "The same Click 1 screen under five region packs"),
  ...figure("diagrams/region_pack.png", 6.9, "What a region pack contains"),
  table(["Region pack", "Admin levels", "Units", "Languages", "Example problems", "Report channel"], [
    ["Hawaiʻi", "State › Island › County › District", "acre, °F", "English, ʻŌlelo Hawaiʻi, Ilocano", "Coffee berry borer, coffee leaf rust, coconut rhinoceros beetle, little fire ant, Rapid ʻŌhiʻa Death, miconia", "HDOA Plant Quarantine · 643-PEST"],
    ["Guam", "Territory › Village (19)", "acre, °F", "English, CHamoru", "Coconut rhinoceros beetle, cycad aulacaspis scale, little fire ant", "Guam Dept. of Agriculture (set by admin)"],
    ["USA mainland", "State › County (FIPS)", "acre, °F", "English, Spanish", "Spotted lanternfly, emerald ash borer", "State Dept. of Agriculture + USDA APHIS"],
    ["Australia", "State/Territory › LGA › Locality", "hectare, °C", "English", "Fall armyworm, Queensland fruit fly, Panama TR4; Xylella (exotic watch)", "Exotic Plant Pest Hotline 1800 084 881"],
    ["Papua New Guinea", "Province › District › LLG › Ward", "hectare, °C", "English, Tok Pisin, Hiri Motu", "Cocoa pod borer, coffee berry borer, coconut rhinoceros beetle, fall armyworm", "NAQIA (set by admin)"],
    ["Kenya", "County › Sub-county › Ward", "acre, °C", "English, Kiswahili", "Fall armyworm, Sigatoka, cassava mosaic, MLN", "County plant-protection office"],
  ], [1350, 1850, 900, 1500, 2600, CONTENT - 8200]),
  p(""),
  bullet("The same pest can have a different status in different regions. Coffee berry borer is Established in Hawaiʻi but Regulated in the PNG example pack, so a PNG report triggers an agency notification."),
  bullet("A region without a pack: a region admin builds one in the web console from boundaries, plant and pest lists, severity rules, contacts and translations. A shared global AI model is used until a regional one is trained."),
  bullet("Packs can nest (USA › Hawaiʻi; Australia › Queensland). The app uses the most specific pack that contains your GPS point."),
);

// Field map
children.push(
  h1("13. CropProtect → PestLand field map"),
  p("For teams moving from CropProtect. Every CropProtect field is kept or improved."),
  table(["CropProtect page · field", "PestLand click · field", "Change"], [
    ["Report type pop-up", "1 · What are you reporting?", "Adds Not sure; splits Insect and Disease"],
    ["Location · Lat/Long", "1 · GPS", "Accuracy badge"],
    ["Location · County, Sub-county, Ward", "1 · Admin areas", "Automatic; levels follow the region"],
    ["Location · Village", "1 · Place / farm name", "Same"],
    ["Crop · Crop affected", "2 · Sector + Plant", "Any plant type, picture cards"],
    ["Crop · Variety", "2 · Variety", "Same"],
    ["Crop · Crop stage", "2 · Growth stage", "Filtered per plant"],
    ["Crop · Planting / Initial detection date", "2 · Planted / First seen", "Date logic enforced"],
    ["Crop · Crop age", "2 · Plant age", "Automatic"],
    ["Pest · Pest/Disease", "3 · AI suggestion + confirm", "AI, Needs ID, legal status"],
    ["Pest · Pest stage", "3 · Life stages seen", "Multi-select; each needs a photo"],
    ["Pest · Part affected, Symptoms", "3 · Part affected, Signs & symptoms", "Filtered"],
    ["Pest · Level of infestation", "4 · Count → level", "Count-based, per region rule"],
    ["Photos · Pest/Disease photo", "4 · One photo per stage", "1 photo → one per stage"],
    ["Photos · Damage severity photo", "4 · Close-up + Field view", "Split in two"],
    ["Pest · Control measures, Pesticide", "5 · Control done + product", "Registered product list"],
    ["Weed · Weed, Control, Chemical", "3 + 5 (weed lists)", "One flow instead of two"],
    ["More info · Rainfall, Vegetation", "5 · Context", "Pre-filled, source recorded"],
    ["More info · Yield loss, Additional info", "5 · Yield loss, Notes", "0–100 % enforced"],
    ["Area · Manual / Mapping / Aerial", "5 · Type / Walk / Draw", "One offline map"],
    ["Submit / Pending submissions", "5 · Submit + sync states", "Draft › Ready › Pending › Sent"],
    ["—", "6 · Risk map", "New"],
    ["—", "7 · AI Lab", "New"],
  ], [3500, 3200, CONTENT - 6700]),
);

// Privacy & support
children.push(
  h1("14. Data, privacy & support"),
  screenBlock("screens/12_profile_help.png", "Profile & help", [
    bullet("Reports belong to the programme that runs your region pack. Reviewers in your region see them. Public maps show only hexagon summaries, never individual farms."),
    bullet("Collector names are never published. Exports use pseudonymous IDs such as COL-042."),
    bullet("The CropProtect sample data used in this manual had collector names replaced this way and GPS rounded to about 100 m. It contained no email or phone columns."),
    bullet("Photos keep their GPS and time for audit and are shared only through signed links."),
    p([t("Support: ", { bold: true }), t("open Profile › Help. The support email, phone or hotline and reporting agency shown there are set by your region admin in the region pack.")]),
  ]),
  p(""),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 400 }, children: [t("Great job in mapping!", { bold: true, size: 32, color: GREEN })] }),
);

// Appendix
children.push(
  h1("Appendix — How PestLand is built"),
  p("PERN stack with native C++ modules. Full details are in docs/TECHNICAL_SPEC.md."),
  ...figure("diagrams/architecture.png", 6.9, "PestLand architecture"),
);

// ---------- document ----------
const doc = new Document({
  creator: "PestLand", title: "PestLand App Manual", description: "User manual for the PestLand mobile app",
  styles: {
    default: { document: { run: { font: "Calibri", size: 21, color: "10201A" } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, color: GREEN }, paragraph: { spacing: { before: 120, after: 200 }, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: "1C9A72", space: 4 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 27, bold: true, color: MID }, paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, color: MID }, paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 240 } } } }] },
    { reference: "num", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 260 } } } }] },
  ] },
  features: { updateFields: true },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: 15840 }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [t("PestLand App Manual · ", { size: 16, color: INK2 }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: INK2 })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(ROOT, "docs", "PestLand_User_Manual.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", path.relative(ROOT, out), (buf.length / 1e6).toFixed(1), "MB");
});
