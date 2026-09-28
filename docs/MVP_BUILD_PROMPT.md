# Build prompt — PestLand MVP (field pilot)

The MVP is the smallest build that puts real phones in real fields: collectors file 5-click reports offline with a photo for every stage, reports sync once and only once, the region switch works between two regions, and the office sees a risk map and a review queue.
Everything else in [`BUILD_PROMPT.md`](BUILD_PROMPT.md) (the full v1.0) comes after the pilot.

Paste everything below the line into Claude Code opened on this repository.

---

You are building the **PestLand MVP**: an offline-first plant-health reporting app for a field pilot, distributed through **Google Play internal testing** and **TestFlight** (not public store listings yet). This repository holds the approved design; build that design, cut to the scope below.

## 0. Read first

- `docs/PestLand_User_Manual.md` and `docs/images/screens/*.png`: screens and fields (the visual spec).
- `docs/TECHNICAL_SPEC.md`: the full-version architecture. **This prompt overrides it wherever they differ.**
- `db/schema.sql`: starting schema (see section 3 for MVP changes).
- `config/regions/ke.json`, `config/regions/us-hi.json`: the two MVP region packs.
- `data/incident_reports_anonymized.csv`: real CropProtect data (Kenya).
- `design/base.css`: colour and spacing tokens for the Tailwind theme.

## 1. MVP scope

**In:**
1. Sign-in (email + password; accounts created by an admin, so there is no public sign-up) and region-pack selection, with GPS auto-suggesting the pack.
2. **Clicks 1–5** exactly as in the manual, fully offline:
   - Click 1: GPS + accuracy badge; admin levels auto-filled by point-in-polygon on the pack's GeoJSON; mismatch warning; report type (Insect / Disease / Weed / Not sure).
   - Click 2: sector, plant, variety, stage (filtered per plant), dates with planting ≤ first-seen, age computed.
   - Click 3: pick problem from the list filtered to plant × region (search + "Not sure / Send to expert"); status badge; stages, parts and symptoms multi-select. Weeds use the same screen.
   - Click 4: sample count → % → level from the pack rule (manual level with a reason as fallback); **one photo per ticked stage + close-up + field view, Next disabled until all are taken**; basic blur check.
   - Click 5: control measures + product (free text for the MVP), rain (typed, with source), vegetation, yield loss 0–100, area **by typing or walking the edge (GPS track)**, review card, Submit.
3. **Outbox and sync:** Draft → Ready → Pending → Sent → Approved / Rejected / Needs ID; client UUIDs; idempotent `POST /incidents`; one pre-signed upload per photo with retry; incident marked `submitted` only when all photos have arrived.
4. **Click 6 Risk map (online):** H3 hex cells (resolution 7) coloured by PRI; filters for problem and last 30/90 days; cell detail (count, median %, trend arrow); CSV export.
5. **Click 7 AI Lab, reduced:** see section 4.
6. **Web console (minimal):** sign-in, report list with filters, report detail with photos, approve / reject / set problem for *Needs ID*, CSV export, and the same risk map.
7. **Two region packs, to prove the region switch:**
   - **Kenya (`ke`), fully populated from real data.** Generate the host, problem, stage, part and symptom lists and the county/sub-county/ward names from `data/incident_reports_anonymized.csv` (37 crops, 133 problems, 21 parts, 16 symptoms). Get Kenya ward boundaries from an openly licensed source and record the source and licence. Seed the database with the CSV so the risk map has data on day one.
   - **Hawaiʻi (`us-hi`), starter pack:** State › Island › County › District boundaries from US Census/State GIS open data; a starter host and problem list limited to the examples already named in `config/regions/us-hi.json`, each marked `verified: false` until I confirm it. Do not add species, thresholds, products or phone numbers that are not already in the repo.
8. **Profile & Help:** role, active pack, units, and the support email/phone taken from the pack (placeholders until I supply them), plus **delete my account** (needed later for the stores; cheap now).

**Out (post-pilot, do not build):** custom C++ modules, offline map tiles and the *Draw* area mode, on-device counting, weather auto-fill, BullMQ/Redis workers, tus resumable uploads, a region-pack editor or signer, Guam/Australia/PNG/US packs beyond their existing JSON, translations (English only, but route all strings through i18n), SMS fallback, alerts to agencies, load testing, and public store listings.

## 2. Stack (MVP)

