from navalforge.geometry.sections import create_simple_planing_hull
from navalforge.technical_core import evaluate_technical_core

hull = create_simple_planing_hull(
    name="Lancha_12m_Sectional_Core",
    lwl=12.0,
    beam=3.2,
    draft=0.55,
    vcg=1.10,
    speed_knots=22.0,
    deadrise_deg=15.0,
    stations=13,
)

result = evaluate_technical_core(hull)

print("=== NavalForge Technical Core v1 ===")
print(f"Hull: {result.hull_name}")
print(f"Displacement: {result.hydrostatics['displacement_kg']:.1f} kg")
print(f"LCB: {result.hydrostatics['lcb_m']:.3f} m")
print(f"KB: {result.hydrostatics['kb_m']:.3f} m")
print(f"GMt: {result.stability['gm_initial_m']:.3f} m")
print(f"Regime: {result.resistance['regime']}")
print(f"Resistance: {result.resistance['total_resistance_n']:.1f} N")
print(f"Brake power: {result.resistance['brake_power_kw']:.1f} kW")
print(f"Installed power: {result.installed_power['installed_power_kw']:.1f} kW")
print("Limitations:")
for item in result.limitations:
    print("-", item)
