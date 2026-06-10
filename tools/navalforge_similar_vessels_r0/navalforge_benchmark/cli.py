from __future__ import annotations

import argparse
import json
from pathlib import Path

from .benchmark import NavalForgeBenchmark
from .models import ProjectTarget


def main() -> None:
    parser = argparse.ArgumentParser(description="NavalForge Similar Vessels R0")
    parser.add_argument("--input", required=True, help="Caminho do .xlsx ou .csv do banco NavalForge")
    parser.add_argument("--sheet", default="Fichas_Reais_v31_v100", help="Nome da aba principal, se usar .xlsx")
    parser.add_argument("--target-json", required=True, help="JSON com dados do projeto-alvo")
    parser.add_argument("--top", type=int, default=20, help="Quantidade de semelhantes")
    parser.add_argument("--out-md", default="relatorio_similar_vessels_r0.md", help="Arquivo Markdown de saída")
    parser.add_argument("--out-json", default="", help="Opcional: relatório completo em JSON")
    args = parser.parse_args()

    with open(args.target_json, encoding="utf-8") as f:
        target = ProjectTarget.from_dict(json.load(f))

    bench = NavalForgeBenchmark.from_file(args.input, sheet_name=args.sheet)
    report = bench.benchmark_report(target, n=args.top)

    out_md = Path(args.out_md)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(bench.report_to_markdown(report), encoding="utf-8")

    if args.out_json:
        out_json = Path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Relatório gerado: {out_md}")
    if args.out_json:
        print(f"JSON gerado: {args.out_json}")


if __name__ == "__main__":
    main()
