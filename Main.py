import code

if __name__ == '__main__':
    log_id = '202200201101'  # 统一认证平台登陆账号(学号)
    passwd = '202200201101'  # 统一认证平台密码
    mainThreat = code.CatchProcession(log_id, passwd)
    mainThreat.auto_doit()
    # 以下代码实现定时启动
    # schedule.every().day.at("13:20").do(mainThreat.auto_doit)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)