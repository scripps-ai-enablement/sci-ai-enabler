#!/usr/bin/env python3
"""Map fiber/probe tip pixels into atlas space and report the subregion + margin.

This is the reference *artifact* for the recipe "Localize a fiber/probe implant
tip in an Allen CCF subregion from 2D histology". The durable record of an
analysis is code, not a chat transcript: an assistant may have authored this
file, but what you commit, cite and re-run is the script, its pinned environment
(requirements.txt) and the provenance record it emits.

Two modes:

  --offline           Replay against `fixtures/` — a tiny synthetic atlas and a
                      QuickNII-format alignment. Pure standard library, no
                      network, no atlas download, fully deterministic. This is
                      the path the test suite exercises and the path that proves
                      the coordinate arithmetic is right.

  (default, live)     Read a real DeepSlice alignment and the real
                      `allen_mouse_25um` atlas via PyNutil + brainglobe-atlasapi,
                      exactly as the recipe describes. Needs
                      `pip install -r requirements.txt`.

THE ARITHMETIC THAT MATTERS. QuickNII/DeepSlice anchoring is a 9-vector
[ox,oy,oz, ux,uy,uz, vx,vy,vz]: an origin plus the two in-plane vectors. A pixel
(x, y) in a section of size (width, height) maps to atlas space as

    atlas_coord = O + (x / width) * U + (y / height) * V

Note the division is by `width`/`height`, NOT width-1 — this matches the
canonical implementation in PyNutil (`transform_to_atlas_space`,
PyNutil/processing/atlas_map.py). Getting this wrong yields coordinates that
look plausible and are wrong, which is the failure mode this recipe exists to
avoid, so `--offline` checks it against a fixture whose answer is known by hand.

In live mode, prefer PyNutil's own `read_alignment` + `xy_to_coords` over
re-deriving this; the formula is reproduced here so the offline replay needs no
third-party package, not to encourage hand-rolling it.

Axis order follows BrainGlobe's orientation string: `allen_mouse_25um` is "asr",
i.e. axis 0 = anterior (AP), axis 1 = superior→inferior (DV), axis 2 = →right
(ML). Read `atlas.orientation` rather than assuming it for another atlas.

Determinism contract (offline): given the same tips, fixtures and target, every
output byte is identical across runs and machines. No wall-clock value reaches
the outputs — the run date is explicit via --run-date.

Usage:
    python localize_tips.py --offline --tips tips.csv --target TGT \\
        --outdir results/demo

    python localize_tips.py --alignment out/alignment.json \\
        --atlas allen_mouse_25um --tips tips.csv --target CA1 --outdir results/run
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"

# Below this margin the placement is reported `marginal` rather than a clean
# verdict: a single 2D section inherits AP uncertainty from the plane prediction,
# so a tip sitting closer than that to a boundary cannot be called confidently.
DEFAULT_AP_ERROR_UM = 25.0


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# the transform
# --------------------------------------------------------------------------- #

def pixel_to_atlas(anchoring: list[float], width: int, height: int,
                   x: float, y: float) -> tuple[float, float, float]:
    """atlas_coord = O + (x/width)*U + (y/height)*V — see the module docstring."""
    if width <= 0 or height <= 0:
        raise ValueError(f"section width/height must be positive, got {width}x{height}")
    if len(anchoring) != 9:
        raise ValueError(f"anchoring must be 9 values, got {len(anchoring)}")
    o, u, v = anchoring[0:3], anchoring[3:6], anchoring[6:9]
    fx, fy = x / width, y / height
    return tuple(o[i] + fx * u[i] + fy * v[i] for i in range(3))


def margin_to_boundary_um(annotation, shape, resolution_um, coord, structure_id):
    """Shortest distance from `coord` to any voxel of a different structure.

    Brute force over the volume. That is fine for the synthetic fixture and is
    deliberately the simplest correct thing; the live path should use a distance
    transform on the real atlas rather than this loop.
    """
    best = math.inf
    for ap in range(shape[0]):
        for dv in range(shape[1]):
            for ml in range(shape[2]):
                if annotation[ap][dv][ml] == structure_id:
                    continue
                d = math.dist(coord, (ap, dv, ml))
                if d < best:
                    best = d
    if best is math.inf:
        return None  # single-structure volume: no boundary exists
    return best * float(resolution_um[0])


# --------------------------------------------------------------------------- #
# atlas access
# --------------------------------------------------------------------------- #

class OfflineAtlas:
    """The synthetic fixture atlas, standing in for a BrainGlobeAtlas."""

    def __init__(self, path: Path):
        d = json.loads(path.read_text(encoding="utf-8"))
        self.name = d["name"]
        self.orientation = d["orientation"]
        self.resolution = d["resolution_um"]
        self.shape = tuple(d["shape"])
        self.annotation = d["annotation"]
        self.labels = {int(k): v for k, v in d["labels"].items()}
        self.version = "fixture"

    def structure_at(self, coord):
        idx = [int(math.floor(c)) for c in coord]
        if any(i < 0 or i >= self.shape[a] for a, i in enumerate(idx)):
            return 0, "Outside atlas", []
        sid = self.annotation[idx[0]][idx[1]][idx[2]]
        meta = self.labels.get(sid)
        if not meta:
            return sid, "Outside atlas", []
        return sid, meta["acronym"], meta["ancestors"]


def load_live_atlas(name: str):
    try:
        from brainglobe_atlasapi import BrainGlobeAtlas
    except ImportError:
        sys.exit("brainglobe-atlasapi is not installed. Either "
                 "`pip install -r requirements.txt` for the live run, or pass "
                 "--offline to replay the fixtures.")
    return BrainGlobeAtlas(name)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #

def read_alignment(path: Path) -> dict[int, dict]:
    """Section number -> {width, height, anchoring} from a QuickNII/DeepSlice JSON."""
    d = json.loads(path.read_text(encoding="utf-8"))
    slices = d.get("slices") or d.get("sections") or []
    out = {}
    for s in slices:
        anchoring = s.get("anchoring") or s.get("ouv")
        if not anchoring:
            continue
        out[int(s["nr"])] = {
            "filename": s.get("filename", ""),
            "width": int(s["width"]),
            "height": int(s["height"]),
            "anchoring": [float(v) for v in anchoring],
        }
    if not out:
        sys.exit(f"{path}: no sections with an anchoring vector")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--offline", action="store_true",
                    help="replay the synthetic fixtures; no network, no atlas download")
    ap.add_argument("--alignment", type=Path, help="DeepSlice/QuickNII JSON (live mode)")
    ap.add_argument("--atlas", default="allen_mouse_25um", help="BrainGlobe atlas name")
    ap.add_argument("--tips", type=Path, default=HERE / "tips.csv",
                    help="CSV: section,x_px,y_px")
    ap.add_argument("--target", required=True, help="intended target acronym")
    ap.add_argument("--ap-error-um", type=float, default=DEFAULT_AP_ERROR_UM,
                    help="margins below this are reported `marginal`")
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--run-date", default=None,
                    help="explicit analysis date; omitted keeps outputs wall-clock-free")
    args = ap.parse_args(argv)

    if args.offline:
        alignment_path = FIXTURES / "alignment.json"
        atlas = OfflineAtlas(FIXTURES / "mini_atlas.json")
        atlas_label = f"{atlas.name} (synthetic fixture)"
    else:
        if not args.alignment:
            ap.error("live mode needs --alignment (or pass --offline)")
        alignment_path = args.alignment
        atlas = load_live_atlas(args.atlas)
        atlas_label = args.atlas

    sections = read_alignment(alignment_path)

    rows = []
    with args.tips.open(encoding="utf-8") as fh:
        for rec in csv.DictReader(fh):
            nr = int(rec["section"])
            sec = sections.get(nr)
            if sec is None:
                sys.exit(f"tips.csv references section {nr}, absent from {alignment_path}")
            x, y = float(rec["x_px"]), float(rec["y_px"])
            coord = pixel_to_atlas(sec["anchoring"], sec["width"], sec["height"], x, y)

            if args.offline:
                sid, acronym, ancestors = atlas.structure_at(coord)
                margin = margin_to_boundary_um(atlas.annotation, atlas.shape,
                                               atlas.resolution, coord, sid)
            else:
                acronym = atlas.structure_from_coords(
                    [int(c) for c in coord], as_acronym=True,
                    key_error_string="Outside atlas")
                sid = atlas.structure_from_coords([int(c) for c in coord],
                                                  key_error_string=0)
                ancestors = (atlas.get_structure_ancestors(acronym)
                             if acronym != "Outside atlas" else [])
                margin = None  # live: use a distance transform, not the brute loop

            in_target = acronym == args.target or args.target in ancestors
            if margin is not None and margin < args.ap_error_um:
                verdict = "marginal"
            else:
                verdict = "hit" if in_target else "miss"

            rows.append({
                "section": nr,
                "x_px": rec["x_px"],
                "y_px": rec["y_px"],
                "ap": f"{coord[0]:.4f}",
                "dv": f"{coord[1]:.4f}",
                "ml": f"{coord[2]:.4f}",
                "structure_id": sid,
                "acronym": acronym,
                "ancestors": "|".join(ancestors),
                "margin_um": "" if margin is None else f"{margin:.2f}",
                "target": args.target,
                "verdict": verdict,
            })

    args.outdir.mkdir(parents=True, exist_ok=True)
    placements = args.outdir / "placements.csv"
    with placements.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    provenance = {
        "analysis": "implant-tip-localization",
        "recipe": "recipes/items/localize-implant-tip-in-brain-atlas-subregion.md",
        "mode": "offline-fixture" if args.offline else "live",
        "atlas": atlas_label,
        "atlas_orientation": atlas.orientation,
        "atlas_resolution_um": list(atlas.resolution),
        "transform": "atlas = O + (x/width)*U + (y/height)*V  [QuickNII anchoring]",
        "transform_reference": (
            "PyNutil transform_to_atlas_space, PyNutil/processing/atlas_map.py"),
        "ap_error_um": args.ap_error_um,
        "inputs": {
            "tips_csv_sha256": sha256_file(args.tips),
            "alignment_sha256": sha256_file(alignment_path),
            "tip_count": len(rows),
        },
        "outputs": {"placements.csv_sha256": sha256_file(placements)},
        "verdict_counts": {
            v: sum(1 for r in rows if r["verdict"] == v)
            for v in sorted({r["verdict"] for r in rows})
        },
    }
    if args.offline:
        provenance["inputs"]["atlas_sha256"] = sha256_file(FIXTURES / "mini_atlas.json")
    if args.run_date:
        provenance["run_date"] = args.run_date

    (args.outdir / "provenance.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for r in rows:
        print(f"  section {r['section']} ({r['x_px']},{r['y_px']}) -> "
              f"{r['acronym']} margin={r['margin_um'] or 'n/a'}um : {r['verdict']}")
    print(f"Wrote {placements} and {args.outdir / 'provenance.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
