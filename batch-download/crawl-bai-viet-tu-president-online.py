import os
import sys
import subprocess
import tempfile
import hashlib
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def build_page_url(base_url: str, page_num: int) -> str:
    """Tạo URL mới bổ sung hoặc cập nhật tham số ?page=N"""
    parsed = urlparse(base_url)
    query = parse_qs(parsed.query)
    query['page'] = [str(page_num)]
    
    new_query = urlencode(query, doseq=True)
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

def fetch_page_content(url: str, temp_dir: str) -> tuple[str | None, str | None]:
    """Trả về tuple: (nội dung_markdown, tên_tệp_gốc)"""
    for item in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, item))

    cmd = ["papeer", "get", url]
    try:
        subprocess.run(cmd, cwd=temp_dir, capture_output=True, text=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  [Lỗi] Không thể chạy taibaiviet cho URL: {url}\n  Chi tiết: {e}")
        return None, None

    md_files = [f for f in os.listdir(temp_dir) if f.endswith('.md')]
    if not md_files:
        return None, None

    filename = md_files[0]
    filepath = os.path.join(temp_dir, filename)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read(), filename

def remove_duplicate_headers(page_content: str, page1_top_lines: list[str]) -> str:
    """Loại bỏ các dòng tiêu đề/metadata ở đầu trang nếu trùng với Trang 1."""
    lines = page_content.strip().splitlines()
    idx = 0
    # So sánh từng dòng đầu trang N với các dòng đầu tương ứng của trang 1
    while idx < len(lines) and idx < len(page1_top_lines):
        if lines[idx].strip() == page1_top_lines[idx].strip():
            idx += 1
        else:
            break
    return "\n".join(lines[idx:]).strip()

def main():
    if len(sys.argv) < 2:
        print("Cú pháp: python taibaiviet_multi.py <URL_BÀI_VIẾT> [TÊN_TỆP_ĐẦU_RA.md]")
        sys.exit(1)

    base_url = sys.argv[1]
    # Nếu truyền tên tệp thì dùng, không thì tự lấy tên tệp gốc từ taibaiviet ở trang 1
    user_output_filename = sys.argv[2] if len(sys.argv) > 2 else None

    pages_content = []
    seen_hashes = set()
    page = 1
    max_pages = 30

    page1_top_lines = []
    default_filename = "bai_viet_full.md"

    print(f"Bắt đầu tải bài viết đa trang từ: {base_url}\n")

    with tempfile.TemporaryDirectory() as temp_dir:
        while page <= max_pages:
            current_url = base_url if page == 1 else build_page_url(base_url, page)
            print(f"-> Đang tải trang {page}: {current_url}")

            content, original_filename = fetch_page_content(current_url, temp_dir)

            if not content or not content.strip():
                print(f"   Trang {page} không có nội dung hoặc gặp lỗi. Dừng tải.")
                break

            # Trang 1: Lưu tên tệp gốc và lấy 10 dòng đầu tiên làm chuẩn so sánh
            if page == 1:
                if original_filename:
                    default_filename = original_filename
                page1_top_lines = [line for line in content.strip().splitlines() if line.strip()][:10]

            # Trang 2 trở đi: Lọc bỏ phần tiêu đề trùng lặp ở đầu trang
            if page > 1 and page1_top_lines:
                cleaned_content = remove_duplicate_headers(content, page1_top_lines)
            else:
                cleaned_content = content.strip()

            content_hash = hashlib.md5(cleaned_content.encode('utf-8')).hexdigest()
            if content_hash in seen_hashes:
                print(f"   Trang {page} có nội dung trùng lặp. Dừng tải.")
                break

            seen_hashes.add(content_hash)
            pages_content.append(cleaned_content)
            page += 1

    # Tên tệp đầu ra cuối cùng
    output_filename = user_output_filename or default_filename

    if pages_content:
        full_markdown = "\n\n---\n\n".join(pages_content)
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(full_markdown)
        print(f"\n[Hoàn tất] Đã gộp {len(pages_content)} trang vào tệp: {output_filename}")
    else:
        print("\n[Thất bại] Không tải được nội dung bài viết.")

if __name__ == "__main__":
    main()