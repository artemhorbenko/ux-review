#!/usr/bin/env python3
"""Turn an audit.json into a finished report page.

Usage: python build_report.py audit.json report.html [--template path] [--force]

Validates the data first (see validate_audit.py) and stops on errors unless
--force is given. Then puts the JSON into the template's
<script type="application/json" id="audit"> block, sets <html lang> and
<title>, and writes the page. Standard library only.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from validate_audit import validate  # noqa: E402

BLOCK = re.compile(r'(<script type="application/json" id="audit">\n?)(.*?)(\n?</script>)', re.S)


def build(audit, template):
    blob = json.dumps(audit, ensure_ascii=False, indent=1)
    blob = blob.replace("</", "<\\/").replace("<!--", "<\\!--")
    if not BLOCK.search(template):
        raise ValueError("the template has no <script type=\"application/json\" id=\"audit\"> block")
    page = BLOCK.sub(lambda m: m.group(1) + blob + m.group(3), template, count=1)
    lang = audit.get("lang", "en")
    page = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', page, count=1)
    title = audit.get("title")
    if title:
        safe = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        page = re.sub(r"<title>.*?</title>", lambda m: f"<title>{safe}</title>", page, count=1, flags=re.S)
    return page


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audit")
    ap.add_argument("out")
    ap.add_argument("--template", default=os.path.join(HERE, "..", "assets", "report-template.html"))
    ap.add_argument("--force", action="store_true", help="write the page even if validation finds errors")
    a = ap.parse_args()

    with open(a.audit, encoding="utf-8") as f:
        audit = json.load(f)
    err, warn = validate(audit)
    for w in warn:
        print("[WARN] ", w)
    for e in err:
        print("[ERROR]", e)
    if err and not a.force:
        print(f"Not built: {len(err)} error(s). Fix them or pass --force.")
        return 1
    with open(a.template, encoding="utf-8") as f:
        page = build(audit, f.read())
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Written {a.out} ({len(page) // 1024} KB). Next: python {os.path.join(HERE, 'check_report.py')} {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
