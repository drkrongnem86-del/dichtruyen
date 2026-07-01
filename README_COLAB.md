# Build APK trên Google Colab — Tính Dịch Truyền

Hướng dẫn build APK Android cho app "Tính Dịch Truyền" bằng **Google Colab** — không cần cài WSL/Docker trên máy Windows.

## 📁 Files cần thiết

| File | Mô tả |
|------|-------|
| `kivy_app.py` | Code app Kivy (chuyển từ Tkinter sang) |
| `buildozer.spec` | Config build (version, package name, requirements...) |
| `Build_APK_Colab.ipynb` | Notebook Colab chạy từng bước |
| `main.py` | App Tkinter gốc (Windows .exe) — KHÔNG dùng cho APK |

## 🚀 Cách build — 5 bước

### Bước 0: Mở Colab
Truy cập [colab.research.google.com](https://colab.research.google.com) → **File → Upload notebook** → chọn `Build_APK_Colab.ipynb`.

### Bước 1: Cài môi trường
Chạy cell "Bước 1" — mất 2-3 phút. Cài Java 17 + buildozer + cython.

### Bước 2: Upload file
Chạy cell "Bước 2" — chọn **cả 2 file** `kivy_app.py` và `buildozer.spec` từ thư mục workspace.

### Bước 3: Accept licenses
Chạy cell "Bước 3" — tự động chấp nhận Android SDK licenses.

### Bước 4: Build APK
Chạy cell "Bước 4" — **mất 30-45 phút lần đầu** (tải SDK + NDK + compile Kivy).

> ⚠️ **Quan trọng**: Mở thêm 1 tab Chrome bất kỳ để Colab không disconnect.

### Bước 5: Download APK
Chạy cell "Bước 5" — tự động tìm file APK và mở hộp thoại download.

## 📱 Cài APK lên điện thoại

1. Copy file `tindichtruyen-1.0.0-debug.apk` vào điện thoại (USB / email / Google Drive).
2. Mở file APK bằng trình quản lý file.
3. Bấm **Cài đặt** → nếu Android hỏi "Cho phép cài từ nguồn này?" → bật lên.
4. App xuất hiện trong màn hình chính với tên **"Tính Dịch Truyền"**.

## 🔧 Troubleshooting

### Build fail ở "pyjnius not found"
Nguyên nhân: pypi chỉ release pyjnius đến 1.6.x, không có 1.7.0. Fix: mở `buildozer.spec`, dòng:
```
requirements = python3==3.11.6, kivy==2.3.0, cython==0.29.36
```
Bỏ `python3==3.11.6` đi (để buildozer tự chọn), upload lại, build lại.

### Build fail ở "libtinfo5 not found"
Nguyên nhân: Ubuntu 22+ không có `libtinfo5`. Fix: thêm cell cài lib tương đương:
```python
!apt install -y -qq libtinfo5 libncurses5 2>&1 | tail -3
```

### APK build xong nhưng app crash khi mở
Nguyên nhân: code Kivy lỗi runtime. Test trước trên desktop:
```bash
pip install kivy
python kivy_app.py
```
Sửa lỗi trước rồi upload lại.

### Colab disconnect giữa chừng
- Mở thêm tab Chrome khác (bất kỳ) — Colab sẽ giữ session.
- Nếu vẫn disconnect, mở session mới và chạy lại từ Bước 2 (cache buildozer vẫn còn nếu chưa xóa runtime).

## 📊 So sánh các phương pháp

| Phương pháp | Thời gian lần đầu | Disk cần | Khó? |
|-------------|---------------------|----------|------|
| **Google Colab** ⭐ | 30-45 phút | 0 (dùng Colab) | Dễ |
| GitHub Actions | 30-45 phút | 0 | Trung bình |
| WSL local | 30-45 phút | ~10 GB | Khó (cần cài WSL) |
| Docker local | 30-45 phút | ~15 GB | Khó (cần cài Docker) |
| Linux native | 30-45 phút | ~10 GB | Khó (cần máy Linux) |

→ **Colab là lựa chọn tốt nhất** cho người không muốn cài gì trên máy.

## 🔄 Cập nhật app

Sau khi sửa `kivy_app.py`:
1. Mở lại notebook
2. Chạy lại Bước 2 → Bước 4 → Bước 5
3. Buildozer sẽ detect file mới và build lại nhanh hơn (10-15 phút do có cache).

## 📞 Hỗ trợ

Nếu gặp lỗi:
1. Chạy cell "Troubleshooting" cuối notebook
2. Copy 50 dòng log cuối gửi cho mình
3. Kèm screenshot nếu có lỗi hiển thị

---

**Code by Dr. Nểm CCĐK** — Khoa Hồi Sức Cấp Cứu