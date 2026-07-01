# Tính Dịch Truyền - Flet version
Code by Dr. Nểm CCĐK

App tính tốc độ truyền dịch/máu cho nhân viên y tế.

## Build APK trên GitHub Codespaces (đơn giản nhất)

1. Push code lên GitHub repo
2. Mở Codespace từ repo
3. Trong terminal của Codespace:
   ```bash
   flet build apk
   ```
4. Tải APK từ `build/apk/app-release.apk`

## Build APK local (cần Docker)

```bash
pip install -r requirements.txt
flet build apk
```

## Chạy thử trên desktop

```bash
python main_flet.py
```