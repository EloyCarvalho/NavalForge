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


def _draw_dimension_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label: str,
    color: str = "#334155",
    text_offset: float = -10.0,
) -> str:
    mid_x = (x1 + x2) / 2.0
    mid_y = (y1 + y2) / 2.0
    dx = x2 - x1
    dy = y2 - y1
    length = max((dx**2 + dy**2) ** 0.5, 1.0)
    ux = dx / length
    uy = dy / length
    arrow = 8.0
    px = -uy
    py = ux
    ax1x = x1 + ux * arrow + px * 4
    ax1y = y1 + uy * arrow + py * 4
    ax2x = x1 + ux * arrow - px * 4
    ax2y = y1 + uy * arrow - py * 4
    bx1x = x2 - ux * arrow + px * 4
    bx1y = y2 - uy * arrow + py * 4
    bx2x = x2 - ux * arrow - px * 4
    bx2y = y2 - uy * arrow - py * 4
    tx = mid_x + px * text_offset
    ty = mid_y + py * text_offset
    return (
        "<g>"
        f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{color}' stroke-width='1.8' />"
        f"<polygon points='{x1:.1f},{y1:.1f} {ax1x:.1f},{ax1y:.1f} {ax2x:.1f},{ax2y:.1f}' fill='{color}' />"
        f"<polygon points='{x2:.1f},{y2:.1f} {bx1x:.1f},{bx1y:.1f} {bx2x:.1f},{bx2y:.1f}' fill='{color}' />"
        f"<text x='{tx:.1f}' y='{ty:.1f}' font-size='17' font-weight='600' fill='{color}' "
        "text-anchor='middle' dominant-baseline='central'>"
        f"{escape(label)}</text>"
        "</g>"
    )


def _draw_scale_bar(x: float, y: float, pixels_per_meter: float, color: str = "#1e293b") -> str:
    x2 = x + pixels_per_meter
    return (
        "<g>"
        f"<line x1='{x:.1f}' y1='{y:.1f}' x2='{x2:.1f}' y2='{y:.1f}' stroke='{color}' stroke-width='4' />"
        f"<line x1='{x:.1f}' y1='{(y - 6):.1f}' x2='{x:.1f}' y2='{(y + 6):.1f}' stroke='{color}' stroke-width='2' />"
        f"<line x1='{x2:.1f}' y1='{(y - 6):.1f}' x2='{x2:.1f}' y2='{(y + 6):.1f}' stroke='{color}' stroke-width='2' />"
        f"<text x='{(x + x2) / 2.0:.1f}' y='{(y - 12):.1f}' font-size='16' fill='{color}' text-anchor='middle'>1 m</text>"
        "</g>"
    )


def _draw_human_silhouette(x: float, base_y: float, height_px: float) -> str:
    head_r = height_px * 0.08
    torso_h = height_px * 0.37
    leg_h = height_px * 0.35
    shoulder_w = height_px * 0.14
    hip_w = height_px * 0.09
    head_y = base_y - height_px + head_r
    torso_top = head_y + head_r * 2 + 2
    torso_bottom = torso_top + torso_h
    hip_y = torso_bottom
    return (
        "<g fill='none' stroke='#334155' stroke-width='2'>"
        f"<circle cx='{x:.1f}' cy='{head_y:.1f}' r='{head_r:.1f}' fill='#cbd5e1' />"
        f"<line x1='{x:.1f}' y1='{torso_top:.1f}' x2='{x:.1f}' y2='{torso_bottom:.1f}' />"
        f"<line x1='{(x - shoulder_w):.1f}' y1='{(torso_top + torso_h * 0.22):.1f}' "
        f"x2='{(x + shoulder_w):.1f}' y2='{(torso_top + torso_h * 0.22):.1f}' />"
        f"<line x1='{x:.1f}' y1='{hip_y:.1f}' x2='{(x - hip_w):.1f}' y2='{(hip_y + leg_h):.1f}' />"
        f"<line x1='{x:.1f}' y1='{hip_y:.1f}' x2='{(x + hip_w):.1f}' y2='{(hip_y + leg_h):.1f}' />"
        "</g>"
    )


