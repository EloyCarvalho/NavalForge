from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from navalforge.visualization.dashboard import (
    export_html_to_png,
    generate_speed_sweep_dashboard,
    generate_speed_sweep_svg,
)


def _fix_svg_canvas_height(svg_path: str, bottom_padding_px: int = 60) -> None:
    """Ajusta a altura do SVG para evitar corte do conteúdo renderizado.

    O dashboard SVG possui elementos posicionados manualmente. Quando a tabela
    tem muitas linhas, alguns elementos podem passar da altura fixa original.
    Esta função calcula o maior valor de `y` encontrado e atualiza `height` e
    `viewBox` do SVG automaticamente.
    """
    path = Path(svg_path)
    if not path.exists():
        return

    svg = path.read_text(encoding="utf-8")
    y_values = [float(match) for match in re.findall(r"\by=['\"]([0-9]+(?:\.[0-9]+)?)['\"]", svg)]
    y_values += [float(match) for match in re.findall(r"\by=\"([0-9]+(?:\.[0-9]+)?)\"", svg)]

    if not y_values:
        return

    required_height = int(max(y_values) + bottom_padding_px)
    current_height_match = re.search(r"<svg[^>]*\bheight=\"([0-9]+)\"", svg)
    current_height = int(current_height_match.group(1)) if current_height_match else 0
    new_height = max(current_height, required_height)

    svg = re.sub(r"height=\"[0-9]+\"", f"height=\"{new_height}\"", svg, count=1)
    svg = re.sub(
        r"viewBox=\"0 0 ([0-9]+) [0-9]+\"",
        rf"viewBox=\"0 0 \1 {new_height}\"",
        svg,
        count=1,
    )
    path.write_text(svg, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gera dashboard local do NavalForge")
    parser.add_argument("--length", type=float, default=8.0)
    parser.add_argument("--beam", type=float, default=2.6)
    parser.add_argument("--speed", type=float, default=28.0)
    parser.add_argument("--passengers", type=int, default=6)
    parser.add_argument("--fuel", type=float, default=300.0)
    parser.add_argument("--material", type=str, default="fiberglass")
    parser.add_argument("--speed-start", type=float, default=18.0)
    parser.add_argument("--speed-end", type=float, default=36.0)
    parser.add_argument("--speed-step", type=float, default=2.0)
    parser.add_argument("--output", type=str, default="reports/navalforge_dashboard.svg")
    parser.add_argument("--html-output", type=str, default="reports/navalforge_dashboard.html")
    parser.add_argument(
        "--export-svg",
        action="store_true",
        help="Compatibilidade: o SVG já é gerado por padrão.",
    )
    parser.add_argument("--export-png", action="store_true")
    parser.add_argument("--export-html", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    output_path = generate_speed_sweep_svg(
        output_path=args.output,
        length_m=args.length,
        beam_m=args.beam,
        target_speed_knots=args.speed,
        passengers=args.passengers,
        fuel_capacity_l=args.fuel,
        material=args.material,
        speed_start_knots=args.speed_start,
        speed_end_knots=args.speed_end,
        speed_step_knots=args.speed_step,
    )
    _fix_svg_canvas_height(output_path)

    print("Dashboard SVG criado em:")
    print(output_path)
    print()
    print("Para abrir: use um navegador ou editor vetorial compatível com SVG.")

    if args.export_png:
        png_path = "reports/navalforge_dashboard.png"
        html_path = generate_speed_sweep_dashboard(
            output_path=args.html_output,
            length_m=args.length,
            beam_m=args.beam,
            target_speed_knots=args.speed,
            passengers=args.passengers,
            fuel_capacity_l=args.fuel,
            material=args.material,
            speed_start_knots=args.speed_start,
            speed_end_knots=args.speed_end,
            speed_step_knots=args.speed_step,
        )
        if export_html_to_png(html_path, png_path):
            print()
            print("Imagem PNG criada em:")
            print(png_path)
        else:
            print()
            print("Falha ao exportar PNG (Playwright pode não estar instalado neste ambiente).")

    if args.export_html:
        html_path = generate_speed_sweep_dashboard(
            output_path=args.html_output,
            length_m=args.length,
            beam_m=args.beam,
            target_speed_knots=args.speed,
            passengers=args.passengers,
            fuel_capacity_l=args.fuel,
            material=args.material,
            speed_start_knots=args.speed_start,
            speed_end_knots=args.speed_end,
            speed_step_knots=args.speed_step,
        )
        print()
        print("Dashboard HTML criado em:")
        print(html_path)


if __name__ == "__main__":
    main()
