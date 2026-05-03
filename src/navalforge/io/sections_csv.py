from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from navalforge.geometry.sections import HullSection, SectionPoint, SectionalHull


def load_sectional_hull_from_csv(
    path: str | Path,
    *,
    name: str = "CSV_Sectional_Hull",
    waterline_z: float,
    vcg: float,
    speed_knots: float,
    deadrise_deg: float = 15.0,
    propulsive_efficiency: float = 0.55,
) -> SectionalHull:
    """Load a symmetric sectional hull from CSV.

    Required columns: x, y, z.
    The file stores one half-section; calculations mirror it about centerline.
    """
    p = Path(path)
    rows_by_x: dict[float, list[SectionPoint]] = defaultdict(list)
    with p.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not {"x", "y", "z"}.issubset(reader.fieldnames):
            raise ValueError("CSV must contain columns: x, y, z")
        for row in reader:
            x = float(row["x"])
            y = float(row["y"])
            z = float(row["z"])
            if y < 0:
                raise ValueError("CSV half-breadth y must be non-negative")
            rows_by_x[x].append(SectionPoint(y=y, z=z))
    hull = SectionalHull(
        name=name,
        sections=tuple(
            HullSection(x=x, points=tuple(sorted(points, key=lambda pt: pt.z)))
            for x, points in sorted(rows_by_x.items())
        ),
        waterline_z=waterline_z,
        vcg=vcg,
        speed_knots=speed_knots,
        deadrise_deg=deadrise_deg,
        propulsive_efficiency=propulsive_efficiency,
        notes=f"Loaded from CSV: {p.name}",
    )
    hull.validate()
    return hull


def write_sectional_hull_to_csv(hull: SectionalHull, path: str | Path) -> Path:
    """Write sectional hull half-breadth points to CSV."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["x", "y", "z"])
        writer.writeheader()
        for sec in hull.ordered_sections():
            for point in sec.sorted_points():
                writer.writerow({"x": sec.x, "y": point.y, "z": point.z})
    return p
