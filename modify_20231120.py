main
self.g

        # 删除目标数据库
        r = db.drop_database()
        if r != '删除数据库数据成功':
            self.error_list.append(f'删除数据库失败:\n' + r)
            self.g = '0'

        # 执行存储过程
        r = db.execute_procedure()
        if r != '执行存储过程成功':
            self.error_list.append(f'执行存储过程失败:\n' + r)
            self.g = '0'


db
self.dw_url = url = f'mssql+pymssql://{username}:{password}@{server}:{port}/DW'

    def drop_database(self):
        try:
            self.session.query(Customer).delete()
            self.session.query(EquityStructure).delete()
            self.session.query(FinancialIndicators).delete()
        except Exception as e:
            return str(e)
        return '删除数据库数据成功'
    
    def execute_procedure(self):
        # 3.1 DW.[dbo].[P_PTY_CUST_CRD_H]
        # 3.2 DW.[dbo].[P_PTY_CUST_CRD_EQ]
        # 3.3 DW.[dbo].[P_PTY_CUST_CRD_FIN]
        try:
            url = self.dw_url
            engine = create_engine(url)
            Session = sessionmaker(bind=engine)
            session = Session()
            # self.session.execute("CALL DW.dbo.P_PTY_CUST_CRD_H")
            # self.session.execute("CALL DW.dbo.P_PTY_CUST_CRD_EQ")
            # self.session.execute("CALL DW.dbo.P_PTY_CUST_CRD_FIN")
            session.execute("exec DW.[dbo].[P_PTY_CUST_CRD_H]")
            session.execute("exec DW.[dbo].[P_PTY_CUST_CRD_EQ]")
            session.execute("exec DW.[dbo].[P_PTY_CUST_CRD_FIN]")
        except Exception as e:
            return str(e)
        finally:
            session.close()
        return '执行存储过程成功'


tools
def format_registered_capital_cib(registered_capital: str) -> Tuple[int, str]:
    if registered_capital == '/':
        return '0', 'CNY'
    if registered_capital == None:
        return '0', 'CNY'
    registered_capital = registered_capital.replace('~', '-')
    registered_capital = registered_capital.replace('～', '-')
    registered_capital = registered_capital.replace('－', '-')
    registered_capital = registered_capital.replace(',', '')
    registered_capital = registered_capital.replace('，', '')
    multiple = 1
    v = ''
    if '万' in registered_capital:
        multiple = 10000
        v = registered_capital.split('万')[0]
    elif '千' in registered_capital:
        multiple = 1000
        v = registered_capital.split('千')[0]
    elif '亿' in registered_capital:
        multiple = 100000000
        v = registered_capital.split('亿')[0]

    # match = re.findall(r"(\d+(,\d+)?(\.\d+)?)", v)
    match = re.search(r"(\d+(\.\d+)?)-(\d+(\.\d+)?)", v)
    match1 = re.search(r"(\d+(\.\d+)?)", v)
    min_amount = -9
    max_amount = -9
    if match:
        min_amount = float(match.group(1)) * multiple
        max_amount = float(match.group(3)) * multiple
    else:
        max_amount = float(match.group(1)) * multiple
    amount = ''
    if min_amount != -9 and  max_amount != -9:
        amount = number_to_standard(min_amount) + '-' + number_to_standard(max_amount)
    elif max_amount != -9:
        amount = number_to_standard(max_amount)
    else:
        amount = '0'
    currency = _get_Currency(registered_capital)
    return amount, currency


qna
            if match:
                limit = number_to_standard(float(match.group(1)) * 10000) + '-' + number_to_standard(float(match.group(2)) * 10000)
                period = match.group(4) + '~' + match.group(5) + '天'
            match = re.search(r"(\d+万)〜(\d+(\.\d+)?)万(\d+)天", s)
            if match and limit == None:
                # limit = float(match.group(2)) * 10000
                limit = number_to_standard(float(match.group(1)) * 10000) + '-' + number_to_standard(float(match.group(2)) * 10000)
                period = match.group(4) + '天'
            match = re.search(r"(\d+(\.\d+)?)万(\d+)〜(\d+)天", s)
            if match and limit == None:
                # limit = float(match.group(1)) * 10000
                limit = number_to_standard(float(match.group(1)) * 10000)
                period = match.group(3) + '~' + match.group(4) + '天'
            match = re.search(r"(\d+(\.\d+)?)万(\d+)天", s)
            if match and limit == None:
                limit = number_to_standard(float(match.group(1)) * 10000)
                period =  match.group(3) + '天'


def number_to_standard(n):
    if not n:
        return 0
    number = int(round(n,0))
    return '{:,}'.format(number)
