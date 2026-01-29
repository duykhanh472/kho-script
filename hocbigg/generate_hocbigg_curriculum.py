#!/usr/bin/env python3

import argparse
import re
import shutil
import yaml
import markdown

from pathlib import Path

# -----------------------
# CLI
# -----------------------

parser = argparse.ArgumentParser()
parser.add_argument("page", help="Root folder / repo name")
args = parser.parse_args()

SCRIPT_DIR = Path(__file__).parent.resolve()

PAGE = args.page.strip("/").strip()

ROOT = Path.cwd() / PAGE
OUT = ROOT / "out"

TEMPLATE = SCRIPT_DIR / "page-template.html"
STYLE = SCRIPT_DIR / "style.css"
ASSETS = ROOT / "assets"

OUT.mkdir(exist_ok=True)

# -----------------------
# Markdown engine
# -----------------------

md = markdown.Markdown(
    extensions=["tables", "fenced_code", "footnotes", "toc"],
)

template_html = TEMPLATE.read_text(encoding="utf-8")

# -----------------------
# Front matter
# -----------------------

def parse_front_matter(text):
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        meta = yaml.safe_load(fm) or {}
        return meta, body.strip()
    return {}, text

def extract_h1(markdown_text):
    lines = markdown_text.lstrip().splitlines()
    if not lines:
        return None

    first = lines[0].strip()
    if first.startswith("# "):
        return first[2:].strip()

    return None

# -----------------------
# Rewrite .md → .html
# -----------------------

def rewrite_md_links(html):
    return re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', html)

def add_target_blank_external_links(html):
    return re.sub(
        r'<a\s+(?![^>]*target=)[^>]*href="(https?://[^"]+)"',
        r'<a target="_blank" rel="noopener noreferrer" href="\1"',
        html
    )

# -----------------------
# NAV generation
# -----------------------

NAV_FILES = [
    ("advanced_topics.md", "Advanced Topics"),
    ("projects.md", "Projects"),
    ("extras/courses.md", "Extra Courses"),
    ("extras/readings.md", "Extra Reading"),
    ("extras/curricula.md", "Extra Curricula"),
]

def build_nav():
    items = []
    items.append(f'<a href="/">Hocbigg</a>')
    label = PAGE.replace("_", " ").title()
    items.append(f'<a href="/{PAGE}/">{label}</a>')

    for md_path, label in NAV_FILES:
        full = ROOT / md_path
        if full.exists():
            html_path = md_path.replace(".md", ".html")
            items.append(f'<a href="/{PAGE}/{html_path}">{label}</a>')

    items.append(f'<a href="https://github.com/hocbigg/{PAGE}/" target="_blank">View on Github</a>')

    return "\n".join(items)

NAV_HTML = build_nav()

PAGE_HEADER = """
<header class="page-header">
  <img src="/images/logo.png" alt="">
  <h1>{{title}}</h1>
</header>
"""

# -----------------------
# Copy static
# -----------------------

if STYLE.exists():
    shutil.copy2(STYLE, OUT / STYLE.name)

if ASSETS.exists():
    shutil.copytree(ASSETS, OUT / "assets", dirs_exist_ok=True)

# -----------------------
# Build
# -----------------------

for md_path in ROOT.rglob("*.md"):

    is_readme = md_path.name.lower() == "readme.md"

    # Skip output folder
    if OUT in md_path.parents:
        continue

    # Skip assets
    if "assets" in md_path.parts:
        continue

    rel = md_path.relative_to(ROOT)

    if md_path.name.lower() == "readme.md":
        out_path = OUT / "index.html"
    else:
        out_path = (OUT / rel).with_suffix(".html")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    raw = md_path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(raw)

    md.reset()
    html_body = md.convert(body)
    html_body = rewrite_md_links(html_body)
    html_body = add_target_blank_external_links(html_body)

    if "title" in meta:
        title = meta["title"]
    else:
        h1 = extract_h1(body)
        title = h1 if h1 else md_path.stem.replace("_", " ").title()

    description = meta.get("description", "")
    author = meta.get("author", "hocbigg")
    language = meta.get("language", "en")

    header_html = PAGE_HEADER if is_readme else ""

    page = (
        template_html
        .replace("{{header}}", header_html)
        .replace("{{title}}", title)
        .replace("{{description}}", description)
        .replace("{{author}}", author)
        .replace("{{language}}", language)
        .replace("{{nav-bar}}", NAV_HTML)
        .replace("{{content}}", html_body)
        .replace("{{page}}", PAGE)
    )

    out_path.write_text(page, encoding="utf-8")

    print(f"✔ {rel} → {out_path.relative_to(ROOT)}")

print("Build finished.")
