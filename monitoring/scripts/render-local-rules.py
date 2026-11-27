#!/usr/bin/env python3
"""Render PrometheusRule CRs (monitoring/rules/*.rules.yaml) to plain Prometheus rule files
(monitoring/prometheus/rules/*.rules.yml) for the local compose Prometheus and for promtool.
Use --check to fail when the committed output is stale (CI)."""
import pathlib
import sys

import yaml

root = pathlib.Path(__file__).resolve().parents[1]
out_dir = root / "prometheus" / "rules"
check = "--check" in sys.argv
stale = False
out_dir.mkdir(parents=True, exist_ok=True)
for src in sorted((root / "rules").glob("*.rules.yaml")):
    doc = yaml.safe_load(src.read_text(encoding="utf-8"))
    header = "# GENERATED from monitoring/rules/%s by monitoring/scripts/render-local-rules.py. Do not edit.\n" % src.name
    text = header + yaml.safe_dump({"groups": doc["spec"]["groups"]}, sort_keys=False, width=1000)
    dst = out_dir / (src.name[: -len(".yaml")] + ".yml")
    if check:
        if not dst.exists() or dst.read_text(encoding="utf-8") != text:
            print("stale: %s" % dst)
            stale = True
    else:
        dst.write_text(text, encoding="utf-8", newline="\n")
        print("wrote %s" % dst)
sys.exit(1 if stale else 0)
