from __future__ import annotations

import csv
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List

NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def _col_to_index(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref or "")
    if not match:
        return 0
    idx = 0
    for ch in match.group(1):
        idx = idx * 26 + (ord(ch) - 64)
    return idx - 1


def _parse_shared_strings(zf: zipfile.ZipFile) -> List[str]:
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    strings: List[str] = []
    for si in root.findall("a:si", NS):
        parts = [t.text or "" for t in si.findall(".//a:t", NS)]
        strings.append("".join(parts))
    return strings


def _sheet_path_by_name(zf: zipfile.ZipFile, sheet_name: str) -> str:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall("rel:Relationship", NS)}
    for sheet in workbook.findall("a:sheets/a:sheet", NS):
        if sheet.attrib.get("name") == sheet_name:
            rid = sheet.attrib.get(f"{{{NS['r']}}}id")
            target = rel_map[rid]
            return "xl/" + target.lstrip("/")
    raise ValueError(f"Aba não encontrada: {sheet_name}")


def read_xlsx_sheet(path: str | Path, sheet_name: str) -> List[Dict[str, Any]]:
    """Leitor XLSX mínimo para a aba principal do banco NavalForge."""
    path = Path(path)
    with zipfile.ZipFile(path) as zf:
        shared = _parse_shared_strings(zf)
        sheet_path = _sheet_path_by_name(zf, sheet_name)
        root = ET.fromstring(zf.read(sheet_path))

        rows: List[List[Any]] = []
        for row in root.findall(".//a:sheetData/a:row", NS):
            values: List[Any] = []
            for cell in row.findall("a:c", NS):
                idx = _col_to_index(cell.attrib.get("r", "A1"))
                while len(values) <= idx:
                    values.append("")
                ctype = cell.attrib.get("t")
                v = cell.find("a:v", NS)
                raw = v.text if v is not None else ""
                if ctype == "s" and raw != "":
                    value: Any = shared[int(raw)]
                else:
                    value = raw
                values[idx] = value
            rows.append(values)

    if not rows:
        return []
    headers = [str(h).strip() for h in rows[0]]
    records: List[Dict[str, Any]] = []
    for row in rows[1:]:
        if not any(str(v).strip() for v in row):
            continue
        rec = {headers[i]: row[i] if i < len(row) else "" for i in range(len(headers)) if headers[i]}
        records.append(rec)
    return records


def read_csv(path: str | Path) -> List[Dict[str, Any]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))
