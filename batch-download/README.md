# Danh sách scripts để tải

## `crawl-bai-viet-tu-spiderum.py`

Bước 1: Cài đặt các thư viện Python cần thiết:

```bash
pip install playwright beautifulsoup4 markdownify requests

```

Bước 2: Tải trình duyệt Firefox tích hợp sẵn cho Playwright:

```bash
playwright install firefox

```

Hướng dẫn sử dụng đơn giản:

Tải 1 bài viết đơn lẻ:

```bash
python crawl.py "https://web.archive.org/web/.../https://spiderum.com/bai-dang/..."

```

Tải hàng loạt bài viết (đặt các URL vào file `links.txt`, mỗi dòng 1 link):

```bash
python crawl.py links.txt

```

Output sẽ kiểu như này"

- File bài viết: `<ten_bai_viet_khong_dau>.md`
- Hình ảnh đính kèm: `assets/<ten_bai_viet_khong_dau>/<ten_anh>.jpg` (đường dẫn ảnh trong file Markdown sẽ tự động trỏ về thư mục local này).
