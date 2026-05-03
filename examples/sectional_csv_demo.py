from pathlib import Path

from navalforge.io.sections_csv import load_sectional_hull_from_csv
from navalforge.technical_core import evaluate_technical_core

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "sections" / "lancha_12m_sections.csv"

hull = load_sectional_hull_from_csv(
    CSV_PATH,
    name="Lancha_12m_CSV",
    waterline_z=0.55,
    vcg=1.10,
    speed_knots=22.0,
    deadrise_deg=15.0,
)

result = evaluate_technical_core(hull)

print("=== NavalForge CSV Sectional Demo ===")
print(f"Hull: {result.hull_name}")
print(f"Displacement: {result.hydrostatics['displacement_kg']:.1f} kg")
print(f"LCB: {result.hydrostatics['lcb_m']:.3f} m")
print(f"KB: {result.hydrostatics['kb_m']:.3f} m")
print(f"GMt: {result.stability['gm_initial_m']:.3f} m")
print(f"Resistance: {result.resistance['total_resistance_n']:.1f} N")
print(f"Brake power: {result.resistance['brake_power_kw']:.1f} kW")
