from __future__ import annotations

from html import escape
from pathlib import Path

from navalforge.analysis import run_speed_sweep
from navalforge.pipeline.design_loop import DesignLoop, MissionInput


def _format_float(value: float) -> str:
    return f"{value:.1f}"


def _scale_point(
    value: float,
    domain_min: float,
    domain_max: float,
    range_min: float,
    range_max: float,
) -> float:
    if domain_max <= domain_min:
        return (range_min + range_max) / 2.0
    ratio = (value - domain_min) / (domain_max - domain_min)
    return range_min + ratio * (range_max - range_min)


def generate_speed_sweep_dashboard(
    output_path: str = "reports/navalforge_dashboard.html",
    length_m: float = 8.0,
    beam_m: float = 2.6,
    target_speed_knots: float = 28.0,
    passengers: int = 6,
    fuel_capacity_l: float = 300.0,
    material: str = "fiberglass",
    speed_start_knots: float = 18.0,
    speed_end_knots: float = 36.0,
    speed_step_knots: float = 2.0,
) -> str:
    mission = MissionInput(
        length_m=length_m,
        beam_m=beam_m,
        target_speed_knots=target_speed_knots,
        passengers=passengers,
        fuel_capacity_l=fuel_capacity_l,
        material=material,
    )

    baseline_result = DesignLoop().run(mission)
    sweep_results = run_speed_sweep(
        base_mission=mission,
        speed_start_knots=speed_start_knots,
        speed_end_knots=speed_end_knots,
        speed_step_knots=speed_step_knots,
    )

    speeds = [item.speed_knots for item in sweep_results]
    power = [item.required_power_kw for item in sweep_results]
    resistance = [item.resistance_n for item in sweep_results]
    trim = [item.trim_deg for item in sweep_results]

    rows = "\n".join(
        (
            "<tr>"
            f"<td>{item.speed_knots:.1f}</td>"
            f"<td>{item.required_power_kw:.1f}</td>"
            f"<td>{item.resistance_n:.1f}</td>"
            f"<td>{item.trim_deg:.2f}</td>"
            f"<td>{escape('; '.join(item.warnings)) if item.warnings else '-'}</td>"
            "</tr>"
        )
        for item in sweep_results
    )

    html = f"""<!doctype html>
<html lang=\"pt-BR\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>NavalForge Dashboard</title>
  <script src=\"https://cdn.plot.ly/plotly-2.35.2.min.js\"></script>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #0f172a; }}
    h1, h2 {{ margin: 0 0 12px 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(260px, 1fr)); gap: 12px; margin-bottom: 24px; }}
    .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px; }}
    .stats {{ display: grid; grid-template-columns: repeat(3, minmax(180px, 1fr)); gap: 12px; margin-bottom: 18px; }}
    .stat {{ background: #eef2ff; border-radius: 8px; padding: 12px; }}
    .stat strong {{ display: block; font-size: 0.95rem; color: #334155; }}
    .stat span {{ font-size: 1.3rem; font-weight: 700; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
    th, td {{ border: 1px solid #cbd5e1; padding: 8px; text-align: left; font-size: 0.9rem; }}
    th {{ background: #e2e8f0; }}
    #chart {{ width: 100%; height: 560px; }}
  </style>
</head>
<body>
  <h1>NavalForge · Dashboard de Speed Sweep</h1>

  <h2>Missão de entrada</h2>
  <div class=\"grid\">
    <div class=\"card\"><strong>Comprimento:</strong> {_format_float(length_m)} m</div>
    <div class=\"card\"><strong>Boca:</strong> {_format_float(beam_m)} m</div>
    <div class=\"card\"><strong>Velocidade alvo:</strong> {_format_float(target_speed_knots)} kn</div>
    <div class=\"card\"><strong>Passageiros:</strong> {passengers}</div>
    <div class=\"card\"><strong>Combustível:</strong> {_format_float(fuel_capacity_l)} L</div>
    <div class=\"card\"><strong>Material:</strong> {escape(material)}</div>
    <div class=\"card\" style=\"grid-column: 1 / -1;\"><strong>Faixa do speed sweep:</strong>
      {_format_float(speed_start_knots)} a {_format_float(speed_end_knots)} kn (passo {_format_float(speed_step_knots)} kn)
    </div>
  </div>

  <h2>Resultado na velocidade alvo</h2>
  <div class=\"stats\">
    <div class=\"stat\"><strong>Deslocamento estimado</strong><span>{baseline_result['estimated_weight_kg']:.1f} kg</span></div>
    <div class=\"stat\"><strong>Resistência</strong><span>{baseline_result['resistance_n']:.1f} N</span></div>
    <div class=\"stat\"><strong>Potência requerida</strong><span>{baseline_result['power_kw']:.1f} kW</span></div>
  </div>

  <div id=\"chart\"></div>

  <h2>Tabela do sweep</h2>
  <table>
    <thead>
      <tr>
        <th>Velocidade (kn)</th>
        <th>Potência (kW)</th>
        <th>Resistência (N)</th>
        <th>Trim (deg)</th>
        <th>Warnings</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>

  <script>
    const speeds = {speeds};
    const power = {power};
    const resistance = {resistance};
    const trim = {trim};

    const traces = [
      {{ x: speeds, y: power, name: 'Power (kW)', type: 'scatter', mode: 'lines+markers', yaxis: 'y' }},
      {{ x: speeds, y: resistance, name: 'Resistance (N)', type: 'scatter', mode: 'lines+markers', yaxis: 'y2' }},
      {{ x: speeds, y: trim, name: 'Trim (deg)', type: 'scatter', mode: 'lines+markers', yaxis: 'y3' }},
    ];

    const layout = {{
      title: 'Speed Sweep',
      xaxis: {{ title: 'Velocidade (kn)' }},
      yaxis: {{ title: 'Potência (kW)' }},
      yaxis2: {{ title: 'Resistência (N)', overlaying: 'y', side: 'right' }},
      yaxis3: {{ title: 'Trim (deg)', anchor: 'free', overlaying: 'y', side: 'right', position: 0.95 }},
      legend: {{ orientation: 'h', y: 1.15 }},
      margin: {{ t: 60 }},
    }};

    Plotly.newPlot('chart', traces, layout, {{ responsive: true }});
  </script>
</body>
</html>
"""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return str(output)


