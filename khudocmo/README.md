# Template cho Khu đọc mở

Để tạo sách này kia

## Tạo sách

Script `build.py` này sẽ được sử dụng để tạo sách (Bao gồm các định dạng sách điện tử: `epub`, `azw3`, `html`, `mobi`, `txt`) cũng như tệp `README.md` (Tệp lưu trữ thông tin cơ bản của sách) cho mỗi thư mục sách tương ứng.


```bash
python3 build.py "Tên tác phẩm" "Tên tác giả" "Mô tả" /path/to/doc.md [--build-assets]
```

Trong mỗi một thư mục tác phẩm thì thường sẽ bao gồm:

```bash
vu-trong-phung_so-do$ tree
.
├── doc.md
├── files
│   ├── vu-trong-phung_so-do.azw3
│   ├── vu-trong-phung_so-do.epub
│   └── vu-trong-phung_so-do.html
├── LICENSE
└── README.md

```

Tệp `doc.md` chính là tệp văn bản thuần (plain-text) viết bằng cú pháp Markdown cho toàn bộ tác phẩm.

### Hướng dẫn tạo sách

Bạn `clone` repo `template` này về:

```
git clone https://github.com/khudocmo/template.git
# Di chuyển vào thư mục này
cd template/
```

Rồi sau đó chạy lệnh:

```
# Lệnh mẫu thôi nhé
python3 build.py "Tên tác phẩm" "Tên tác giả" "Mô tả" ~/Projects/khudocmo/vu-trong-phung/so-do/doc.md [--build-assets]

# `~/Projects/khudocmo/vu-trong-phung/so-do/doc.md` chính là `path` đầy đủ của tệp `doc.md`
```

Và thế là xong (Hơi phức tạp chút tại mình viết khá tạp nham nên thư mục `template` này dùng cả đống tệp linh tinh để xử lý các phần khác tự động)

(Thực ra là còn một số lỗi liên quan đến xử lý các tệp hình ảnh của sách nhưng mà lười quá nên chưa sửa :>)
