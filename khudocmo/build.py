#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path

args = sys.argv[1:]

if len(args) < 4:
    print('python3 build.py "Tên tác phẩm" "Tên tác giả" "Mô tả" /path/to/doc.md [--build-assets]')
    sys.exit(1)

BUILD_ASSETS = False
if "--build-assets" in args:
    BUILD_ASSETS = True
    args.remove("--build-assets")

TITLE, AUTHOR, DESC, DOC_PATH_RAW = args[:4]
DOC_PATH = Path(DOC_PATH_RAW).expanduser().resolve()

if not DOC_PATH.exists():
    print(f"Lỗi: Markdown file not found: {DOC_PATH}")
    sys.exit(1)

# Tệp config
SCRIPT_DIR = Path(__file__).resolve().parent
CSS_PATH = SCRIPT_DIR / "minimal.css"

# Project FILE STRUCTURE
PROJECT_DIR = DOC_PATH.parent
BASE_NAME = PROJECT_DIR.name
FILES_DIR = PROJECT_DIR / "files"
FILES_DIR.mkdir(exist_ok=True)

README_TEMPLATE_PATH = SCRIPT_DIR / "README.template.md"
LICENSE_TEMPLATE_PATH = SCRIPT_DIR / "LICENSE.md"
README_PATH = PROJECT_DIR / "README.md"
LICENSE_PATH = PROJECT_DIR / "LICENSE.md"

readme_content = README_TEMPLATE_PATH.read_text(encoding="utf-8")
license_content = LICENSE_TEMPLATE_PATH.read_text(encoding="utf-8")

readme_content = (
    readme_content
    .replace("[title]", TITLE)
    .replace("[author]", AUTHOR)
    .replace("[desc]", DESC)
    .replace("[ten-tep]", BASE_NAME)
)

LICENSE_PATH.write_text(license_content, encoding="utf-8")
README_PATH.write_text(readme_content, encoding="utf-8")


env = os.environ.copy()
env.update({
    "TITLE": TITLE,
    "AUTHOR": AUTHOR,
    "DOC_PATH": str(DOC_PATH),
    "BASE_NAME": BASE_NAME,
    "FILES_DIR": str(FILES_DIR),
    "CSS_PATH": str(CSS_PATH),
})

if BUILD_ASSETS:
    subprocess.run(
        ["bash", str(SCRIPT_DIR / "build.sh")],
        check=True,
        env=env,
        cwd=PROJECT_DIR
    )
    print("Đã build lại ebook assets")
else:
    print("Chỉ cập nhật README.md (skip build assets)")


print(f"Hoàn tất: {PROJECT_DIR}")
