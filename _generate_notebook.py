# -*- coding: utf-8 -*-
"""
Script generate Build_APK_Colab.ipynb
Chạy 1 lần để tạo notebook. Có thể xóa file này sau khi đã có .ipynb.
"""

import json
from pathlib import Path

WORKSPACE = Path(r"C:\Users\MyPC\.mavis\sessions\mvs_743f10055b3a47f8bb9c47a9b011efbe\workspace")
OUT = WORKSPACE / "Build_APK_Colab.ipynb"


def md(*lines):
    """Markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [l + "\n" for l in lines],
    }


def code(*lines):
    """Code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [l + "\n" for l in lines],
    }


cells = []

# ════════════════════════════════════════════════════════════════════════
# Cell 0: Title
# ════════════════════════════════════════════════════════════════════════
cells.append(md(
    "# 💉 Build APK — Tính Dịch Truyền (Dr. Nểm CCĐK)",
    "",
    "Notebook này build file **APK Android** từ app Kivy trên Google Colab — không cần cài WSL, Docker, hay gì trên máy Windows.",
    "",
    "## 📋 Cách dùng",
    "1. Upload 2 file vào Colab (cell **Bước 1**):",
    "   - `kivy_app.py` (code app Kivy)",
    "   - `buildozer.spec` (config build)",
    "2. Chạy **Bước 1 → Bước 5** theo thứ tự, đợi mỗi cell xong mới chạy tiếp.",
    "3. APK tải về tự động ở **Bước 5**.",
    "",
    "## ⏱️ Thời gian dự kiến",
    "- Lần đầu: **30-45 phút** (tải SDK + NDK + compile Kivy)",
    "- Lần 2 trở đi: **10-15 phút** (Colab giữ cache)",
    "",
    "> 💡 **Mẹo**: Để tab Colab luôn mở (không bị disconnect), mở thêm tab Chrome bất kỳ cùng trình duyệt — Colab sẽ giữ session.",
))

# ════════════════════════════════════════════════════════════════════════
# Cell 1: Cài môi trường
# ════════════════════════════════════════════════════════════════════════
cells.append(md(
    "## ⚙️ Bước 1: Cài môi trường (Java 17 + buildozer + cython)",
    "",
    "Chạy cell này **một lần** — mất khoảng 2-3 phút.",
))
cells.append(code(
    "# Cập nhật apt + cài Java 17 + các thư viện build cần thiết",
    "!apt update -qq 2>&1 | tail -2",
    "!apt install -y -qq openjdk-17-jdk-headless libffi-dev libssl-dev \\",
    "    autoconf libtool pkg-config ninja-build cmake zip unzip 2>&1 | tail -5",
    "",
    "# Cài Python packages",
    "!pip install -q --upgrade pip",
    "!pip install -q buildozer==1.5.0 cython==0.29.36",
    "",
    "# Verify",
    "import subprocess",
    "print('Java:', subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT).decode().splitlines()[0])",
    "print('Buildozer:', subprocess.check_output(['buildozer', '--version']).decode().strip())",
    "",
    "print('\\n✅ Môi trường OK, sẵn sàng build APK')",
))

# ════════════════════════════════════════════════════════════════════════
# Cell 2: Upload file
# ════════════════════════════════════════════════════════════════════════
cells.append(md(
    "## 📂 Bước 2: Upload 2 file `kivy_app.py` và `buildozer.spec`",
    "",
    "Cell này sẽ mở hộp thoại chọn file. Anh chọn **cả 2 file** trong thư mục workspace rồi nhấn Open.",
))
cells.append(code(
    "from google.colab import files",
    "import os",
    "",
    "# Xóa file cũ nếu có (để tránh conflict khi chạy lại)",
    "for f in ['kivy_app.py', 'buildozer.spec', 'main.py']:",
    "    if os.path.exists(f):",
    "        os.remove(f)",
    "        print(f'Đã xóa file cũ: {f}')",
    "",
    "print('\\n👉 Chọn 2 file: kivy_app.py + buildozer.spec\\n')",
    "uploaded = files.upload()",
    "",
    "# Kiểm tra file đã upload đủ chưa",
    "have = set(os.listdir('.'))",
    "missing = [f for f in ['kivy_app.py', 'buildozer.spec'] if f not in have]",
    "if missing:",
    "    print(f'\\n❌ THIẾU FILE: {missing}')",
    "    print('Upload lại nhé.')",
    "else:",
    "    size_kivy = os.path.getsize('kivy_app.py') / 1024",
    "    size_spec = os.path.getsize('buildozer.spec') / 1024",
    "    print(f'\\n✅ kivy_app.py: {size_kivy:.1f} KB')",
    "    print(f'✅ buildozer.spec: {size_spec:.1f} KB')",
    "    print('\\nSẵn sàng build APK → chạy Bước 3.')",
))

