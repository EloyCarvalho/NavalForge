from navalforge.hull import Hull
from navalforge.evaluator import evaluate_hull
from navalforge.reporting import write_markdown_report, write_html_report

hull = Hull(name="Lancha_12m_Base", lwl=12.0, beam=3.20, draft=0.55, cb=0.42, cp=0.65, cwp=0.78, lcb=5.8, lcg=5.8, vcg=1.10, speed_knots=22.0, deadrise_deg=15)
result = evaluate_hull(hull)
print("=== NavalForge - Caso único ===")
print(f"Status: {result.status}")
print(f"Score: {result.score:.1f}")
print(write_markdown_report(result, "reports/lancha_12m_report.md"))
print(write_html_report(result, "reports/lancha_12m_report.html"))
for rec in result.recommendations:
    print("-", rec)
