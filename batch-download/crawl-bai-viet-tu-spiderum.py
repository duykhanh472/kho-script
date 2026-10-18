import sys
import re
import time
from pathlib import Path
from urllib.parse import urlparse
import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from markdownify import markdownify
import unicodedata # 👈 Thêm thư viện này ở đầu file

# ------------------ Helpers ------------------

def convert_to_raw_archive_url(url: str) -> str:
    """
    Tự động chèn 'id_' vào URL Wayback Machine để lấy thẳng HTML gốc, 
    bỏ qua khung Banner JS và né lỗi 404 giả.
    """
    # Tìm chuỗi 14 chữ số thời gian và chèn 'id_' vào sau nếu chưa có
    pattern = r'(/web/\d{14})(?!id_)(/)'
    if 'web.archive.org' in url and re.search(pattern, url):
        return re.sub(pattern, r'\1id_\2', url)
    return url

def clean_archive_url(url: str) -> str:
    """
    Bóc tách URL gốc khỏi URL của Wayback Machine
    Ví dụ: https://web.archive.org/web/20250909222428im_/https://[URL] -> https://[URL]
    """
    if not url:
        return ""
    match = re.search(r'/web/\d+(?:[a-z_]+)?/(https?://.*)', url)
    if match:
        return match.group(1)
    return url


def ext_from_content_type(ct: str) -> str:
    """Xác định đuôi file dựa trên Content-Type"""
    if not ct:
        return ".img"
    ct = ct.lower()
    if "jpeg" in ct or "jpg" in ct:
        return ".jpg"
    if "png" in ct:
        return ".png"
    if "webp" in ct:
        return ".webp"
    if "gif" in ct:
        return ".gif"
    if "svg" in ct:
        return ".svg"
    return ".img"


def filename_from_url(url: str) -> str | None:
    """Lấy tên file từ URL nếu có chứa phần mở rộng hợp lệ"""
    name = Path(urlparse(url).path).name
    if "." in name and len(name.split(".")[-1]) <= 5:
        return name
    return None


def remove_vietnamese_accent(text: str) -> str:
    """Loại bỏ dấu tiếng Việt khỏi chuỗi văn bản"""
    text = text.replace('Đ', 'D').replace('đ', 'd')
    normalized = unicodedata.normalize('NFD', text)
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')


def sanitize_filename(name: str) -> str:
    """
    Chuyển tên bài viết thành dạng Slug chuẩn: 
    Ví dụ: 'Tại sao ông bà...?' -> 'tai_sao_ong_ba'
    """
    # 1. Bỏ dấu tiếng Việt
    text = remove_vietnamese_accent(name)
    # 2. Chuyển thành chữ thường
    text = text.lower()
    # 3. Thay các ký tự đặc biệt & khoảng trắng thành dấu gạch dưới (_)
    text = re.sub(r'[^a-z0-9_-]', '_', text)
    # 4. Gộp nhiều dấu '_' liên tiếp thành 1 dấu '_'
    text = re.sub(r'_+', '_', text)
    # 5. Xóa dấu '_' thừa ở đầu và cuối
    cleaned = text.strip('_')
    
    return cleaned if cleaned else "bai_viet_khong_ten"

# ------------------ Image Downloader ------------------

