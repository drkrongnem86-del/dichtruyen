# -*- coding: utf-8 -*-
"""Quick script to fix Bước 1 in Build_APK_Colab.ipynb - lần 3: thêm pip vào venv"""

import json
from pathlib import Path

NOTEBOOK = Path(r"C:\Users\MyPC\.mavis\sessions\mvs_743f10055b3a47f8bb9c47a9b011efbe\workspace\Build_APK_Colab.ipynb")

with open(NOTEBOOK, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Tìm cell code đầu tiên (Bước 1)
for cell in nb['cells']:
    if cell.get('cell_type') == 'code':
        source = cell.get('source', [])
        if any('Bước 1a' in line for line in source):
            print(f"Found Bước 1 cell, replacing source...")
            new_source = [
                "import os, subprocess\n",
                "# Bước 1a: Cài Python 3.11 bằng uv (Colab có sẵn uv)\n",
                "subprocess.run(['pip', 'install', '-q', 'uv'], check=True)\n",
                "subprocess.run(['uv', 'python', 'install', '3.11.6'], check=True)\n",
                "result = subprocess.run(['uv', 'python', 'find', '3.11.6'], capture_output=True, text=True)\n",
                "py311 = result.stdout.strip()\n",
                "print(f'Python 3.11 ở: {py311}')\n",
                "# Symlink /usr/local/bin/python3 → python3.11\n",
                "if os.path.exists('/usr/local/bin/python3'):\n",
                "    os.remove('/usr/local/bin/python3')\n",
                "os.symlink(py311, '/usr/local/bin/python3')\n",
                "print('Đã symlink python3 →', py311)\n",
                "# Bước 1b: Cài Java 17 + lib build\n",
                "subprocess.run(['apt', 'install', '-y', '-qq', 'openjdk-17-jdk-headless', 'libffi-dev', 'libssl-dev', 'autoconf', 'libtool', 'pkg-config', 'ninja-build', 'cmake', 'zip', 'unzip'], check=True)\n",
                "print('Đã cài Java 17 + lib build')\n",
                "# Bước 1c: Verify Python và Java\n",
                "print()\n",
                "r = subprocess.run(['python3', '--version'], capture_output=True, text=True)\n",
                "print('python3:', r.stdout.strip())\n",
                "r = subprocess.run('java -version 2>&1', shell=True, capture_output=True, text=True)\n",
                "print('Java:', (r.stdout.splitlines()[0] if r.stdout else 'unknown'))\n",
                "# Bước 1d: Tạo venv với Python 3.11\n",
                "subprocess.run(['uv', 'venv', '/content/venv', '--python', '3.11.6'], check=True)\n",
                "print('Đã tạo venv tại /content/venv')\n",
                "# Cài pip vào venv TRƯỚC (uv tạo venv không tự cài pip)\n",
                "subprocess.run(['uv', 'pip', 'install', '--python', '/content/venv/bin/python', 'pip', 'setuptools', 'wheel'], check=True)\n",
                "print('Đã cài pip + setuptools + wheel vào venv')\n",
                "# Cài buildozer + cython vào venv\n",
                "subprocess.run(['uv', 'pip', 'install', '--python', '/content/venv/bin/python', 'buildozer==1.5.0', 'cython>=3.0'], check=True)\n",
                "print('Đã cài buildozer + cython vào venv')\n",
                "# Symlink buildozer CLI để gọi ngắn gọn\n",
                "if os.path.exists('/usr/local/bin/buildozer'):\n",
                "    os.remove('/usr/local/bin/buildozer')\n",
                "os.symlink('/content/venv/bin/buildozer', '/usr/local/bin/buildozer')\n",
                "print('Đã symlink buildozer')\n",
                "# Verify buildozer\n",
                "r = subprocess.run(['buildozer', '--version'], capture_output=True, text=True)\n",
                "print('Buildozer:', r.stdout.strip())\n",
                "print()\n",
                "print('✅ Bước 1 xong — môi trường sẵn sàng (Python 3.11 + Java 17 + Cython 3+)')\n",
            ]
            cell['source'] = new_source
            print("Đã thay source Bước 1")
            break

with open(NOTEBOOK, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"✅ Saved {NOTEBOOK}")
print(f"   Size: {NOTEBOOK.stat().st_size / 1024:.1f} KB")