def _draw_boat_side_view(
    x: float,
    y: float,
    width: float,
    height: float,
    length_m: float,
    beam_m: float,
    pixels_per_meter: float,
) -> str:
    length_px = max(length_m * pixels_per_meter, 20.0)
    hull_h = max(beam_m * pixels_per_meter * 0.42, 16.0)
    x0 = x + 30
    water_y = y + height * 0.72
    x1 = x0 + length_px
    deck_y = water_y - hull_h * 0.92
    keel_y = water_y + hull_h * 0.28
    cabin_x0 = x0 + length_px * 0.42
    cabin_x1 = x0 + length_px * 0.70
    cabin_y = deck_y - hull_h * 0.45
    hull = (
        f"M {x0:.1f},{deck_y:.1f} "
        f"L {(x0 + length_px * 0.12):.1f},{(deck_y - hull_h * 0.10):.1f} "
        f"L {(x0 + length_px * 0.82):.1f},{(deck_y - hull_h * 0.06):.1f} "
        f"L {x1:.1f},{(deck_y + hull_h * 0.10):.1f} "
        f"L {(x1 - length_px * 0.04):.1f},{(water_y + hull_h * 0.12):.1f} "
        f"Q {(x0 + length_px * 0.45):.1f},{keel_y:.1f} {x0:.1f},{(water_y + hull_h * 0.04):.1f} Z"
    )
    return (
        "<g>"
        f"<text x='{(x + 18):.1f}' y='{(y + 30):.1f}' font-size='22' font-weight='700' fill='#1f2937'>Vista lateral</text>"
        f"<line x1='{(x + 10):.1f}' y1='{water_y:.1f}' x2='{(x + width - 15):.1f}' y2='{water_y:.1f}' "
        "stroke='#0ea5e9' stroke-width='2' stroke-dasharray='10 6' />"
        f"<text x='{(x + width - 95):.1f}' y='{(water_y - 8):.1f}' font-size='14' fill='#0284c7'>Linha d'água</text>"
        f"<path d='{hull}' fill='#bfdbfe' stroke='#1e3a8a' stroke-width='2' />"
        f"<rect x='{cabin_x0:.1f}' y='{cabin_y:.1f}' width='{(cabin_x1 - cabin_x0):.1f}' height='{(deck_y - cabin_y + 2):.1f}' "
        "fill='#dbeafe' stroke='#1e3a8a' stroke-width='1.8' rx='6' />"
        f"<line x1='{(cabin_x0 + 8):.1f}' y1='{(cabin_y + 10):.1f}' x2='{(cabin_x1 - 8):.1f}' y2='{(cabin_y + 10):.1f}' stroke='#1e40af' />"
        f"<text x='{(x0 + 3):.1f}' y='{(deck_y - 14):.1f}' font-size='14' fill='#334155'>Popa</text>"
        f"<text x='{(x1 - 30):.1f}' y='{(deck_y - 14):.1f}' font-size='14' fill='#334155'>Proa</text>"
        f"{_draw_dimension_line(x0, water_y + 48, x1, water_y + 48, f'L = {length_m:.1f} m')}"
        f"{_draw_human_silhouette(x + width - 35, water_y + 2, 1.75 * pixels_per_meter)}"
        "</g>"
    )


