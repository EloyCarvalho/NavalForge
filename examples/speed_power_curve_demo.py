from pathlib import Path

from navalforge.io.sections_csv import load_sectional_hull_from_csv
from navalforge.performance.speed_power import speed_power_curve, write_speed_power_csv

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "sections" / "lancha_12m_sections.csv"
OUT_PATH = ROOT / "reports" / "speed_power_curve_v2.csv"

hull = load_sectional_hull_from_csv(
    CSV_PATH,
    name="Lancha_12m_CSV",
    waterline_z=0.55,
    vcg=1.10,
    speed_knots=22.0,
    deadrise_deg=15.0,
)

points = speed_power_curve(hull, speeds_knots=range(6, 35, 2))
write_speed_power_csv(points, OUT_PATH)

print("=== NavalForge Speed-Power Curve v2 ===")
for point in points:
    print(
        f"{point.speed_knots:>4.0f} kn | Fn {point.froude_number:.3f} | "
        f"{point.regime:<18} | R {point.resistance_n:>8.1f} N | "
        f"P_inst {point.installed_power_kw:>7.1f} kW"
    )
print(f"CSV exported to: {OUT_PATH}")
