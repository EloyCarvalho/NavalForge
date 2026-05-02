from navalforge.hull import Hull
from navalforge.variants import generate_variants, evaluate_variants
from navalforge.dashboard import generate_html_dashboard, generate_power_curve_csv

base = Hull(name="Lancha_12m", lwl=12.0, beam=3.20, draft=0.55, cb=0.42, cp=0.65, cwp=0.78, lcb=5.8, lcg=5.8, vcg=1.10, speed_knots=22.0, deadrise_deg=15)
variants = generate_variants(base, [2.9, 3.1, 3.3, 3.5], [0.45, 0.55, 0.65], [16, 20, 24, 28], [12, 15, 18])
df = evaluate_variants(variants)
print(generate_html_dashboard(df, "reports/navalforge_dashboard.html"))
print(generate_power_curve_csv(df, "reports/power_curve.csv"))
