# Build APK — Flet (Đơn giản nhất)

App Tính Dịch Truyền — **Flet version** build APK siêu đơn giản.

## 🚀 Cách build NHANH NHẤT (chỉ 2 lệnh)

### Phương án A: Trên máy có Python (Windows/Mac/Linux)

```bash
pip install flet
flet build apk
```

APK sẽ ở: `build/apk/app-release.apk`

### Phương án B: Trên Google Colab (không cần cài gì)

1. Mở https://colab.research.google.com
2. Upload file `Build_APK_Flet.ipynb` (đã có sẵn trong repo)
3. Chạy 4 cells theo thứ tự

### Phương án C: Trên GitHub Codespaces (đơn giản nhất)

1. Push code lên GitHub repo
2. Vào https://github.com/codespaces → "New codespace" → chọn repo
3. Trong terminal:
   ```bash
   pip install flet
   flet build apk
   ```
4. Tải APK từ `build/apk/`

**GitHub Codespaces free 60h/tháng** — không cần cài gì trên máy.

## 📁 Files cần thiết

| File | Mô tả |
|------|-------|
| `main_flet.py` | Code app Flet (logic giống main.py, đẹp hơn) |
| `Build_APK_Flet.ipynb` | Notebook Colab (4 cells đơn giản) |

## 🎨 Tại sao Flet đơn giản hơn Kivy?

| Kivy + Buildozer | Flet |
|------------------|------|
| Cần buildozer.spec config phức tạp | 1 lệnh duy nhất `flet build apk` |
| Phải fix Python version, NDK, clang errors | Flet tự động xử lý tất cả |
| Pin cython, hostpython3, etc. | Tự động |
| Build 30-60 phút, hay fail | Build 10-15 phút, ít fail hơn |
| Code phải dùng Kivy widget riêng | Code Python thuần, UI Material Design |

## 📱 Cài APK lên điện thoại

1. Copy file `app-release.apk` vào điện thoại (USB / email / Drive)
2. Mở file bằng **Trình quản lý file**
3. Bấm **Cài đặt** → cho phép cài từ nguồn này
4. App xuất hiện ở màn hình chính với tên "Tính Dịch Truyền"

## 🆘 Troubleshooting

### `flet: command not found`
- Cài lại: `pip install flet --upgrade`

### Build fail ở "Android SDK not found"
- Flet tự động tải SDK. Nếu fail, kiểm tra disk:
  ```bash
  df -h
  ```
- Cần ít nhất 5GB trống.

### Build fail ở Java
- Cài Java 17:
  ```bash
  apt install -y openjdk-17-jdk-headless   # Linux
  brew install openjdk@17                  # macOS
  winget install Microsoft.OpenJDK.17      # Windows
  ```

### APK build OK nhưng app crash khi mở
- Test trên desktop trước:
  ```bash
  python main_flet.py
  ```
- Fix lỗi trước, build lại.

## 🔄 Cập nhật app

Sau khi sửa `main_flet.py`:
```bash
flet build apk
```
Flet tự detect code mới và build lại (cache nhanh hơn).

---

**Code by Dr. Nểm CCĐK** — Khoa Hồi Sức Cấp Cứu