# Build prompt — PestLand v1.0 for store publication

For a first field pilot, use [`MVP_BUILD_PROMPT.md`](MVP_BUILD_PROMPT.md) instead; this prompt is the full release that follows it.

Paste everything below the line into Claude Code (or another coding agent) opened on this repository.

---

You are building **PestLand v1.0**, a plant-health surveillance mobile app, for publication on **Google Play** and the **Apple App Store**, plus the API and web console behind it. This repository already holds the approved design. Build exactly that design; do not redesign it.

## 0. Read first (source of truth)

1. `docs/PestLand_User_Manual.md`: every screen, field and rule. The screens in `docs/images/screens/` are the visual spec.
2. `docs/TECHNICAL_SPEC.md`: stack, sync protocol, AI pipeline, region packs, CropProtect field mapping.
3. `db/schema.sql`: database schema (PostgreSQL + PostGIS + h3-pg).
4. `config/regions/*.json`: region-pack manifests.
5. `design/base.css`: design tokens (colours, radii, type). Port them to the Tailwind/NativeWind theme.
6. `data/incident_reports_anonymized.csv`: 38,762 anonymized CropProtect reports, used as seed and test data.

If these files disagree, the manual wins for user-facing behaviour and the spec wins for technical choices. List every conflict you find in `docs/DECISIONS.md`.

## 1. Product rules (non-negotiable)

- **5 clicks to collect, 2 to analyse.** Click 1 Where & type → 2 Host plant → 3 Identify → 4 Level & stage photos → 5 Action, area & send; then 6 Risk map, 7 AI Lab. One screen per click, one Next tap each, with the progress bar and numbered dot shown in the mockups.
- **Any plant:** field crops, fruit & veg, tree crops, ornamental & nursery, forest & native, turf & pasture. **Any problem:** insect/mite, disease, weed, not sure.
- **Region confinement:** the active region pack drives admin levels, lists, pest status, severity rules, products, AI model, offline map, languages, units and support contacts. No region-specific value may be hard-coded. Adding a region = adding a pack, never a code change.
- **Stage photos:** after the level is set in Click 4, require one photo per life/symptom stage ticked in Click 3, plus a damage close-up and a field view. Next stays disabled until each photo passes the quality check. Enforce the same rule on the server (`incident_missing_stage_photos`).
- **Offline first:** every collection feature works with no network. States: Draft → Ready → Pending sync → Sent → Approved / Rejected / Needs ID. Sync is idempotent (client UUIDs) and photo uploads are resumable.
- **Light:** one map library (MapLibre) with offline PMTiles, opened only in Click 5 › Draw and Click 6. No Google Maps SDK, no Leaflet, no WebView maps. Click 1 shows a static snapshot.
- **AI assists, never decides:** store the AI suggestion and the confirmed answer separately. Never present the output as a diagnosis or a treatment prescription.
- **Privacy:** collector names never appear on public maps or exports (use pseudonymous IDs). Public map endpoints return only H3 cells with n ≥ 3. Support email/phone/hotline come from the region pack and are shown in Profile › Help.

## 2. Stack (use current stable versions; pin them in lockfiles)

- **Monorepo:** pnpm workspaces + Turborepo. `apps/mobile`, `apps/api`, `apps/web`, `packages/shared` (Zod schemas + TS types generated once and used everywhere), `packages/region-packs` (pack builder, validator, signer), `native/cpp` (shared C++).
- **Mobile:** Expo (latest SDK, New Architecture), React Native, TypeScript strict, Expo Router, NativeWind (Tailwind), React Hook Form + Zod, Zustand, SQLite (op-sqlite or expo-sqlite) with an outbox table, `@maplibre/maplibre-react-native` + PMTiles, expo-camera, expo-location (foreground only).
- **Native C++ (JSI / Expo Modules or Nitro Modules):** ONNX Runtime Mobile (or LiteRT) inference + NMS + counting, image quality (blur/exposure), H3 indexing, point-in-polygon against pack boundaries. Shared by Android and iOS; include unit tests (GoogleTest) for the C++.
- **API:** Node 22 LTS, Express 5, OpenAPI 3.1 (generated from Zod), JWT access/refresh, role-based access, tus uploads to S3-compatible storage, BullMQ + Redis workers (risk index, weather enrichment, alerts), Pino logs, rate limiting, Helmet.
- **Database:** PostgreSQL 17 + PostGIS + h3-pg. Turn `db/schema.sql` into versioned migrations (Drizzle or node-pg-migrate) and add row-level security by `region_id`.
- **Web console:** React 19 + Vite + Tailwind v4 + MapLibre GL JS. Review/approve queue, expert ID with box correction, dashboards, exports (CSV, GeoJSON, Shapefile), region-pack editor.
- **Infra:** Docker Compose for local dev (Postgres/PostGIS, Redis, MinIO), GitHub Actions CI, EAS Build/Submit for the stores, Sentry for crashes.

## 3. Launch scope

