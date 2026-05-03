from __future__ import annotations

from pathlib import Path

from navalforge.technical_core import TechnicalCoreResult


def technical_result_to_markdown(result: TechnicalCoreResult) -> str:
    """Generate a traceable preliminary Markdown report."""
    h = result.hydrostatics
    s = result.stability
    r = result.resistance
    p = result.installed_power
    lines = [
        f"# NavalForge Technical Report — {result.hull_name}",
        "",
        "## Status",
        "Preliminary engineering screening. Not valid as final design documentation.",
        "",
        "## Hydrostatics",
        f"- Displacement: {h['displacement_kg']:.2f} kg",
        f"- Volume: {h['volume_m3']:.3f} m³",
        f"- LCB: {h['lcb_m']:.3f} m",
        f"- KB: {h['kb_m']:.3f} m",
        f"- Waterplane area: {h['waterplane_area_m2']:.3f} m²",
        f"- Cb: {h['cb']:.3f}",
        f"- Cwp: {h['cwp']:.3f}",
        "",
        "## Initial stability",
        f"- GMt: {s['gm_initial_m']:.3f} m",
        f"- Status: {s['status']}",
        "",
        "## Resistance and power",
        f"- Regime: {r['regime']}",
        f"- Total resistance: {r['total_resistance_n']:.2f} N",
        f"- Effective power: {r['effective_power_kw']:.2f} kW",
        f"- Brake power: {r['brake_power_kw']:.2f} kW",
        f"- Installed power: {p['installed_power_kw']:.2f} kW",
        "",
        "## Limitations",
    ]
    for item in result.limitations:
        lines.append(f"- {item}")
    lines += [
        "",
        "## Required validation before engineering use",
        "- Validate geometry from CAD or measured offsets.",
        "- Validate hydrostatics against trusted software or hand checks.",
        "- Validate resistance method against reference data or sea trials.",
        "- Produce complete GZ curves and loading conditions where required.",
    ]
    return "\n".join(lines) + "\n"


def write_technical_report(result: TechnicalCoreResult, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(technical_result_to_markdown(result), encoding="utf-8")
    return p
