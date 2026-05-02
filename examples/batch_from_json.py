from navalforge.io.project_store import load_hull
from navalforge.evaluator import evaluate_hull
from navalforge.reporting import write_markdown_report

hull = load_hull("data/projects/lancha_12m.json")
result = evaluate_hull(hull)
print(write_markdown_report(result, "reports/json_case_report.md"))
