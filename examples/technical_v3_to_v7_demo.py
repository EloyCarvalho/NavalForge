from pathlib import Path

from navalforge.interface.core_api import evaluate_from_csv_project
from navalforge.reporting.technical_report import write_technical_report
from navalforge.technical_core import TechnicalCoreResult

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "sections" / "lancha_12m_sections.csv"
REPORT_PATH = ROOT / "reports" / "technical_report_v3_to_v7.md"

result = evaluate_from_csv_project(
    CSV_PATH,
    name="Lancha_12m_v3_to_v7",
    waterline_z=0.55,
    vcg=1.10,
    speed_knots=22.0,
    deadrise_deg=15.0,
)

core = TechnicalCoreResult(**result["core"])
write_technical_report(core, REPORT_PATH)

print("=== NavalForge Technical v3 to v7 Demo ===")
print(f"Status: {result['status']}")
print(f"Displacement: {result['core']['hydrostatics']['displacement_kg']:.1f} kg")
print(f"GMt: {result['core']['stability']['gm_initial_m']:.3f} m")
print(f"Savitsky v1 brake power: {result['savitsky_v1']['brake_power_kw']:.1f} kW")
print(f"GZ max: {result['gz_curve']['max_gz_m']:.3f} m at {result['gz_curve']['angle_at_max_gz_deg']:.1f} deg")
print(f"Report exported to: {REPORT_PATH}")
