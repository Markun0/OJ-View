import pymysql.connections
import re
# 数据库连接信息
db_config = {
    'user': 'root',
    'password': 'Mkl20040310',
    'host': 'localhost',
    'database': 'webdatabase'
}

def clear_and_insert_data(data_list):
    try:
        # 创建数据库连接
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # 清空表的 SQL 语句
        truncate_table_query = "TRUNCATE TABLE student_stats"

        # 执行清空表的 SQL 语句
        cursor.execute(truncate_table_query)

        # 插入数据的 SQL 语句
        insert_query = """
        INSERT INTO student_stats (ranking, username, correct_count, total_time, A, Ax, B, Bx, C, Cx, D, Dx, E, Ex)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # 将字符串类型的数据转换为对应的数值类型
        converted_data_list = convert_data_types(data_list)

        # 执行批量插入数据的 SQL 语句
        cursor.executemany(insert_query, converted_data_list)
        conn.commit()
        print("批量数据插入成功")

    except pymysql.Error as err:
        print(f"Error: {err}")
    finally:
        # 关闭连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


def convert_data_types(data_list):
    converted_data = []
    # 定义正则表达式
    time_pattern = r'(\d+):(\d+):(\d+)'
    for row in data_list:
        time = []
        value = []
        for i in range(0, 6):
            # 使用正则表达式进行匹配
            time_match = re.search(time_pattern, row[i + 4])
            # 提取匹配的结果
            hours = int(time_match.group(1)) if time_match else 0
            minutes = int(time_match.group(2)) if time_match else 0
            seconds = int(time_match.group(3)) if time_match else 0
            take = hours * 60 + minutes + seconds / 60
            time.append(take if take else None)
            value.append(int(row[i + 4][9:-1]) if row[i + 4][9:-1] else None)


        # 转换数据类型
        converted_row = [
            int(row[0]),  # ranking
            row[1],       # username
            int(row[3]),  # correct_count
            time[0],       # total_time
            time[1],       # A
            value[1],      # Ax
            time[2],       # B
            value[2],      # Bx
            time[3],       # C
            value[3],      # Cx
            time[4],       # D
            value[4],      # Dx
            time[5],       # E
            value[5],      # Ex
        ]
        converted_data.append(converted_row)
    return converted_data


def get_stats():
    try:
        # 创建数据库连接
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # 查询每道题的通过人数和通过时间
        query = """
        SELECT 
            COUNT(A) AS A_passed,
            AVG(A) AS A_avg_time,
            MIN(A) AS A_first_pass_time,
            COUNT(B) AS B_passed,
            AVG(B) AS B_avg_time,
            MIN(B) AS B_first_pass_time,
            COUNT(C) AS C_passed,
            AVG(C) AS C_avg_time,
            MIN(C) AS C_first_pass_time,
            COUNT(D) AS D_passed,
            AVG(D) AS D_avg_time,
            MIN(D) AS D_first_pass_time,
            COUNT(E) AS E_passed,
            AVG(E) AS E_avg_time,
            MIN(E) AS E_first_pass_time
        FROM student_stats
        """
        cursor.execute(query)
        result = cursor.fetchone()

        stats = {
            'A_passed': result[0],
            'A_avg_time': float(result[1]) if result[1] is not None else None,
            'A_first_pass_time': float(result[2]) if result[2] is not None else None,
            'B_passed': result[3],
            'B_avg_time': float(result[4]) if result[4] is not None else None,
            'B_first_pass_time': float(result[5]) if result[5] is not None else None,
            'C_passed': result[6],
            'C_avg_time': float(result[7]) if result[7] is not None else None,
            'C_first_pass_time': float(result[8]) if result[8] is not None else None,
            'D_passed': result[9],
            'D_avg_time': float(result[10]) if result[10] is not None else None,
            'D_first_pass_time': float(result[11]) if result[11] is not None else None,
            'E_passed': result[12],
            'E_avg_time': float(result[13]) if result[13] is not None else None,
            'E_first_pass_time': float(result[14]) if result[14] is not None else None,
        }

        print(stats)
        return stats

    except pymysql.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        # 关闭连接
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def add_data(data_list):


if __name__ == '__main__':
    data_list = []
    row = []
    row.append("1")
    row.append("202300204002")
    row.append("李洪宇")
    row.append("5")
    row.append("01:57:29")
    row.append("00:55:47(-10)")
    row.append("null")
    row.append("01:02:24(-2)")
    row.append("01:24:33")
    row.append("01:57:29")
    data_list.append(row)
    clear_and_insert_data(data_list)
    data_list.clear()
    row[1] = "202200201101"
    data_list.append(row)
    add_data(data_list)
    get_stats()
