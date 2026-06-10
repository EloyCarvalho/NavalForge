from navalforge_benchmark import NavalForgeBenchmark, ProjectTarget

# Ajuste este caminho para apontar para o CSV ou XLSX do Banco NavalForge.
banco = "data/navalforge_embarcacoes_semelhantes_r0.csv"

target = ProjectTarget(
    nome="DGS/FRB 8,5 m - exemplo",
    loa_m=8.50,
    b_m=2.80,
    grupo_navalforge="RIB / Inflável rígido",
    material_normalizado="RIB/GRP+tubo",
    propulsao_normalizada="motor de popa",
    regime_principal="Planante",
)

bench = NavalForgeBenchmark.from_file(banco)
report = bench.benchmark_report(target, n=20)

print(bench.report_to_markdown(report))