def process_and_download_images(md_text: str, base_name: str, base_dir: Path = Path(".")) -> str:
    """
    Tìm tất cả URL ảnh trong bài Markdown, tải về thư mục assets/<base_name>/
    và thay thế đường dẫn trong Markdown thành đường dẫn tương đối local.
    """
    assets_dir = base_dir / "assets" / base_name
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Tìm các link ảnh dạng Markdown ![alt](url) hoặc HTML <img src="url">
    md_img_pattern = re.compile(r'!\[[^\]]*\]\((https?://[^)]+)\)')
    html_img_pattern = re.compile(r'<img[^>]+src=["\'](https?://[^"\']+)["\']')

    urls = list(dict.fromkeys(md_img_pattern.findall(md_text) + html_img_pattern.findall(md_text)))

    if not urls:
        print(f"  [i] Không tìm thấy ảnh nào trong bài '{base_name}'.")
        return md_text

    print(f"  [i] Tìm thấy {len(urls)} ảnh. Bắt đầu tải...")

    counter = 1
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for url in urls:
        # Đảm bảo URL đã được làm sạch Wayback prefix
        clean_url = clean_archive_url(url)
        filename = filename_from_url(clean_url)

        # Nếu đã đoán được filename, kiểm tra xem đã tồn tại local chưa
        if filename:
            local_path = assets_dir / filename
            local_ref = f"assets/{base_name}/{filename}"

            if local_path.exists() and local_path.stat().st_size > 0:
                print(f"   ✓ Đã có sẵn: {filename} (bỏ qua download)")
                md_text = md_text.replace(url, local_ref)
                continue

        # Tiến hành tải ảnh từ URL gốc
        try:
            r = requests.get(clean_url, headers=headers, timeout=20)
            r.raise_for_status()
        except Exception as e:
            print(f"   ⚠ Không thể tải ảnh từ {clean_url}: {e}")
            continue

        # Nếu chưa có filename thì sinh tên file theo Content-Type
        if not filename:
            ext = ext_from_content_type(r.headers.get("Content-Type", ""))
            filename = f"{base_name}-{counter}{ext}"
            counter += 1

        local_path = assets_dir / filename
        local_ref = f"assets/{base_name}/{filename}"

        if not local_path.exists() or local_path.stat().st_size == 0:
            print(f"   ↓ Đã tải: {filename}")
            local_path.write_bytes(r.content)

        # Cập nhật đường dẫn URL cũ trong Markdown thành relative path local
        md_text = md_text.replace(url, local_ref)

    return md_text


# ------------------ HTML to Markdown Converter ------------------

