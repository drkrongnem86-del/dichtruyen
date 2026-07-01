[app]

# (str) Tên file Python chính — phải là kivy_app.py
source.filename = kivy_app.py

# (list) Thư mục chứa source code (relative hoặc absolute)
source.dir = .

# (list) File extension được include vào build
source.include_exts = py,png,jpg,kv,atlas

# (str) Version của app (hiển thị trên Google Play / About)
version = 1.0.0

# (str) Số version cho Android (versionCode)
version.numeric = 1

# (str) Tên hiển thị trên launcher và title bar
title = Tính Dịch Truyền

# (str) Package name — không được trùng package khác
package.name = tindichtruyen

# (str) Domain cho package (đảo ngược)
package.domain = com.ccdk.drip

# (str) Author
author = Dr. Nem CCDK

# (str) Email author (optional)
# author.email =

# (str) Mô tả ngắn
# author.fullname =

# (list) Python + thư viện cần thiết
# QUAN TRỌNG:
# - KHÔNG pin python3 version — Colab host là Python 3.14.2,
#   python3 phải match với hostpython3 nếu không sẽ fail với:
#   "python3 should have same version as hostpython3, X.Y.Z != A.B.C"
# - KHÔNG pin cython==0.29.x — Python 3.14 đã thêm parameter 'with_exceptions'
#   vào _PyLong_AsByteArray(), Cython 0.29.x không tương thích.
#   Dùng Cython 3.0+ để tương thích Python 3.14.
requirements = python3, kivy==2.3.0, cython>=3.0

# (str) Hướng màn hình: portrait / landscape / all
orientation = portrait

# (bool) Có cho phép sleep trong app không
# android.allow_sleep = True

# (bool) Hiển thị app full screen (không status bar)
# fullscreen = 0

# ─── Icon & launcher ──────────────────────────────────────────────────────
# (str) Icon cho app — buildozer dùng Kivy icon mặc định nếu không có
# icon.filename = %(source.dir)s/icon.png
# (str) Launcher icon cho Android
# presplash.filename = %(source.dir)s/presplash.png


[buildozer]

# (int) Log level: 0 = debug, 1 = info, 2 = warning, 3 = error
log_level = 2

# (int) Số worker khi build Cython
# build_dir = ./.buildozer


[android]

# (int) Android API target (compileSdk)
android.api = 33

# (int) Min Android API để chạy được app (Android 5.0+)
android.minapi = 21

# (int) Android SDK version (giống android.api)
android.sdk = 33

# (str) Android NDK version
android.ndk = 25b

# (int) NDK API level
android.ndk_api = 21

# (bool) Skip update Android SDK/NDK khi đã có sẵn — giúp build nhanh hơn
android.skip_update = False

# (str) Chế độ build: debug / release
build_mode = debug

# (list) Permissions Android cần khai báo — app này chỉ cần INTERNET optional
android.permissions = INTERNET

# (str) Entry point class cho Kivy
android.entrypoint = org.kivy.android.PythonActivity

# (str) Java home — set trong buildozer.android entry
# android.java_dir = /usr/lib/jvm/java-17-openjdk-amd64

# (bool) Auto accept Android SDK licenses (QUAN TRỌNG trên Colab)
android.accept_sdk_license = True

# (list) Các biến env cho p4a (python-for-android)
# p4a.extra_args =

# (list) Recipes bổ sung nếu cần
# p4a.extra_recipes =


[source]

# (str) Pattern để trích version từ source code
# version.pattern = ?VERSION?

# (bool) Tự động detect version từ source code
# version.regex =

# (str) Modules
# requirements = python3,kivy


[presplash]

# (str) Màu nền cho màn hình chờ (color hex)
# presplash.color = #1565c0


[icons]

# Cấu hình icon các kích thước — buildozer tự tạo placeholder nếu không có
# icon.filename = %(source.dir)s/icon.png
# icon.adaptive.filename = %(source.dir)s/icon_adaptive.png