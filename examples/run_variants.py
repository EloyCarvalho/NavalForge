from navalforge.hull import Hull
from navalforge.variants import generate_variants, evaluate_variants

base = Hull(name="Lancha_12m", lwl=12.0, beam=3.20, draft=0.55, cb=0.42, cp=0.65, cwp=0.78, lcb=5.8, lcg=5.8, vcg=1.10, speed_knots=22.0, deadrise_deg=15)
variants = generate_variants(base, beam_values=[3.0, 3.2, 3.4], draft_values=[0.45, 0.55, 0.65], speed_values=[18, 22, 26], deadrise_values=[12, 15, 18])
df = evaluate_variants(variants)
df.to_csv("reports/variants.csv", index=False)
print(df.head(12).to_string(index=False))
print("Arquivo gerado: reports/variants.csv")
