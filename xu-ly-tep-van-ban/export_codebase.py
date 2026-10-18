#!/usr/bin/env python3
"""
Codebase to AI Prompt Exporter
- Uses only Python Standard Library.
- Filters out .gitignore patterns, binary files, build artifacts, and oversized files.
- Generates a visual Directory Tree.
- Bundles code with syntax highlighting tags into an English AI Prompt.
"""

import argparse
import fnmatch
import os
import sys
from pathlib import Path

# ==============================================================================
# CONFIGURATION
# ==============================================================================

DEFAULT_OUTPUT_FILE = "codebase_prompt.txt"
DEFAULT_MAX_FILE_SIZE_KB = 500  # Skip files larger than 500 KB

# Folders to skip by default (Python, JS/TS, Rust, IDEs, etc.)
DEFAULT_IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    ".next",
    ".nuxt",
    "dist",
    "build",
    "target",  # Rust build directory
    ".venv",
    "venv",
    "env",
    ".idea",
    ".vscode",
}

# Specific noisy/lock files to skip (huge token waste)
DEFAULT_IGNORED_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Cargo.lock",
    "poetry.lock",
    "Pipfile.lock",
}

# Common binary extensions
BINARY_EXTENSIONS = {
    # Images & Media
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".tiff", ".svg",
    ".mp3", ".wav", ".ogg", ".mp4", ".avi", ".mov", ".mkv",
    # Archives & Binaries
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar", ".iso",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".pyc", ".pyd", ".class", ".wasm",
    # Documents & Fonts
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    # Databases
    ".db", ".sqlite", ".sqlite3",
}

# Mapping file extensions to Markdown syntax highlighters
EXTENSION_LANG_MAP = {
    # Python
    ".py": "python",
    ".pyw": "python",
    # Web (HTML/CSS/JS/TS)
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "scss",
    ".sass": "sass",
    ".less": "less",
    ".js": "javascript",
    ".jsx": "jsx",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".vue": "vue",
    ".svelte": "svelte",
    # Rust
    ".rs": "rust",
    # Configs & Data
    ".json": "json",
    ".toml": "toml",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".xml": "xml",
    ".sql": "sql",
    ".md": "markdown",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".env.example": "dotenv",
}


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

class GitIgnoreFilter:
    """Parses and matches .gitignore rules using standard library fnmatch."""
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir.resolve()
        self.patterns = []
        self._load_gitignore()

    def _load_gitignore(self):
        gitignore_path = self.root_dir / ".gitignore"
        if gitignore_path.exists():
            try:
                with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            self.patterns.append(line)
            except Exception as e:
                print(f"Warning: Could not read .gitignore: {e}", file=sys.stderr)

    def is_ignored(self, path: Path) -> bool:
        try:
            rel_path = path.resolve().relative_to(self.root_dir).as_posix()
            parts = path.resolve().relative_to(self.root_dir).parts
        except ValueError:
            return False

        # Check default ignored folders & files
        for part in parts:
            if part in DEFAULT_IGNORED_DIRS:
                return True
        if path.name in DEFAULT_IGNORED_FILES:
            return True

        # Match .gitignore patterns
        for pattern in self.patterns:
            pat = pattern.rstrip("/")
            if fnmatch.fnmatch(path.name, pat):
                return True
            if fnmatch.fnmatch(rel_path, pat) or fnmatch.fnmatch(rel_path, f"*/{pat}"):
                return True
            for part in parts:
                if fnmatch.fnmatch(part, pat):
                    return True
        return False


def is_binary_file(file_path: Path) -> bool:
    """Checks if a file is binary by extension or by inspecting the first 1KB."""
    if file_path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            if b"\x00" in chunk:
                return True
    except Exception:
        return True
    return False


