from __future__ import annotations
import json
from pathlib import Path
from navalforge.hull import Hull

def save_hull(hull: Hull, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(hull.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return p

def load_hull(path: str | Path) -> Hull:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return Hull.from_dict(data)
