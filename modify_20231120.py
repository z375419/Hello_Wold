from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models import  RobotRec
from src.db import copy_file
import os

def record_run_time():
    # 记录运行时间
    session = None
    try:
        username = 'rpa'
        password = 'sickrpa123,'
        server = 'cngcns16058'
        port = '1433'
        database = 'sickprod'
        url = f'mssql+pymssql://{username}:{password}@{server}:{port}/{database}'
        engine = create_engine(url)
        Session = sessionmaker(bind=engine) 
        session = Session()
        query = session.query(RobotRec).limit(5)
        for rb in query:
            print(rb.run_time, rb.dept_name, rb.sys_name, rb.start_time)
    except Exception as e:
        print(str(e))
    finally:
        if not session:
            session.close()

def move_file():
    folder_path = r'D:\python\env\uiautobot\ExtractPDfInformation\data\已完成'
    for attr_folder in os.listdir(folder_path):
        sub_folder_path = os.path.join(folder_path, attr_folder)
        if os.path.isdir(sub_folder_path) == False:
            continue
        status = ''
        status_path = os.path.join(sub_folder_path, 'status.txt')
        with open(status_path, 'r', encoding='utf-8') as f:
            status = f.read()
        pdf_path = ''
        word_path = ''
        for file_name in os.listdir(sub_folder_path):
            if file_name.lower()[-4:] == '.pdf':
                pdf_path = os.path.join(sub_folder_path, file_name)
            if file_name.lower()[-5:] == '.docx' and file_name.startswith('`$') == False:
                word_path = os.path.join(sub_folder_path, file_name)
        if pdf_path == '':
            pdf_path = word_path
        if status == '解析完成':
            json_path = ''
            for file_name in os.listdir(sub_folder_path):
                if file_name.lower()[-5:] == '.json' and file_name.lower() != 'word.json':
                    json_path = os.path.join(sub_folder_path, file_name)
            r = ''
            if json_path:
                try:
                    new_pdf_path = copy_file(pdf_path, r'\\cngcns16001\Shares\FIN&IT\RPA Credit Report')
                    if os.path.basename(new_pdf_path) != os.path.basename(pdf_path):
                        print(pdf_path, ':', new_pdf_path)
                except Exception as e:
                    print(sub_folder_path, ':', str(e))

# record_run_time()
move_file()


