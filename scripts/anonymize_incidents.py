"""Anonymize the CropProtect incident export for use as PestLand seed/demo data.

- Collector names are replaced with stable pseudonymous IDs (COL-001 ...).
- GPS is rounded to 3 decimals (~110 m) so individual farms cannot be pinpointed,
  while keeping enough precision for H3 res-7/8 risk maps.
- Everything else (crop, pest, stage, severity, photo file keys, etc.) is kept.
  The export has no email/phone/contact columns, so nothing of that kind is touched.

Usage: python scripts/anonymize_incidents.py <raw.csv> data/incident_reports_anonymized.csv
"""
import sys
import pandas as pd

src, dst = sys.argv[1], sys.argv[2]
df = pd.read_csv(src, low_memory=False)

names = sorted(df["name"].dropna().str.strip().str.lower().unique())
ids = {n: f"COL-{i + 1:03d}" for i, n in enumerate(names)}
df.insert(0, "collector_id", df["name"].str.strip().str.lower().map(ids))
df = df.drop(columns=["name"])

df["latitude"] = df["latitude"].round(3)
df["longitude"] = df["longitude"].round(3)
df["category"] = df["category"].str.title()  # 'PEST' / 'Pest' -> 'Pest'

df.to_csv(dst, index=False)
print(f"{len(df)} rows, {len(ids)} collectors pseudonymized -> {dst}")
