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



models.py

class RobotRec(Base):
    __tablename__ = 'robot_rec'

    sys_name = Column(String(100))
    dept_name = Column(String(100))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    run_time = Column(String(20))
    succ_qty = Column(Integer)
    fail_qty = Column(Integer)
    total_qty = Column(Integer)
    develop_tool = Column(String(100))
    __mapper_args__ = {
        'primary_key': [develop_tool, start_time, sys_name, dept_name, run_time]
    }


db.py

def record_run_time(start_time, end_time, succ_qty, fail_qty):
    # 记录运行时间
    session = None
    run_time = (end_time - start_time).seconds
    run_time = str(run_time)
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
        new_record = RobotRec(
            sys_name='自动读取信用报告', 
            dept_name='FIN', 
            start_time=start_time, 
            end_time=end_time, 
            run_time=run_time, 
            succ_qty=succ_qty, 
            fail_qty=fail_qty, 
            total_qty=succ_qty + fail_qty, 
            develop_tool='Python') 
        session.add(new_record) 
        session.commit()
    except Exception as e:
        return str(e)
    finally:
        if not session:
            session.close()


def copy_file(src_file, dst_folder):
    base_name = os.path.basename(src_file)
    dst_file = os.path.join(dst_folder, base_name)
    
    if os.path.exists(dst_file):
        file_name, file_extension = os.path.splitext(base_name)
        index = 1
        while os.path.exists(dst_file):
            new_file_name = f"{file_name}({index}){file_extension}"
            dst_file = os.path.join(dst_folder, new_file_name)
            index += 1
    
    shutil.copy2(src_file, dst_file)
    return os.path.basename(dst_file)


main.py
from src.db import DB, record_run_time, copy_file

        self.start_time = datetime.datetime.now()
        self.succ_qty = 0
        self.fail_qty = 0
        self.total_qty = 0

self.total_qty += 1
self.fail_qty += 1
self.succ_qty += 1

new_pdf_path = copy_file(pdf_path, r'\\cngcns16001\Shares\FIN&IT\RPA Credit Report')


        # 记录时间
        self.end_time = datetime.datetime.now()
        record_run_time(self.start_time, self.end_time, self.succ_qty, self.fail_qty)
