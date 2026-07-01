# Google Colab Script - Build APK Tính Dịch Truyền
# Chạy trên: https://colab.research.google.com

# ============================================================
# CELL 1: Cài đặt môi trường
# ============================================================
!apt update -qq 2>/dev/null
!apt install -y -qq openjdk-17-jdk-headless libffi-dev libssl-dev autoconf libtool 2>/dev/null
!pip install buildozer cython -q 2>/dev/null

# ============================================================
# CELL 2: Upload file
# ============================================================
from google.colab import files
import os

# Xóa file cũ nếu có
for f in ['buildozer.spec', 'kivy_app.py', 'buildozer (1).spec', 'kivy_app (1).py']:
    if os.path.exists(f):
        os.remove(f)

print("Upload kivy_app.py:")
uploaded = files.upload()
print("Upload buildozer.spec:")
uploaded = files.upload()

# Kiểm tra file đã upload
print("\nFile trong thư mục:")
!ls -la *.spec *.py 2>/dev/null

# ============================================================
# CELL 3: Build APK
# ============================================================
!buildozer -v android debug 2>&1 | tail -80

# ============================================================
# CELL 4: Download APK
# ============================================================
import os
if os.path.exists('bin/tindichtruyen-1.0-debug.apk'):
    files.download('bin/tindichtruyen-1.0-debug.apk')
    print("APK downloaded!")
else:
    print("APK chưa được tạo. Kiểm tra log cell trên.")