- **One repo, three apps:** pnpm workspaces: `apps/mobile`, `apps/api`, `apps/web`, `packages/shared` (Zod schemas + types used by all three). No Turborepo until it is needed.
- **Mobile:** Expo (latest stable SDK, development builds via EAS), TypeScript strict, Expo Router, NativeWind, React Hook Form + Zod, Zustand, `expo-sqlite` (outbox), `expo-location` (foreground only), `expo-camera`, `h3-js`, `@turf/boolean-point-in-polygon`. **No custom native code.**
- **AI on the phone:** `react-native-fast-tflite` (its C++ runs through JSI, so the app needs no C++ of its own). This covers the brief's C++ requirement for the MVP.
- **Maps:** `@maplibre/maplibre-react-native` on the web console map and Click 6 only, with an online vector style; there are no maps in Clicks 1–5 (Click 1 shows coordinates and a small static image).
- **API:** Node 22 LTS, Express 5, Zod validation, OpenAPI generated from the shared schemas, JWT, `pg` + migrations (node-pg-migrate or Drizzle), S3-compatible storage with pre-signed URLs, Pino logs, rate limiting.
- **Database:** PostgreSQL 16+ with **PostGIS only**. Compute the H3 cell on the phone/API with `h3-js` and store it as text, so the database runs on any managed Postgres that offers PostGIS. Refresh the risk view on a timer inside the API (every 10 minutes).
- **Web:** React + Vite + Tailwind + MapLibre GL JS.
- **Hosting:** pick the cheapest option that gives managed Postgres with PostGIS, object storage and one container for the API and web console. Document it in `docs/DEPLOY.md`. Docker Compose for local development.

## 3. Schema changes from `db/schema.sql`

Drop the `h3`/`h3_postgis` extensions and replace `h3_r7 h3index GENERATED ...` with `h3_r7 text NOT NULL`. Add `verified boolean` to `host_plant`, `problem` and `region_problem`. Keep every other constraint, including the stage-photo view, and write the risk view against the text column.

## 4. AI in the MVP (read carefully)

- **If I provide the CropProtect photo archive** at `data/photos/` (file names match the `pest_photo` / `damage_photo` columns in the CSV): train an **image classifier** in `ml/` (Python, a small MobileNet/EfficientNet-class model, TFLite int8) for the Kenya problems with ≥ 300 photos (currently 23), plus an "other" class. Split train/validation/test **by collector and date**, not at random, and report real top-1/top-3 accuracy per class in `ml/REPORT.md`. Ship the model only if top-3 accuracy is ≥ 80 % on the test split; in the app, show suggestions only above a confidence threshold you choose from the validation set.
- **If the archive is not provided:** build the Click 3 "Snap to identify" UI and the model-loading path, ship with the model disabled, and make "Pick from list" the default. Do not ship a model trained on made-up or scraped data.
- **Click 7 in the MVP:** *Identify* (same classifier) and **tap-to-count** (the user taps each insect on a photo; the app numbers the taps and stores the points as `detection` rows with `model = 'manual'`). These taps become training labels for the post-pilot automatic counter. Hide *% leaf damage* and *Batch*.
- Always store the AI suggestion (`ai_suggestion`, with the model version) separately from the confirmed problem.

## 5. Acceptance tests (automate each)

1. A complete report in **airplane mode**, app killed and reopened, then reconnect → exactly **one** incident with all photos on the server.
2. Submitting twice (double tap, flaky network) → one incident.
3. Ticking Egg + Adult in Click 3 → Click 4 demands exactly those two stage photos + close-up + field view; the server rejects an incident missing any of them.
4. A GPS point in Kakamega with Nyeri selected → mismatch warning; the choice made is stored with `boundary_ok = false`.
5. Switching the pack from Kenya to Hawaiʻi changes the admin levels, plant list, units (acre/°F) and support contact with no app update.
6. After seeding the CSV, the risk map for fall armyworm shows cells, and PRI values match a SQL check on the same data.
7. A *Needs ID* report appears in the web console queue; setting the problem there updates the phone's copy after the next sync.
8. Planting date after first-seen date and yield loss over 100 are both blocked.

Testing tools: Vitest for shared logic and the API (against PostGIS in Docker), Maestro for the mobile flows above, and one GitHub Actions workflow running lint, type-check and tests on every push.

## 6. Order of work (stop and report after each step)

1. Repo, shared Zod schemas, migrations, Kenya pack generated from the CSV, seed script.
2. Clicks 1–5 with the offline outbox; tests 3, 4 and 8.
3. API + photo upload + sync; tests 1, 2 and 7 (console queue stubbed).
4. Web console + Click 6 risk map; test 6.
5. Hawaiʻi starter pack + pack switching + Profile & Help; test 5.
6. AI per section 4; Click 7 tap-to-count.
7. Pilot builds: EAS internal distribution (Play internal testing + TestFlight), staging deployment, `docs/PILOT_CHECKLIST.md`.

After each step, report what works, what is stubbed and what you need from me. Ask before adding any dependency not listed above.

## 7. Ground rules

- Don't invent pest data, legal status, thresholds, products, contacts or model accuracy. Stub missing items visibly and list them in `docs/REGION_DATA_NEEDED.md`.
- No region-specific value in code: everything comes from the pack.
- Collector names never leave the server; exports use `COL-###` IDs.
- Keep the screens as simple as the mockups: one Next per click and no extra screens.

**Definition of done:** internal-testing builds installed on at least one Android and one iOS device; all 8 acceptance tests green in CI; the API and web console live at a staging URL; `docs/PILOT_CHECKLIST.md` lists what I must do before the pilot (accounts, contacts, Hawaiʻi list confirmation, photo archive).

**Pilot success measures to instrument:** reports per collector per day, median time from Click 1 to Submit (target under 3 minutes), share of reports synced within 24 h, share of reports with every stage photo, and — if the model ships — how often collectors accept the AI's top suggestion.
