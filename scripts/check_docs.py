#!/usr/bin/env python3
"""Check relative Markdown link targets without external dependencies.

Intentionally checks only local target existence, not web links or fragments.
"""
from pathlib import Path
from urllib.parse import unquote
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')
errors = []
SKIP_DIRS = {'.git', '.venv', 'node_modules', 'runs', 'artifacts', 'logs', 'build', 'dist'}

for markdown_file in sorted(ROOT.rglob('*.md')):
    if any(segment in SKIP_DIRS for segment in markdown_file.relative_to(ROOT).parts):
        continue
    content = markdown_file.read_text(encoding='utf-8')
    for match in LINK_RE.finditer(content):
        raw = match.group(1).strip().split(' ', 1)[0].strip('<>')
        path_str = unquote(raw.split('#', 1)[0].split('?', 1)[0])
        if not path_str or path_str.startswith(('https:', 'http:', 'mailto:', 'data:', '//')):
            continue
        target = (ROOT / path_str.lstrip('/')) if path_str.startswith('/') else (markdown_file.parent / path_str)
        target = target.resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(f'{markdown_file.relative_to(ROOT)}: missing or unsafe link: {raw}')

if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)

print('Documentation link check passed.')
