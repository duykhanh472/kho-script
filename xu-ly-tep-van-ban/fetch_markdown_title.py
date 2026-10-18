import os

BASE_DIR = os.getcwd()
CONTENT_DIR = os.path.join(BASE_DIR, 'content')


def is_markdown_file(filename: str) -> bool:
    return filename.lower().endswith('.md')


def extract_title(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()

    # Loại bỏ ký tự heading Markdown (#)
    return first_line.lstrip('#').strip()


def to_relative_path(path: str) -> str:
    return os.path.relpath(path, BASE_DIR).replace(os.sep, '/')


def main():
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if not is_markdown_file(file):
                continue

            file_path = os.path.join(root, file)
            title = extract_title(file_path)

            if not title:
                continue

            rel_path = to_relative_path(file_path)
            print(f'- [{title}]({rel_path})')


if __name__ == '__main__':
    main()
