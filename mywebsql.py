import pymysql.connections
from datetime import datetime, timedelta

# 数据库连接信息
db_config = {
    'user': 'root',
    'password': 'Mkl20040310',
    'host': 'localhost',
    'database': 'webdatabase'
}
# 标记
last_vist = '0'


def insert_data(data_list, flag):
    try:
        # 创建数据库连接
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        if flag:
            # 清空表的 SQL 语句
            truncate_table_query = "TRUNCATE TABLE student_problem"

            # 执行清空表
            cursor.execute(truncate_table_query)

        # 将字符串类型的数据转换为对应的数值类型
        converted_data_list = convert_data_types(data_list)

        # 插入数据的SQL语句
        sql = """
                        INSERT INTO student_problem (problem_id, student_id, submission_status, submission_time) 
                        VALUES (%s, %s, %s, %s)
                    """
        # 执行批量插入
        cursor.executemany(sql, converted_data_list)
        conn.commit()
        if flag:
            print("批量数据插入成功")
        else:
            print("数据更新成功")
    except pymysql.Error as err:
        print(f"Error: {err}")
    finally:
        # 关闭连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def get_monday_date():
    today = datetime.today()
    # 计算今天是星期几（周一是0，周日是6）
    weekday = today.weekday()
    # 计算本周星期一的日期
    monday = today - timedelta(days=weekday)
    # 格式化日期为yyyy-mm-dd格式
    monday_date = monday.strftime('%Y-%m-%d')
    return monday_date


def convert_data_types(data_list):
    # 定义时间
    global last_vist
    start_time = datetime.strptime(get_monday_date() + ' 14:50:00', '%Y-%m-%d %H:%M:%S')

    converted_data = []
    print("导入如下数据:")
    for row in data_list:
        if row[2] <= last_vist:
            break
        end_time = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
        # 计算时间差
        time_difference = end_time - start_time
        # 转换为分钟
        time = time_difference.total_seconds() / 60

        # 转换数据类型
        converted_row = [
            row[1],  # problem_id
            row[3],  # student_id
            row[5],  # submission_status
            int(time),  # submission_time
        ]
        print("problem_id: " + row[1] + "    student_id: " + row[3] + "    submission_status: " + row[5] + "    submission_time: " + str(int(time)))
        converted_data.append(converted_row)
    last_vist = data_list[0][2]
    return converted_data