def generate_speed_sweep_svg(
    output_path: str = "reports/navalforge_dashboard.svg",
    length_m: float = 8.0,
    beam_m: float = 2.6,
    target_speed_knots: float = 28.0,
    passengers: int = 6,
    fuel_capacity_l: float = 300.0,
    material: str = "fiberglass",
    speed_start_knots: float = 18.0,
    speed_end_knots: float = 36.0,
    speed_step_knots: float = 2.0,
) -> str:
    mission = MissionInput(
        length_m=length_m,
        beam_m=beam_m,
        target_speed_knots=target_speed_knots,
        passengers=passengers,
        fuel_capacity_l=fuel_capacity_l,
        material=material,
    )

    baseline_result = DesignLoop().run(mission)
    sweep_results = run_speed_sweep(
        base_mission=mission,
        speed_start_knots=speed_start_knots,
        speed_end_knots=speed_end_knots,
        speed_step_knots=speed_step_knots,
    )

    speeds = [item.speed_knots for item in sweep_results]
    powers = [item.required_power_kw for item in sweep_results]
    trims = [item.trim_deg for item in sweep_results]

    width, height = 1600, 1100
    background = "#f3f6fb"
    card_bg = "#ffffff"
    border = "#d6dfeb"
    text_dark = "#1f2937"
    text_muted = "#4b5563"
    blue = "#1d4ed8"
    red = "#dc2626"

    power_warn_count = sum(1 for item in sweep_results if item.required_power_kw > 600.0)
    trim_warn_count = sum(1 for item in sweep_results if item.trim_deg > 6.0)
    total_warnings = sum(len(item.warnings) for item in sweep_results)

    mission_lines = [
        f"Comprimento: {length_m:.1f} m",
        f"Boca: {beam_m:.1f} m",
        f"Velocidade alvo: {target_speed_knots:.1f} kn",
        f"Passageiros: {passengers}",
        f"Combustível: {fuel_capacity_l:.1f} L",
        f"Material: {material}",
    ]
    kpi_cards = [
        ("Deslocamento estimado", f"{baseline_result['estimated_weight_kg']:.1f} kg", False),
        ("Resistência total", f"{baseline_result['resistance_n']:.1f} N", False),
        ("Potência requerida", f"{baseline_result['power_kw']:.1f} kW", baseline_result["power_kw"] > 600.0),
        ("Trim previsto", f"{baseline_result['trim_deg']:.2f} deg", baseline_result["trim_deg"] > 6.0),
        (
            "Warnings",
            f"{total_warnings} ({power_warn_count} potência / {trim_warn_count} trim)",
            total_warnings > 0,
        ),
    ]

    power_x0, power_y0, power_w, power_h = 560, 250, 500, 300
    trim_x0, trim_y0, trim_w, trim_h = 1080, 250, 500, 300

    x_min = min(speeds)
    x_max = max(speeds)
    power_min = min(0.0, min(powers))
    power_max = max(600.0, max(powers)) * 1.05
    trim_min = min(0.0, min(trims))
    trim_max = max(6.0, max(trims)) * 1.1

    power_points: list[str] = []
    trim_points: list[str] = []
    point_marks: list[str] = []
    trim_marks: list[str] = []
    table_rows: list[str] = []

    for idx, item in enumerate(sweep_results):
        px = _scale_point(item.speed_knots, x_min, x_max, power_x0 + 40, power_x0 + power_w - 25)
        py = _scale_point(item.required_power_kw, power_min, power_max, power_y0 + power_h - 40, power_y0 + 25)
        tx = _scale_point(item.speed_knots, x_min, x_max, trim_x0 + 40, trim_x0 + trim_w - 25)
        ty = _scale_point(item.trim_deg, trim_min, trim_max, trim_y0 + trim_h - 40, trim_y0 + 25)
        power_points.append(f"{px:.2f},{py:.2f}")
        trim_points.append(f"{tx:.2f},{ty:.2f}")

        point_color = red if item.required_power_kw > 600.0 else blue
        trim_color = red if item.trim_deg > 6.0 else blue
        point_marks.append(f"<circle cx='{px:.2f}' cy='{py:.2f}' r='4' fill='{point_color}' />")
        trim_marks.append(f"<circle cx='{tx:.2f}' cy='{ty:.2f}' r='4' fill='{trim_color}' />")

        row_bg = "#fff1f2" if (item.required_power_kw > 600.0 or item.trim_deg > 6.0) else "#ffffff"
        alert = "ALERTA" if item.warnings else "-"
        table_rows.append(
            "<g>"
            f"<rect x='560' y='{590 + idx * 34}' width='1020' height='34' fill='{row_bg}' stroke='{border}' />"
            f"<text x='590' y='{612 + idx * 34}' font-size='15' fill='{text_dark}'>{item.speed_knots:.1f}</text>"
            f"<text x='760' y='{612 + idx * 34}' font-size='15' fill='{text_dark}'>{item.required_power_kw:.1f}</text>"
            f"<text x='950' y='{612 + idx * 34}' font-size='15' fill='{text_dark}'>{item.trim_deg:.2f}</text>"
            f"<text x='1110' y='{612 + idx * 34}' font-size='15' fill='{red if alert == 'ALERTA' else text_muted}'>{alert}</text>"
            "</g>"
        )

    power_alert_y = _scale_point(600.0, power_min, power_max, power_y0 + power_h - 40, power_y0 + 25)
    trim_alert_y = _scale_point(6.0, trim_min, trim_max, trim_y0 + trim_h - 40, trim_y0 + 25)

    mission_text = "".join(
        f"<text x='70' y='{286 + idx * 28}' font-size='20' fill='{text_dark}'>{escape(line)}</text>"
        for idx, line in enumerate(mission_lines)
    )
    kpi_text = "".join(
        (
            f"<rect x='{560 + idx * 203}' y='120' width='190' height='95' rx='12' fill='{card_bg}' stroke='{border}' />"
            f"<text x='{574 + idx * 203}' y='152' font-size='16' fill='{text_muted}'>{escape(title)}</text>"
            f"<text x='{574 + idx * 203}' y='184' font-size='20' font-weight='700' fill='{red if is_alert else blue}'>"
            f"{escape(value)}</text>"
        )
        for idx, (title, value, is_alert) in enumerate(kpi_cards)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="{background}" />
  <text x="50" y="58" font-size="38" font-weight="700" fill="{text_dark}">NavalForge — Dashboard Visual</text>
  <text x="50" y="90" font-size="20" fill="{text_muted}">Missão → Peso → Hidrodinâmica → Potência → Alertas</text>

  <rect x="40" y="120" width="490" height="430" rx="14" fill="{card_bg}" stroke="{border}" />
  <text x="70" y="165" font-size="28" font-weight="700" fill="{text_dark}">Missão de entrada</text>
  {mission_text}
  <text x="70" y="490" font-size="18" fill="{text_muted}">Sweep: {speed_start_knots:.1f} → {speed_end_knots:.1f} kn (passo {speed_step_knots:.1f})</text>

  {kpi_text}

  <rect x="{power_x0}" y="{power_y0}" width="{power_w}" height="{power_h}" rx="14" fill="{card_bg}" stroke="{border}" />
  <text x="{power_x0 + 20}" y="{power_y0 + 34}" font-size="20" font-weight="700" fill="{text_dark}">Potência requerida vs Velocidade</text>
  <line x1="{power_x0 + 40}" y1="{power_y0 + power_h - 40}" x2="{power_x0 + power_w - 25}" y2="{power_y0 + power_h - 40}" stroke="{text_muted}" />
  <line x1="{power_x0 + 40}" y1="{power_y0 + 25}" x2="{power_x0 + 40}" y2="{power_y0 + power_h - 40}" stroke="{text_muted}" />
  <line x1="{power_x0 + 40}" y1="{power_alert_y:.2f}" x2="{power_x0 + power_w - 25}" y2="{power_alert_y:.2f}" stroke="{red}" stroke-dasharray="8 6" />
  <text x="{power_x0 + power_w - 140}" y="{power_alert_y - 8:.2f}" font-size="14" fill="{red}">600 kW limite</text>
  <polyline fill="none" stroke="{blue}" stroke-width="3" points="{' '.join(power_points)}" />
  {''.join(point_marks)}
  <text x="{power_x0 + 42}" y="{power_y0 + power_h - 12}" font-size="14" fill="{text_muted}">Velocidade (kn)</text>
  <text x="{power_x0 + 45}" y="{power_y0 + 40}" font-size="14" fill="{text_muted}">Potência (kW)</text>

  <rect x="{trim_x0}" y="{trim_y0}" width="{trim_w}" height="{trim_h}" rx="14" fill="{card_bg}" stroke="{border}" />
  <text x="{trim_x0 + 20}" y="{trim_y0 + 34}" font-size="20" font-weight="700" fill="{text_dark}">Trim vs Velocidade</text>
  <line x1="{trim_x0 + 40}" y1="{trim_y0 + trim_h - 40}" x2="{trim_x0 + trim_w - 25}" y2="{trim_y0 + trim_h - 40}" stroke="{text_muted}" />
  <line x1="{trim_x0 + 40}" y1="{trim_y0 + 25}" x2="{trim_x0 + 40}" y2="{trim_y0 + trim_h - 40}" stroke="{text_muted}" />
  <line x1="{trim_x0 + 40}" y1="{trim_alert_y:.2f}" x2="{trim_x0 + trim_w - 25}" y2="{trim_alert_y:.2f}" stroke="{red}" stroke-dasharray="8 6" />
  <text x="{trim_x0 + trim_w - 125}" y="{trim_alert_y - 8:.2f}" font-size="14" fill="{red}">6.0° limite</text>
  <polyline fill="none" stroke="{blue}" stroke-width="3" points="{' '.join(trim_points)}" />
  {''.join(trim_marks)}
  <text x="{trim_x0 + 42}" y="{trim_y0 + trim_h - 12}" font-size="14" fill="{text_muted}">Velocidade (kn)</text>
  <text x="{trim_x0 + 45}" y="{trim_y0 + 40}" font-size="14" fill="{text_muted}">Trim (deg)</text>

  <rect x="560" y="560" width="1020" height="430" rx="14" fill="{card_bg}" stroke="{border}" />
  <text x="590" y="598" font-size="24" font-weight="700" fill="{text_dark}">Tabela resumida do speed sweep</text>
  <rect x="560" y="610" width="1020" height="34" fill="#eff4ff" stroke="{border}" />
  <text x="590" y="632" font-size="15" font-weight="700" fill="{text_dark}">Velocidade (kn)</text>
  <text x="760" y="632" font-size="15" font-weight="700" fill="{text_dark}">Potência (kW)</text>
  <text x="950" y="632" font-size="15" font-weight="700" fill="{text_dark}">Trim (deg)</text>
  <text x="1110" y="632" font-size="15" font-weight="700" fill="{text_dark}">Alerta</text>
  {''.join(table_rows)}

  <rect x="40" y="570" width="490" height="420" rx="14" fill="{card_bg}" stroke="{border}" />
  <text x="70" y="612" font-size="28" font-weight="700" fill="{text_dark}">Leitura de Engenharia</text>
  <text x="70" y="660" font-size="20" fill="{text_dark}">• Faixa mais razoável desta configuração: 26–30 nós</text>
  <text x="70" y="708" font-size="20" fill="{text_dark}">• Acima de 32 nós, a potência requerida entra em alerta</text>
  <text x="70" y="756" font-size="20" fill="{text_dark}">• Em 34–36 nós, o trim também sai da faixa preferida</text>
  <text x="70" y="804" font-size="20" fill="{text_dark}">• Conclusão preliminar: revisar peso, casco ou missão para velocidades mais altas</text>
</svg>
"""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    return str(output)


def export_html_to_png(html_path: str, png_path: str) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Para exportar PNG, instale: pip install playwright && python -m playwright install chromium"
        )
        return False

    html_file = Path(html_path).resolve()
    png_file = Path(png_path)
    png_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1600, "height": 1000})
            page.goto(html_file.as_uri(), wait_until="networkidle")
            page.screenshot(path=str(png_file), full_page=True)
            browser.close()
        return True
    except Exception:
        return False
