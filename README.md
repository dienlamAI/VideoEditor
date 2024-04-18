# VideoEditor

VideoEditor là công cụ chỉnh sửa video tự động, sử dụng thư viện MoviePy để thực hiện các tác vụ biên tập video dựa trên yêu cầu của người dùng. Tính năng nổi bật bao gồm khả năng trích xuất và thêm subtitle vào video một cách nhanh chóng và dễ dàng. VideoEditor hỗ trợ công nghệ AI tiên tiến từ OpenAI và có thể sử dụng WhisperModel để thực hiện các tác vụ liên quan đến ngôn ngữ.

## Tính Năng

- Trích xuất text từ subtitle của video.
- Thêm subtitle vào video.
- Sử dụng AI để cải thiện và tối ưu hóa quá trình biên tập video.
- Edit video 1 cách nhanh chóng theo yêu cầu của người dùng

## Cài Đặt

Để sử dụng VideoEditor, hãy thực hiện theo các bước dưới đây:

### Bước 1: Clone Repository

```bash
git clone https://github.com/DienStudio/VideoEditor.git
```

### Bước 2: Tạo Môi Trường Ảo

Di chuyển vào thư mục VideoEditor:

```bash
cd VideoEditor
```

Tạo môi trường ảo:

```bash
python -m venv .venv
```

### Bước 3: Kích Hoạt Môi Trường Ảo

```bash
.venv\Scripts\activate
```

### Bước 4: Cài Đặt Các Gói Phụ Thuộc

```bash
pip install -r requirements.txt
```

### Bước 5: Chạy Ứng Dụng

```bash
py main.py
```

## Lưu ý

- Đảm bảo đã tải và cài đặt `magick.exe`. Gán đường link tới `IMAGEMAGICK_BINARY` trong file cấu hình để sử dụng các tính năng liên quan đến hình ảnh.

- Nếu không thể sử dụng OpenAI, bạn có thể thay thế bằng WhisperModel. Tuy nhiên, lưu ý rằng việc này có thể tốn nhiều thời gian hơn.
