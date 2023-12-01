def get_table_info(element, is_allograph = False) -> List:
    arr = []
    for row in element.rows:
        sub_arr = []
        old_text = ''
        for cell in row.cells:
            sub_text = cell.text
            sub_text = sub_text.replace(' ', '').strip()
            if is_allograph:
                sub_text = tools.replace_encode(sub_text)
            if sub_text == '':
                if old_text == '注册日期':
                    rs = cell._element.xpath('.//w:t')
                    rs = ''.join([r.text for r in rs])
                    sub_text = str(rs).replace(' ', '').strip()
                    if is_allograph:
                        sub_text = tools.replace_encode(sub_text)
            old_text = sub_text
            sub_arr.append(sub_text)
        arr.append(sub_arr)
    return arr


转换pdf完成

Sub CheckTables()
    Dim myArray(1 To 2, 1 To 2) As String
    Dim tbl As Table
    Dim i As Integer, j As Integer, matchCount As Integer
    
    ' 预设的二维数组内容
    myArray(1, 1) = "企业名称"
    myArray(1, 2) = ""
    myArray(2, 1) = "英文名称"
    myArray(2, 2) = ""

    
    ' 循环遍历所有表格
    For Each tbl In ActiveDocument.Tables
        totalCount = 0
        notMatchCount = 0
        ' 检查表格第一行和第二行是否与预设的数组匹配
        For i = 1 To UBound(myArray)
            For j = 1 To UBound(myArray, 2)
                If myArray(i, j) <> "" Then
                    totalCount = totalCount + 1
                    If InStr(tbl.Cell(i, j).Range.Text, myArray(i, j)) > 0 Then
                    Else
                        notMatchCount = notMatchCount + 1
                    End If
                End If
            Next
        Next
        ' 如果匹配数量符合条件，则表示是寻找的表格
        If totalCount > 0 And notMatchCount = 0 Then
            MsgBox "找到匹配的表格"
            Set c = tbl.Cell(1, 1)
            ' 在此处可以添加其他操作
        End If
    Next tbl
End Sub




import os
import shutil
顺丰泰森
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

