import os
import shutil

青岛威纳的“青”字无法识别
folders = [
    r'D:\python\env\uiautobot\ExtractPDfInformation\data\已完成\55'
]
with open(r'4.txt', 'r', encoding='utf-8') as f:
    txt = f.read()
    folders = txt.split('\n')
target_folder_path = r'D:\python\env\uiautobot\ExtractPDfInformation\data\未完成'
for folder in folders:
    if not folder:
        continue
    new_folder_path = os.path.join(target_folder_path, '00-' + os.path.basename(folder))
    print(new_folder_path)
    if os.path.exists(new_folder_path) == True:
        shutil.rmtree(new_folder_path)
    shutil.copytree(folder, new_folder_path)
    with open(os.path.join(new_folder_path, 'status.txt'), 'w', encoding='utf-8') as f:
        f.write('转换pdf完成')


import os
import json
base_folder = r'D:\python\env\uiautobot\ExtractPDfInformation\data\未完成'
for folder_name in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder_name)
    for file_name in os.listdir(folder_path):
        if '.json' in file_name and file_name not in ['status.json', 'word.json']:
            try:
                file_path = os.path.join(folder_path, file_name)
                jsdata = json.load(open(file_path, 'r', encoding='utf-8'))
                print(folder_name, jsdata['cust']['date_year'])
            except Exception as e:
                print(folder_name, str(e))