def generate_tree(dir_path: Path, prefix: str = "", git_filter: GitIgnoreFilter = None, max_size_kb: int = DEFAULT_MAX_FILE_SIZE_KB, output_file_name: str = "") -> list:
    """Generates an ASCII directory tree."""
    lines = []
    try:
        entries = sorted(list(dir_path.iterdir()), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        return lines

    # Filter out ignored entries
    valid_entries = []
    for entry in entries:
        if entry.name == output_file_name:
            continue
        if git_filter and git_filter.is_ignored(entry):
            continue
        if entry.is_file():
            if is_binary_file(entry):
                continue
            if entry.stat().st_size > max_size_kb * 1024:
                continue
        valid_entries.append(entry)

    count = len(valid_entries)
    for i, entry in enumerate(valid_entries):
        is_last = (i == count - 1)
        connector = "└── " if is_last else "├── "
        if entry.is_dir():
            lines.append(f"{prefix}{connector}{entry.name}/")
            sub_prefix = prefix + ("    " if is_last else "│   ")
            lines.extend(generate_tree(entry, sub_prefix, git_filter, max_size_kb, output_file_name))
        else:
            lines.append(f"{prefix}{connector}{entry.name}")
    return lines


def get_language(file_path: Path) -> str:
    """Returns markdown language identifier for syntax highlighting."""
    return EXTENSION_LANG_MAP.get(file_path.suffix.lower(), "")


# ==============================================================================
# MAIN PROCESSING
# ==============================================================================

def build_prompt(project_root: Path, output_file: Path, max_size_kb: int):
    git_filter = GitIgnoreFilter(project_root)
    output_filename = output_file.name

    print(f"[*] Scanning project directory: {project_root.resolve()}")
    
    # 1. Generate Directory Tree
    print("[*] Generating directory tree...")
    tree_lines = [f"{project_root.name}/"]
    tree_lines.extend(generate_tree(project_root, prefix="", git_filter=git_filter, max_size_kb=max_size_kb, output_file_name=output_filename))
    directory_tree_str = "\n".join(tree_lines)

    # 2. Collect Valid Files
    print("[*] Collecting source code files...")
    collected_files = []
    for root, dirs, files in os.walk(project_root):
        current_dir = Path(root)
        # Prune ignored directories in-place for efficiency
        dirs[:] = [d for d in dirs if not git_filter.is_ignored(current_dir / d) and d != output_filename]
        
        for file in sorted(files):
            file_path = current_dir / file
            if file == output_filename:
                continue
            if git_filter.is_ignored(file_path):
                continue
            if is_binary_file(file_path):
                continue
            try:
                if file_path.stat().st_size > max_size_kb * 1024:
                    print(f"    [-] Skipped oversized file (> {max_size_kb}KB): {file_path.relative_to(project_root)}")
                    continue
            except OSError:
                continue

            collected_files.append(file_path)

    # 3. Build English System Prompt Header
    prompt_content = []
    prompt_content.append("# SYSTEM INSTRUCTION & CONTEXT INGESTION")
    prompt_content.append("""You are an expert software engineer and AI assistant.
Below is the complete context and codebase for this project.

## Your Tasks:
1. Carefully review, analyze, and internalize the project architecture, directory structure, module interactions, dependencies, coding conventions, and overall logic.
2. Do NOT execute, refactor, or rewrite any code immediately.
3. Acknowledge that you have successfully ingested and understood this codebase by providing:
   - A concise high-level overview of what the project does.
   - The identified technology stack and key dependencies.
   - A summary of the core modules/components.
4. State that you are ready to answer subsequent questions, debug, or implement new features based on this codebase.

---

## 1. Project Directory Structure
```text
""" + directory_tree_str + """
```

---

## 2. Codebase Files
""")

    # 4. Append File Contents
    for file_path in collected_files:
        rel_path = file_path.relative_to(project_root).as_posix()
        lang = get_language(file_path)
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                file_content = f.read()

            prompt_content.append(f"### File: `{rel_path}`")
            prompt_content.append(f"")
            prompt_content.append(f"```{lang}\n{file_content}\n```\n")
        except Exception as e:
            print(f"Warning: Could not read file {rel_path}: {e}", file=sys.stderr)

    # 5. Write to Output File
    output_path = project_root / output_file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(prompt_content))

    print(f"\n[+] Successfully exported {len(collected_files)} files into: {output_path.resolve()}")
    print(f"[+] Output size: {output_path.stat().st_size / 1024:.2f} KB")


def main():
    help_epilog = """
HƯỚNG DẪN SỬ DỤNG / USAGE EXAMPLES:

1. Chạy mặc định (quét thư mục hiện tại, xuất ra codebase_prompt.txt):
   python export_codebase.py

2. Chỉ định thư mục dự án và tên file output tùy ý:
   python export_codebase.py /path/to/my-project -o my_prompt.txt

3. Tùy chỉnh giới hạn kích thước file (ví dụ: chỉ lấy file <= 300 KB):
   python export_codebase.py --max-size 300

4. Kết hợp tất cả tùy chọn:
   python export_codebase.py ../my-rust-app -o rust_context.txt --max-size 200
"""

    parser = argparse.ArgumentParser(
        description="Convert entire codebase into a single AI context prompt.",
        epilog=help_epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter  # Giúp giữ nguyên format xuống dòng của epilog
    )
    
    parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Path to project root directory (default: current directory)"
    )
    parser.add_argument(
        "-o", "--output", 
        default=DEFAULT_OUTPUT_FILE, 
        help=f"Output prompt file name (default: {DEFAULT_OUTPUT_FILE})"
    )
    parser.add_argument(
        "--max-size", 
        type=int, 
        default=DEFAULT_MAX_FILE_SIZE_KB, 
        help=f"Max file size in KB to include (default: {DEFAULT_MAX_FILE_SIZE_KB} KB)"
    )

    args = parser.parse_args()
    project_dir = Path(args.path).resolve()

    if not project_dir.is_dir():
        print(f"Error: Path '{project_dir}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    build_prompt(project_root=project_dir, output_file=Path(args.output), max_size_kb=args.max_size)

if __name__ == "__main__":
    main()