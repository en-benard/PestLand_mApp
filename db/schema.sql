-- PestLand core schema - PostgreSQL 17 + PostGIS 3.5 (+ h3-pg for hex risk maps)
-- Every CropProtect export column has a home here; see docs/TECHNICAL_SPEC.md §5 for the mapping.

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS h3;
CREATE EXTENSION IF NOT EXISTS h3_postgis CASCADE;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ---------- region packs ----------
CREATE TABLE region (
  id            text PRIMARY KEY,                 -- 'us-hi', 'gu', 'au', 'pg', 'ke'
  name          text NOT NULL,
  pack_version  text NOT NULL,                    -- '2026.09'
  manifest      jsonb NOT NULL,                   -- config/regions/<id>.json
  footprint     geometry(MultiPolygon, 4326)
);

CREATE TABLE admin_area (
  id         bigserial PRIMARY KEY,
  region_id  text NOT NULL REFERENCES region(id),
  level      smallint NOT NULL,                   -- 1 = state/county ... n = ward/district
  level_name text NOT NULL,                       -- 'island', 'LGA', 'LLG', 'ward'
  code       text,
  name       text NOT NULL,
  parent_id  bigint REFERENCES admin_area(id),
  geom       geometry(MultiPolygon, 4326) NOT NULL
);
CREATE INDEX ON admin_area USING gist (geom);

-- ---------- reference lists (filtered per region) ----------
CREATE TABLE host_plant (
  id         text PRIMARY KEY,                    -- 'coffea_arabica'
  common     jsonb NOT NULL,                      -- {"en":"Coffee","haw":"Kope"}
  scientific text,
  sector     text NOT NULL CHECK (sector IN ('field_crops','fruit_veg','tree_crops','ornamental_nursery','forest_native','turf_pasture')),
  lifecycle  text CHECK (lifecycle IN ('annual','perennial','biennial')),
  stages     text[] NOT NULL
);

CREATE TABLE problem (                              -- pests, diseases, weeds
  id         text PRIMARY KEY,
  common     jsonb NOT NULL,
  scientific text,
  kind       text NOT NULL CHECK (kind IN ('insect','mite','disease','weed','nematode','mollusc','vertebrate','unknown')),
  stages     text[] NOT NULL                      -- egg, larva, pupa, adult | early, advancing, late
);

CREATE TABLE region_problem (                       -- status + severity rule differ per region and host
  region_id  text REFERENCES region(id),
  problem_id text REFERENCES problem(id),
  host_id    text REFERENCES host_plant(id),
  status     text NOT NULL CHECK (status IN ('established','regulated','quarantine','exotic','new_to_region')),
  severity   jsonb,                               -- {"method":"berries_bored_per_100","thresholds":{...}}
  PRIMARY KEY (region_id, problem_id, host_id)
);

-- ---------- users ----------
CREATE TABLE app_user (
  id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email     text UNIQUE NOT NULL,
  phone     text,
  role      text NOT NULL CHECK (role IN ('collector','expert','reviewer','region_admin','super_admin')),
  region_id text REFERENCES region(id)
);

