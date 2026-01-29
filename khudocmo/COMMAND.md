# Hướng dẫn xử lý và tạo sách điện tử

## Thông tin cơ bản

### Cấu trúc thư mục cho trang web

Trong thư mục docs sẽ có những tệp sau:

- `index.html`: Trang HTML chính - giới thiệu sách cũng như thông tin về sách và đường dẫn tải xuống.
- Trong thư mục `files` sẽ bao gồm:
    - `.epub`: Được tạo bằng `pandoc`.
    - `.azw3`: Được tạo bằng Calibre (`ebook-convert`).
    - `.html`: Được tạo bằng `pandoc`.

Toàn bộ các lệnh chạy đều được lưu trữ ở tệp [COMMAND.md](COMMAND.md)

### Viết một script xử lý

Chạy lệnh

```
python3 build.py
```

## Chuyển đổi, định dạng và xử lý nội dung ban đầu

### Chuyển từ EPUB gốc sang Markdown

```
pandoc [ten-tep].epub -o doc.md --wrap=none --extract-media=assets --to=commonmark_x+footnotes --standalone --lua-filter=clean-attrs.lua
```

### Dọn sạch đống dấu cách bị thừa trong tệp EPUB

Sử dụng Regex này

```
^\s+|\s+$|\s+(?=\s)
```

## Tạo EPUB + AZW3 + HTML

### Trước khi bắt đầu

Find and Replace toàn bộ những Fields sau (Có cách nào để find and replace nhanh trong thư mục hiện tại không? Các field mình liệt kê dưới đây mình đang cân nhắc đặt vào trong tệp config: `khudocmo.yml`):

- `[title]`: Tên tác phẩm
- `[author]`: Tên tác giả
- `[desc]`: Mô tả
- `[ten-tep]`: Tên tác phẩm theo kiểu URL (Ví dụ: Ngày xuân thì thành `ngay-xuan`, nếu có thể chuyển đổi tự động bằng code luôn thì càng tốt)

### Chuyển đổi nhanh

```
python3 build.py "Title" "Author" "Description" "Path"
```
### Chuyển đổi từ Markdown sang EPUB

```
pandoc doc.md -f markdown -t epub -s -o [ten-tep].epub \
	--metadata title="[title]" \
	--metadata author="[author]" \
	--metadata language="vi" \
  --css="minimal.css"
```

### Chuyển đổi từ EPUB sang AZW3

Mình sử dụng `ebook-convert` của Calibre.

```
ebook-convert [ten-tep].epub [ten-tep].azw3
```

### Chuyển đổi từ Markdown sang HTML

```
pandoc doc.md -s -o [ten-tep].html
```