def html_to_markdown(html_content: str) -> str:
    """Làm sạch HTML của Editor.js/Angular và chuyển đổi sang Markdown"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # 🛑 BƯỚC MỚI: Xóa bỏ phần thẻ tags bài viết (.tags-wrapper) và toàn bộ nội dung bên trong nó
    for tags_div in soup.select('.tags-wrapper'):
        tags_div.decompose()

    # 1. Chuyển các thẻ <div class="ce-paragraph"> thành thẻ <p>
    for para in soup.find_all('div', class_='ce-paragraph'):
        para.name = 'p'

    # 2. Xử lý Ảnh và Caption
    for img_container in soup.find_all('div', class_='image-tool__image'):
        img_tag = img_container.find('img')
        caption_tag = img_container.find('div', class_='image-tool__caption')

        if img_tag:
            img_tag['src'] = clean_archive_url(img_tag.get('src', ''))

            if caption_tag and caption_tag.text.strip():
                img_tag['alt'] = caption_tag.text.strip()

            img_container.replace_with(img_tag)

    # 3. Làm sạch các link
    for a_tag in soup.find_all('a'):
        if a_tag.get('href'):
            a_tag['href'] = clean_archive_url(a_tag.get('href'))

    # 4. Convert sang Markdown
    md_text = markdownify(str(soup), heading_style="ATX", strip=['script', 'style'])
    return md_text

# ------------------ Article Crawler ------------------

def crawl_single_article(page, url: str) -> bool:
    # 🛑 BƯỚC MỚI: Tự động chuyển URL sang dạng RAW để né lỗi 404 giả
    target_url = convert_to_raw_archive_url(url)
    print(f"\n[➔] Đang xử lý: {target_url}")

    max_retries = 4
    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                wait_time = 5 * attempt
                print(f"  [🔄] Thử kết nối lại lần {attempt}/{max_retries} sau {wait_time}s...")
                time.sleep(wait_time)

            # Tải trang bằng URL RAW
            response = page.goto(target_url, timeout=90000, wait_until="domcontentloaded")

            # Kiểm tra lỗi 503, 429 hoặc 404 từ archive
            if response and response.status in [503, 429, 404] and attempt < max_retries:
                print(f"  [⚠️] Máy chủ phản hồi mã {response.status}. Đang thử lại...")
                continue

            break

        except Exception as e:
            if attempt == max_retries:
                print(f"  [❌] Lỗi khi kết nối tới trang: {e}")
                return False
            print(f"  [⚠️] Lỗi mạng/Timeout, đang chờ để thử lại...")

    # BẮT ĐẦU TÌM NỘI DUNG
    try:
        selectors_to_try = ['#post-content', 'article', 'main']
        content_element = None

        for sel in selectors_to_try:
            try:
                page.wait_for_selector(sel, timeout=5000)
                content_element = page.query_selector(sel)
                if content_element:
                    print(f"  [i] Đã tìm thấy nội dung qua thẻ '{sel}'")
                    break
            except Exception:
                continue

        if not content_element:
            print("  [❌] Thất bại: Không tìm thấy khung bài viết (Thử kiểm tra lại giao diện trình duyệt).")
            return False

        # Lấy tiêu đề bài viết
        raw_title = page.title() or "Bai_viet"
        raw_title = re.sub(r'\s*(\||-|–).*$', '', raw_title).strip()
        title = sanitize_filename(raw_title)

        # Trích xuất HTML & Convert sang Markdown
        content_html = content_element.inner_html()
        md_body = html_to_markdown(content_html)
        full_md = f"# {raw_title}\n\n" + md_body

        # Tải ảnh và lưu file
        full_md_with_local_images = process_and_download_images(full_md, base_name=title)
        md_filename = f"{title}.md"
        Path(md_filename).write_text(full_md_with_local_images, encoding="utf-8")

        print(f"  [✔] Thành công! Đã lưu: {md_filename}")
        return True

    except Exception as e:
        print(f"  [❌] Lỗi xử lý dữ liệu: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Cú pháp sử dụng:")
        print("  1. Tải 1 link trực tiếp : python crawl.py <URL>")
        print("  2. Tải nhiều links từ file: python crawl.py links.txt")
        sys.exit(1)

    arg_input = sys.argv[1].strip()
    urls_to_process = []

    input_path = Path(arg_input)
    if input_path.is_file():
        lines = input_path.read_text(encoding="utf-8").splitlines()
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                urls_to_process.append(line)
        print(f"[*] Đã đọc được {len(urls_to_process)} links từ file '{arg_input}'.")
    else:
        urls_to_process.append(arg_input)

    if not urls_to_process:
        print("[!] Không tìm thấy URL hợp lệ nào để xử lý.")
        sys.exit(1)

    print(f"[*] Khởi động Playwright Firefox (Bản tích hợp sẵn)...")
    total = len(urls_to_process)
    success_count = 0

    with sync_playwright() as p:
        # 🛑 DÙNG FIREFOX CÓ SẴN (Không cần cài Chrome ngoài)
        browser = p.firefox.launch(
            headless=False
        )

        # Giả lập Firefox trên Windows
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            viewport={"width": 1920, "height": 1080},
            extra_http_headers={
                "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            }
        )

        page = context.new_page()

        for idx, url in enumerate(urls_to_process, start=1):
            print("\n==========================================")
            print(f" Tiến trình: [{idx}/{total}]")
            print("==========================================")

            ok = crawl_single_article(page, url)
            if ok:
                success_count += 1

            if idx < total:
                time.sleep(3)

        time.sleep(2)
        browser.close()

    print("\n==========================================")
    print(f"🎉 TỔNG KẾT: Hoàn thành {success_count}/{total} bài viết!")
    print("==========================================")


if __name__ == "__main__":
    main()