def _draw_boat_top_view(
    x: float,
    y: float,
    width: float,
    height: float,
    length_m: float,
    beam_m: float,
    pixels_per_meter: float,
) -> str:
    length_px = max(length_m * pixels_per_meter, 20.0)
    beam_px = max(beam_m * pixels_per_meter, 10.0)
    cx = x + 30 + length_px / 2.0
    cy = y + height * 0.56
    x0 = cx - length_px / 2.0
    x1 = cx + length_px / 2.0
    y0 = cy - beam_px / 2.0
    y1 = cy + beam_px / 2.0
    outline = (
        f"M {x0:.1f},{cy:.1f} "
        f"Q {(x0 + length_px * 0.18):.1f},{y0:.1f} {(cx - length_px * 0.06):.1f},{y0:.1f} "
        f"L {(cx + length_px * 0.30):.1f},{(cy - beam_px * 0.30):.1f} "
        f"Q {(x1 - length_px * 0.02):.1f},{(cy - beam_px * 0.08):.1f} {x1:.1f},{cy:.1f} "
        f"Q {(x1 - length_px * 0.02):.1f},{(cy + beam_px * 0.08):.1f} {(cx + length_px * 0.30):.1f},{(cy + beam_px * 0.30):.1f} "
        f"L {(cx - length_px * 0.06):.1f},{y1:.1f} "
        f"Q {(x0 + length_px * 0.18):.1f},{y1:.1f} {x0:.1f},{cy:.1f} Z"
    )
    beam_x = cx - length_px * 0.22
    return (
        "<g>"
        f"<text x='{(x + 18):.1f}' y='{(y + 30):.1f}' font-size='22' font-weight='700' fill='#1f2937'>Vista superior</text>"
        f"<path d='{outline}' fill='#dbeafe' stroke='#1e3a8a' stroke-width='2' />"
        f"<line x1='{beam_x:.1f}' y1='{y0:.1f}' x2='{beam_x:.1f}' y2='{y1:.1f}' stroke='#2563eb' stroke-width='2' stroke-dasharray='5 4' />"
        f"{_draw_dimension_line(beam_x, y0, beam_x, y1, f'B = {beam_m:.1f} m', text_offset=14.0)}"
        "</g>"
    )


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

    width, height = 1800, 1200
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

    power_x0, power_y0, power_w, power_h = 40, 700, 850, 250
    trim_x0, trim_y0, trim_w, trim_h = 910, 700, 850, 250

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
            f"<rect x='910' y='{1015 + idx * 17}' width='850' height='17' fill='{row_bg}' stroke='{border}' />"
            f"<text x='930' y='{1028 + idx * 17}' font-size='12' fill='{text_dark}'>{item.speed_knots:.1f}</text>"
            f"<text x='1060' y='{1028 + idx * 17}' font-size='12' fill='{text_dark}'>{item.required_power_kw:.1f}</text>"
            f"<text x='1210' y='{1028 + idx * 17}' font-size='12' fill='{text_dark}'>{item.trim_deg:.2f}</text>"
            f"<text x='1320' y='{1028 + idx * 17}' font-size='12' fill='{red if alert == 'ALERTA' else text_muted}'>{alert}</text>"
            "</g>"
        )

    power_alert_y = _scale_point(600.0, power_min, power_max, power_y0 + power_h - 40, power_y0 + 25)
    trim_alert_y = _scale_point(6.0, trim_min, trim_max, trim_y0 + trim_h - 40, trim_y0 + 25)

    mission_text = "".join(
        f"<text x='70' y='{205 + idx * 33}' font-size='25' fill='{text_dark}'>{escape(line)}</text>"
        for idx, line in enumerate(mission_lines)
    )
    kpi_text = "".join(
        (
            f"<rect x='{580 + idx * 236}' y='120' width='220' height='130' rx='14' fill='{card_bg}' stroke='{border}' />"
            f"<text x='{595 + idx * 236}' y='165' font-size='20' fill='{text_muted}'>{escape(title)}</text>"
            f"<text x='{595 + idx * 236}' y='208' font-size='30' font-weight='700' fill='{red if is_alert else blue}'>"
            f"{escape(value)}</text>"
        )
        for idx, (title, value, is_alert) in enumerate(kpi_cards)
    )

    boat_x, boat_y, boat_w, boat_h = 40, 350, 1720, 320
    side_x, side_y, side_w, side_h = 60, 390, 820, 250
    top_x, top_y, top_w, top_h = 910, 390, 820, 250
    pixels_per_meter = min(
        (side_w - 120) / max(length_m, 0.1),
        (top_w - 120) / max(length_m, 0.1),
        (top_h - 110) / max(beam_m, 0.1),
    )
    boat_section = (
        f"<rect x='{boat_x}' y='{boat_y}' width='{boat_w}' height='{boat_h}' rx='16' fill='{card_bg}' stroke='{border}' />"
        f"<text x='70' y='386' font-size='30' font-weight='700' fill='{text_dark}'>Vista esquemática da embarcação</text>"
        f"{_draw_boat_side_view(side_x, side_y, side_w, side_h, length_m, beam_m, pixels_per_meter)}"
        f"{_draw_boat_top_view(top_x, top_y, top_w, top_h, length_m, beam_m, pixels_per_meter)}"
        f"{_draw_scale_bar(80, 646, pixels_per_meter)}"
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="{background}" />
  <text x="40" y="60" font-size="46" font-weight="700" fill="{text_dark}">NavalForge — Dashboard Visual</text>
  <text x="40" y="95" font-size="24" fill="{text_muted}">Missão → Peso → Hidrodinâmica → Potência → Alertas</text>

  <rect x="40" y="120" width="520" height="210" rx="16" fill="{card_bg}" stroke="{border}" />
  <text x="70" y="165" font-size="32" font-weight="700" fill="{text_dark}">Missão de entrada</text>
  {mission_text}
  <text x="70" y="318" font-size="20" fill="{text_muted}">Sweep: {speed_start_knots:.1f} → {speed_end_knots:.1f} kn (passo {speed_step_knots:.1f})</text>

  {kpi_text}
  {boat_section}

  <rect x="{power_x0}" y="{power_y0}" width="{power_w}" height="{power_h}" rx="14" fill="{card_bg}" stroke="{border}" />
  <text x="{power_x0 + 20}" y="{power_y0 + 40}" font-size="27" font-weight="700" fill="{text_dark}">Potência requerida vs Velocidade</text>
  <line x1="{power_x0 + 40}" y1="{power_y0 + power_h - 40}" x2="{power_x0 + power_w - 25}" y2="{power_y0 + power_h - 40}" stroke="{text_muted}" />
  <line x1="{power_x0 + 40}" y1="{power_y0 + 25}" x2="{power_x0 + 40}" y2="{power_y0 + power_h - 40}" stroke="{text_muted}" />
  <line x1="{power_x0 + 40}" y1="{power_alert_y:.2f}" x2="{power_x0 + power_w - 25}" y2="{power_alert_y:.2f}" stroke="{red}" stroke-dasharray="8 6" />
  <text x="{power_x0 + power_w - 170}" y="{power_alert_y - 8:.2f}" font-size="17" fill="{red}">600 kW limite</text>
  <polyline fill="none" stroke="{blue}" stroke-width="3" points="{' '.join(power_points)}" />
  {''.join(point_marks)}
  <text x="{power_x0 + 42}" y="{power_y0 + power_h - 12}" font-size="17" fill="{text_muted}">Velocidade (kn)</text>
  <text x="{power_x0 + 45}" y="{power_y0 + 65}" font-size="17" fill="{text_muted}">Potência (kW)</text>

  <rect x="{trim_x0}" y="{trim_y0}" width="{trim_w}" height="{trim_h}" rx="14" fill="{card_bg}" stroke="{border}" />
  <text x="{trim_x0 + 20}" y="{trim_y0 + 40}" font-size="27" font-weight="700" fill="{text_dark}">Trim vs Velocidade</text>
  <line x1="{trim_x0 + 40}" y1="{trim_y0 + trim_h - 40}" x2="{trim_x0 + trim_w - 25}" y2="{trim_y0 + trim_h - 40}" stroke="{text_muted}" />
  <line x1="{trim_x0 + 40}" y1="{trim_y0 + 25}" x2="{trim_x0 + 40}" y2="{trim_y0 + trim_h - 40}" stroke="{text_muted}" />
  <line x1="{trim_x0 + 40}" y1="{trim_alert_y:.2f}" x2="{trim_x0 + trim_w - 25}" y2="{trim_alert_y:.2f}" stroke="{red}" stroke-dasharray="8 6" />
  <text x="{trim_x0 + trim_w - 145}" y="{trim_alert_y - 8:.2f}" font-size="17" fill="{red}">6.0° limite</text>
  <polyline fill="none" stroke="{blue}" stroke-width="3" points="{' '.join(trim_points)}" />
  {''.join(trim_marks)}
  <text x="{trim_x0 + 42}" y="{trim_y0 + trim_h - 12}" font-size="17" fill="{text_muted}">Velocidade (kn)</text>
  <text x="{trim_x0 + 45}" y="{trim_y0 + 65}" font-size="17" fill="{text_muted}">Trim (deg)</text>

  <rect x="910" y="960" width="850" height="220" rx="14" fill="{card_bg}" stroke="{border}" />
  <text x="940" y="995" font-size="26" font-weight="700" fill="{text_dark}">Tabela resumida do speed sweep</text>
  <rect x="910" y="1005" width="850" height="17" fill="#eff4ff" stroke="{border}" />
  <text x="930" y="1018" font-size="12" font-weight="700" fill="{text_dark}">Velocidade (kn)</text>
  <text x="1060" y="1018" font-size="12" font-weight="700" fill="{text_dark}">Potência (kW)</text>
  <text x="1210" y="1018" font-size="12" font-weight="700" fill="{text_dark}">Trim (deg)</text>
  <text x="1320" y="1018" font-size="12" font-weight="700" fill="{text_dark}">Alerta</text>
  {''.join(table_rows)}

  <rect x="40" y="960" width="850" height="220" rx="14" fill="{card_bg}" stroke="{border}" />
  <text x="70" y="998" font-size="30" font-weight="700" fill="{text_dark}">Leitura de Engenharia</text>
  <text x="70" y="1040" font-size="24" fill="{text_dark}">• Faixa mais razoável desta configuração: 26–30 nós</text>
  <text x="70" y="1074" font-size="24" fill="{text_dark}">• Acima de 32 nós, a potência requerida entra em alerta</text>
  <text x="70" y="1108" font-size="24" fill="{text_dark}">• Em 34–36 nós, o trim também sai da faixa preferida</text>
  <text x="70" y="1142" font-size="24" fill="{text_dark}">• Conclusão preliminar: revisar peso, casco ou missão para velocidades mais altas</text>
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