-- ---------- incidents (one per 5-click report) ----------
CREATE TABLE incident (
  id               uuid PRIMARY KEY,               -- generated on the phone -> idempotent sync
  region_id        text NOT NULL REFERENCES region(id),
  pack_version     text NOT NULL,
  collector_id     uuid REFERENCES app_user(id),
  state            text NOT NULL DEFAULT 'submitted'
                   CHECK (state IN ('draft','ready','pending_sync','submitted','approved','rejected','needs_id')),
  -- Click 1
  geom             geometry(Point, 4326) NOT NULL,
  gps_accuracy_m   real,
  admin_path       bigint[] NOT NULL,              -- admin_area ids, top -> bottom
  place_name       text,
  boundary_ok      boolean,
  report_type      text NOT NULL CHECK (report_type IN ('insect','disease','weed','unknown')),
  -- Click 2
  host_id          text REFERENCES host_plant(id),
  host_other       text,
  variety          text,
  host_stage       text,
  planting_date    date,
  detection_date   date,
  CHECK (planting_date IS NULL OR detection_date IS NULL OR planting_date <= detection_date),
  -- Click 3
  problem_id       text REFERENCES problem(id),
  ai_suggestion    jsonb,                          -- [{"id":..,"p":0.94}, ...] + model version
  id_method        text CHECK (id_method IN ('confirmed_ai','picked','expert','unknown')),
  stages_seen      text[] NOT NULL DEFAULT '{}',
  parts_affected   text[] NOT NULL DEFAULT '{}',
  symptoms         text[] NOT NULL DEFAULT '{}',
  -- Click 4
  sample_size      integer,
  sample_positive  integer,
  infestation_pct  real CHECK (infestation_pct BETWEEN 0 AND 100),
  level            text CHECK (level IN ('low','medium','high')),
  level_override   text,                           -- reason when user overrides the computed level
  -- Click 5
  control_measures text[] NOT NULL DEFAULT '{}',   -- cultural, physical_mechanical, biological, chemical, none
  products         text[] NOT NULL DEFAULT '{}',
  rain_7d_mm       real,
  rain_source      text CHECK (rain_source IN ('farmer','observed','weather_api')),
  vegetation       text CHECK (vegetation IN ('green','greening','drying','dry')),
  yield_loss_pct   real CHECK (yield_loss_pct BETWEEN 0 AND 100),
  area_m2          real,                           -- one internal unit; UI converts to acre/ha
  area_method      text CHECK (area_method IN ('typed','walked','drawn')),
  area_geom        geometry(Polygon, 4326),
  notes            text,
  created_at       timestamptz NOT NULL,           -- phone time
  received_at      timestamptz NOT NULL DEFAULT now(),
  h3_r7            h3index GENERATED ALWAYS AS (h3_lat_lng_to_cell(geom::point, 7)) STORED
);
CREATE INDEX ON incident USING gist (geom);
CREATE INDEX ON incident (region_id, problem_id, created_at);
CREATE INDEX ON incident (h3_r7);

CREATE TABLE photo (
  id          uuid PRIMARY KEY,
  incident_id uuid NOT NULL REFERENCES incident(id) ON DELETE CASCADE,
  kind        text NOT NULL CHECK (kind IN ('stage','damage_closeup','field_view','trap','other')),
  stage       text,                                 -- required when kind = 'stage'
  object_key  text NOT NULL,                        -- S3 key
  sha256      text NOT NULL,
  quality     jsonb,                                -- {"blur":0.08,"exposure":"ok"}
  taken_at    timestamptz,
  geom        geometry(Point, 4326),
  CHECK (kind <> 'stage' OR stage IS NOT NULL)
);

CREATE TABLE detection (                            -- AI Lab boxes (Click 7) + expert corrections
  id          bigserial PRIMARY KEY,
  photo_id    uuid NOT NULL REFERENCES photo(id) ON DELETE CASCADE,
  problem_id  text REFERENCES problem(id),
  stage       text,
  bbox        real[4] NOT NULL,                     -- x, y, w, h (0-1)
  confidence  real,
  model       text NOT NULL,                        -- 'us-hi-det-v3' or 'expert:<user id>'
  created_at  timestamptz NOT NULL DEFAULT now()
);

-- Rule: every stage ticked in Click 3 has at least one stage photo (enforced on the phone, re-checked here).
CREATE VIEW incident_missing_stage_photos AS
SELECT i.id, s.stage
FROM incident i CROSS JOIN LATERAL unnest(i.stages_seen) AS s(stage)
WHERE NOT EXISTS (SELECT 1 FROM photo p WHERE p.incident_id = i.id AND p.kind = 'stage' AND p.stage = s.stage);

-- ---------- Click 6: PestLand Risk Index per H3 cell ----------
-- PRI = 100 * (mean severity - 1) / 2 * min(1, n / 5), severity low=1 medium=2 high=3
CREATE MATERIALIZED VIEW risk_cell_30d AS
SELECT region_id, problem_id, h3_r7 AS cell,
       count(*) AS n,
       round((100 * (avg(CASE level WHEN 'low' THEN 1 WHEN 'medium' THEN 2 WHEN 'high' THEN 3 END) - 1) / 2
              * least(1, count(*) / 5.0))::numeric, 1) AS pri
FROM incident
WHERE level IS NOT NULL AND created_at > now() - interval '30 days' AND state IN ('submitted','approved')
GROUP BY 1, 2, 3;
CREATE INDEX ON risk_cell_30d (region_id, problem_id);
