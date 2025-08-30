#!/usr/bin/env python3
"""
Split a Markdown table by the 'Application/field' column into separate .md files,
and add a heading (# Field Name) at the top of each file.
"""
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

def slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", name.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "untitled"

def is_table_sep(line: str) -> bool:
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return False
    cells = [c.strip() for c in s.strip("|").split("|")]
    return all(re.fullmatch(r":?-{3,}:?", c or "-") for c in cells)

def is_table_row(line: str) -> bool:
    return line.strip().startswith("|") and line.strip().endswith("|")

def split_markdown_tables(lines: List[str]) -> List[Tuple[int, int]]:
    spans = []
    i = 0
    n = len(lines)
    while i < n:
        if is_table_row(lines[i]):
            if i + 1 < n and is_table_sep(lines[i + 1]):
                j = i + 2
                while j < n and is_table_row(lines[j]):
                    j += 1
                if j > i + 2:
                    spans.append((i, j))
                    i = j
                    continue
        i += 1
    return spans

def parse_row(line: str) -> List[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]

def split_by_application_field(table_lines: List[str]) -> Dict[str, Tuple[str, List[str]]]:
    out: Dict[str, Tuple[str, List[str]]] = {}
    header = table_lines[0]
    sep = table_lines[1]

    subheader = None
    data_start_idx = 2
    if len(table_lines) >= 3:
        maybe_sub = table_lines[2]
        if is_table_row(maybe_sub):
            cells = parse_row(maybe_sub)
            if cells and (cells[0] == "" or cells[0] == " "):
                subheader = maybe_sub
                data_start_idx = 3

    header_cells = parse_row(header)
    try:
        app_col = next(
            idx for idx, name in enumerate(header_cells)
            if name.strip().lower() in {"application/field", "application", "field"}
        )
    except StopIteration:
        app_col = 0

    header_block = [header, sep]
    if subheader is not None:
        header_block.append(subheader)

    for line in table_lines[data_start_idx:]:
        if not is_table_row(line):
            continue
        cells = parse_row(line)
        if app_col >= len(cells):
            continue
        key = cells[app_col].strip()
        if not key:
            continue
        slug = slugify(key)
        out[slug] = (key, header_block + [line]) if slug not in out else (key, out[slug][1] + [line])
    return out

def main(inp: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = inp.read_text(encoding="utf-8").splitlines()

    tables = split_markdown_tables(lines)
    if not tables:
        print("No Markdown tables found.")
        return

    for (start, end) in tables:
        block = lines[start:end]
        per_field = split_by_application_field(block)

        for slug, (field_name, table_lines) in per_field.items():
            md_path = out_dir / f"{slug}.md"

            if md_path.exists():
                existing = md_path.read_text(encoding="utf-8").splitlines()
                # Append only new rows (skip header if already written)
                write_lines = table_lines[2:]
                if len(table_lines) >= 3 and parse_row(table_lines[2]) and (parse_row(table_lines[2])[0] == "" or parse_row(table_lines[2])[0] == " "):
                    write_lines = table_lines[3:]
                with md_path.open("a", encoding="utf-8") as f:
                    f.write("\n")
                    f.write("\n".join(write_lines))
                    f.write("\n")
            else:
                # Add heading at the very top
                md_content = f"# {field_name}\n\n" + "\n".join(table_lines) + "\n"
                md_path.write_text(md_content, encoding="utf-8")
                print(f"Wrote {md_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_md_tables.py input.md")
        sys.exit(1)
    inp = Path(sys.argv[1])
    out_dir = Path("out_tables")
    main(inp, out_dir)