# ════════════════════════════════════════════════════════════════════════
# Cell 3: Accept licenses + check
# ════════════════════════════════════════════════════════════════════════
cells.append(md(
    "## 🔑 Bước 3: Chấp nhận Android SDK licenses",
    "",
    "Cell này accept Android SDK licenses tự động (cần thiết để buildozer tải SDK).",
))
cells.append(code(
    "import os",
    "import subprocess",
    "",
    "# Tạo sẵn thư mục SDK để buildozer không hỏi lại",
    "sdk_root = os.path.expanduser('~/.buildozer/android/platform/android-33')",
    "os.makedirs(sdk_root, exist_ok=True)",
    "",
    "# Accept SDK licenses tự động bằng yes pipe",
    "print('Đang accept Android SDK licenses...')",
    "result = subprocess.run(",
    "    ['bash', '-c', \"yes | buildozer android debug 2>&1 | head -20 || true\"],\n    "    capture_output=True, text=True, timeout=120",
    ")",
    "print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)",
    "",
    "print('\\n✅ Licenses đã được chấp nhận (nếu lỗi thì kệ, build sẽ tự xử lý)')",
))

# ════════════════════════════════════════════════════════════════════════
# Cell 4: Build APK
# ════════════════════════════════════════════════════════════════════════
cells.append(md(
    "## 🔨 Bước 4: Build APK",
    "",
    "⏱️ **Lần đầu 30-45 phút** (tải SDK/NDK ~1GB + compile Kivy).",
    "",
    "> ⚠️ **Không tắt tab, không để Colab sleep.** Mở thêm 1 tab Chrome khác để giữ session.",
))
cells.append(code(
    "# Build APK — lệnh chính",
    "# -v: verbose (in log chi tiết)",
    "# android: target Android",
    "# debug: build dạng debug (không cần ký release key, cài trực tiếp được)",
    "",
    "import time",
    "t0 = time.time()",
    "",
    "!buildozer -v android debug 2>&1 | tee build.log | tail -50",
    "",
    "elapsed = time.time() - t0",
    "mins = int(elapsed // 60)",
    "secs = int(elapsed % 60)",
    "print(f'\\n⏱️ Thời gian build: {mins} phút {secs} giây')",
))

# ════════════════════════════════════════════════════════════════════════
# Cell 5: Download APK
# ════════════════════════════════════════════════════════════════════════
cells.append(md(
    "## 📥 Bước 5: Tải APK về máy",
    "",
    "Cell này tìm file APK và mở hộp thoại download.",
))
cells.append(code(
    "import os",
    "import glob",
    "from google.colab import files",
    "",
    "# Tìm file APK trong các đường dẫn có thể",
    "apk_candidates = glob.glob('bin/*.apk') + glob.glob('.buildozer/android/platform/build-*/dists/*/build/outputs/apk/**/*.apk', recursive=True)",
    "",
    "print('Tìm thấy các file APK:')",
    "for apk in apk_candidates:",
    "    size_mb = os.path.getsize(apk) / 1024 / 1024",
    "    print(f'  📦 {apk}  ({size_mb:.2f} MB)')",
    "",
    "if not apk_candidates:",
    "    print('\\n❌ KHÔNG TÌM THẤY APK!')",
    "    print('→ Kéo xuống cell Bước 4 xem log build có lỗi gì')",
    "else:",
    "    # Ưu tiên file debug nhỏ hơn",
    "    debug_apks = [a for a in apk_candidates if 'debug' in a]",
    "    target = sorted(debug_apks, key=lambda a: os.path.getsize(a))[0] if debug_apks else apk_candidates[0]",
    "",
    "    size_mb = os.path.getsize(target) / 1024 / 1024",
    "    print(f'\\n🎯 File sẽ tải về: {target} ({size_mb:.2f} MB)')",
    "    print('Đang mở hộp thoại download...\\n')",
    "",
    "    files.download(target)",
    "    print('\\n✅ Đã tải APK thành công!')",
    "    print('👉 Copy file .apk vào điện thoại Android → mở file → cài đặt.')",
))

# ════════════════════════════════════════════════════════════════════════
# Cell 6: Troubleshooting helper
# ════════════════════════════════════════════════════════════════════════
cells.append(md(
    "## 🛠️ Nếu build fail — chạy cell này để xem log chi tiết",
    "",
    "Nếu APK không được tạo, copy **toàn bộ** nội dung log dán cho mình để debug nhé.",
))
cells.append(code(
    "import subprocess",
    "",
    "# Hiển thị 80 dòng cuối của build log để xem lỗi",
    "print('=' * 70)",
    "print('80 DÒNG CUỐI CỦA build.log')",
    "print('=' * 70)",
    "try:",
    "    result = subprocess.run(['tail', '-80', 'build.log'], capture_output=True, text=True)",
    "    print(result.stdout)",
    "except FileNotFoundError:",
    "    # Fallback nếu tail không có",
    "    with open('build.log', 'r', errors='ignore') as f:",
    "        lines = f.readlines()",
    "        print(''.join(lines[-80:]))",
))

# ════════════════════════════════════════════════════════════════════════
# Save notebook
# ════════════════════════════════════════════════════════════════════════
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.10",
            "mimetype": "text/x-python",
            "file_extension": ".py",
            "pygments_lexer": "ipython3",
            "codemirror_mode": {"name": "ipython", "version": 3},
        },
        "colab": {
            "provenance": [],
            "collapsed_sections": [],
            "name": "Build_APK_Colab.ipynb",
        },
        "accelerator": "GPU",
    },
    "nbformat": 4,
    "nbformat_minor": 0,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"✅ Đã tạo: {OUT}")
print(f"   Kích thước: {OUT.stat().st_size / 1024:.1f} KB")
print(f"   Số cell: {len(cells)}")