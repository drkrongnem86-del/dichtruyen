import json
nb = json.load(open(r'C:\Users\MyPC\.mavis\sessions\mvs_743f10055b3a47f8bb9c47a9b011efbe\workspace\Build_APK_Colab.ipynb', encoding='utf-8'))
cell = [c for c in nb['cells'] if c.get('cell_type')=='code'][0]
print(''.join(cell['source']))