- **Fully populated packs:** `us-hi` (Hawaiʻi) and `ke` (Kenya, migrated from the CropProtect CSV). Ship `gu`, `au`, `pg` and `us` as valid but thin packs (boundaries + structure). Do **not** invent species lists, thresholds, registered products or hotline numbers: leave clearly marked `TODO(region-admin)` placeholders and list them in `docs/REGION_DATA_NEEDED.md`.
- **AI:** build the full on-device pipeline with a small starter model and a label map. If a pack has no model, Click 3/7 must fall back to "Pick from list / Send to expert" without errors. Put the training/export script in `ml/` (Python, YOLO-family → ONNX int8) and document it; do not claim accuracy numbers you have not measured.
- **Risk index:** PRI = 100 × (mean severity − 1) / 2 × min(1, n/5), severity low=1, medium=2, high=3. Classes <25 / 25–50 / 50–75 / ≥75. Compute in the `risk_cell_30d` view refreshed by a worker.

## 4. Acceptance criteria per click (write an automated test for each)

1. **Where:** GPS + accuracy badge (Good ≤10 m, Fair ≤30 m, Poor >30 m); every admin level auto-filled from pack boundaries offline; boundary-mismatch warning; report type required.
2. **Host plant:** sector + plant from pack; stages filtered per plant; planting ≤ first-seen enforced; age computed; "Other" free text allowed and flagged.
3. **Identify:** top-3 AI suggestion offline; lists filtered to plant × region; pest status badge; agency notification queued for regulated/quarantine/exotic/new_to_region; stages, parts, symptoms multi-select; weed branch uses the same screen.
4. **Level & photos:** sample/affected → % → level from the pack rule; override requires a reason; one slot per ticked stage + close-up + field view; quality check; Next disabled until complete.
5. **Action, area & send:** control multi-select + registered product list; weather auto-fill with source recorded; yield loss 0–100; area by type/walk/draw stored as m²; review card with edit links; submit online or queue offline.
6. **Risk map:** H3 cells coloured by PRI; filters for problem/period/host; cell detail with count, trend, median; export; alert.
7. **AI Lab:** identify, count with boxes, % leaf damage, batch; box editing saved as `detection` rows (`model = 'expert:<id>'`); attach count to a report.

## 5. Store-publication requirements (both stores)

- **Account deletion** inside the app and via a web link; data export on request.
- **Privacy policy + terms** hosted on the web console domain; in-app links; Google Play **Data safety** and Apple **privacy nutrition labels** filled in from what the app actually collects (location, photos, email, diagnostics). Include the iOS privacy manifest.
- **Permissions:** foreground location only, with a clear rationale screen before each OS prompt (camera, location, notifications). No background location.
- **Targets:** meet the current Google Play target-API requirement and current Xcode/iOS SDK requirement at submission time.
- **Accessibility:** screen-reader labels, dynamic type, 44 pt touch targets, colour is never the only signal (icons + labels on severity/status).
- **Localization:** i18n framework wired up; English complete; pack-provided languages load at runtime.
- **Assets:** app icon, adaptive icon, splash, store screenshots (regenerate from `design/render.py` or real device captures), short and full store descriptions, and content rating questionnaire answers in `store/`.
- **Release engineering:** semantic versioning, EAS channels (dev / preview / production), OTA updates for JS-only fixes, Sentry release tracking, a signed-pack verification step on the phone.

## 6. Quality gates (CI must pass before any release build)

- TypeScript strict, ESLint, Prettier; C++ builds + GoogleTest.
- Unit tests (shared schemas, severity rules, PRI, sync reducer); API integration tests against PostGIS in Docker; E2E mobile flows with Maestro, including a full **airplane-mode** report → reconnect → single server record.
- Load test: 1,000 concurrent syncs with photos, with no duplicates.
- Security: dependency audit, OWASP ASVS L1 checklist, no secrets in the repo, signed URLs only, RLS tested per role.
- Seed script loads `data/incident_reports_anonymized.csv` into the Kenya pack and the risk map renders from it.

## 7. How to work

- Work in phases, committing after each one with passing CI: **(1)** monorepo + shared schemas + DB migrations → **(2)** Clicks 1–5 offline + sync → **(3)** API + web review queue → **(4)** region-pack builder + Hawaiʻi/Kenya packs → **(5)** Click 6 risk map → **(6)** C++ AI + Clicks 3/7 → **(7)** store-readiness (section 5) → **(8)** release candidate builds.
- At the end of each phase, report what works, what is stubbed and what data you need from me. Ask before adding any dependency outside the stack above.
- Never fabricate pest data, contacts, legal status or model metrics. When real data is missing, stub it visibly and add it to `docs/REGION_DATA_NEEDED.md`.

**Definition of done:** signed Android App Bundle and iOS build uploaded to internal testing tracks (Play internal testing, TestFlight); the API and web console deployed to a staging URL; all quality gates green; `docs/RELEASE_CHECKLIST.md` completed with anything I must do by hand (store accounts, signing keys, privacy-policy approval, region data).
