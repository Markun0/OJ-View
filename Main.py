import reptile

if __name__ == '__main__':

    log_id = '202200201101'  # 统一认证平台登陆账号(学号)
    passwd = '202200201101'  # 统一认证平台密码
    mainThreat = reptile.CatchProcession(log_id, passwd)
    mainThreat.auto_doit()
