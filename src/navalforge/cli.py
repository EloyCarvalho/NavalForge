from __future__ import annotations
import argparse
from .hull import Hull
from .evaluator import evaluate_hull
from .variants import generate_variants, evaluate_variants
from .reporting import write_markdown_report, write_html_report
from .io.project_store import save_hull, load_hull

def build_hull_from_args(args) -> Hull:
    return Hull(name=args.name, lwl=args.lwl, beam=args.beam, draft=args.draft, cb=args.cb, cp=args.cp, cwp=args.cwp, lcb=args.lcb, lcg=args.lcg, vcg=args.vcg, speed_knots=args.speed, deadrise_deg=args.deadrise)

def add_hull_args(p):
    p.add_argument("--name", default="Case_001")
    p.add_argument("--lwl", type=float, default=12.0)
    p.add_argument("--beam", type=float, default=3.2)
    p.add_argument("--draft", type=float, default=0.55)
    p.add_argument("--cb", type=float, default=0.42)
    p.add_argument("--cp", type=float, default=0.65)
    p.add_argument("--cwp", type=float, default=0.78)
    p.add_argument("--lcb", type=float, default=5.8)
    p.add_argument("--lcg", type=float, default=5.8)
    p.add_argument("--vcg", type=float, default=1.1)
    p.add_argument("--speed", type=float, default=22.0)
    p.add_argument("--deadrise", type=float, default=15.0)

def main(argv=None):
    parser = argparse.ArgumentParser(prog="navalforge")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_eval = sub.add_parser("evaluate")
    add_hull_args(p_eval)
    p_eval.add_argument("--html", action="store_true")
    p_var = sub.add_parser("variants")
    add_hull_args(p_var)
    p_save = sub.add_parser("save")
    add_hull_args(p_save)
    p_save.add_argument("--out", default="data/projects/case.json")
    p_load = sub.add_parser("load-evaluate")
    p_load.add_argument("path")
    args = parser.parse_args(argv)
    if args.cmd == "evaluate":
        result = evaluate_hull(build_hull_from_args(args))
        print(f"Status: {result.status} | Score: {result.score:.1f}")
        print(write_markdown_report(result, "reports/cli_report.md"))
        if args.html:
            print(write_html_report(result, "reports/cli_report.html"))
    elif args.cmd == "variants":
        base = build_hull_from_args(args)
        variants = generate_variants(base, [base.beam*0.95, base.beam, base.beam*1.05], [base.draft*0.9, base.draft, base.draft*1.1], [base.speed_knots*0.85, base.speed_knots, base.speed_knots*1.15])
        df = evaluate_variants(variants)
        df.to_csv("reports/cli_variants.csv", index=False)
        print(df.head(10).to_string(index=False))
    elif args.cmd == "save":
        print(save_hull(build_hull_from_args(args), args.out))
    elif args.cmd == "load-evaluate":
        result = evaluate_hull(load_hull(args.path))
        print(f"Status: {result.status} | Score: {result.score:.1f}")

if __name__ == "__main__":
    main()
