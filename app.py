from flask import Flask
import pymysql
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)


def fetch_submit_types(problem_id):
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Mkl20040310',
            database='webdatabase',
            charset='utf8mb4'
        )
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                            SELECT submission_status, COUNT(*) as count
                            FROM student_problem
                            WHERE problem_id = %s
                            GROUP BY submission_status;
                        """
            cursor.execute(sql, (problem_id,))
            results = cursor.fetchall()
            return results
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return []
    finally:
        connection.close()


def create_pie_chart(data, problem_id):
    # 创建 labels 和 count 列表
    labels = [item['submission_status'] for item in data]
    count = [item['count'] for item in data]
    # 设置颜色映射
    colors = {
        '答案正确/AC': '#90EE90',  # 淡绿色
        '编译错误/CE': '#FFD700',  # 浅黄色
        '部分正确/PA': '#FF69B4',
        '运行时异常/RE': '#FF69B4',
        'CPU运行超时/CTLE': '#FF69B4',
        '格式错误/PE': '#FF69B4',  # 热粉色
        '答案错误/WA': 'red',
    }

    # 生成对应的颜色列表
    color_list = [colors.get(status, 'red') for status in labels]
    # 创建饼图
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=count,
        title=f'Problem {problem_id}',
        marker=dict(colors=color_list)
    )])

    # 保存图表
    fig.write_html(f'templates/pie_chart_{problem_id}.html')


def fetch_pass_counts():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Mkl20040310',
            database='webdatabase',
            charset='utf8mb4'
        )
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT problem_id, COUNT(DISTINCT student_id) as count
                FROM student_problem
                WHERE submission_status = '答案正确/AC'
                GROUP BY problem_id;
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return []
    finally:
        connection.close()


def create_bar_chart(data, problem_ids):
    # 创建 DataFrame
    df = pd.DataFrame(data, columns=['problem_id', 'count'])

    # 按照问题ID汇总通过人数
    passed_counts = []
    for problem_id in problem_ids:
        count = df[df['problem_id'] == problem_id]['count'].sum()
        passed_counts.append(count)

    # 绘制柱状图
    fig = go.Figure(data=[
        go.Bar(
            x=problem_ids,
            y=passed_counts,
            text=passed_counts,
            textposition='outside',  # 将文本显示在柱子外部
            textfont=dict(size=28, color='black')  # 设置文本大小和颜色
        )
    ])
    # 更新布局以调整字体大小
    fig.update_layout(
        title={'text': 'Passed Count for Each Problem', 'font': {'size': 24}},
        xaxis={'title': {'text': 'Problem ID', 'font': {'size': 18}}, 'tickfont': {'size': 28}},
        yaxis={'title': {'text': 'Passed Count', 'font': {'size': 18}}, 'showticklabels': False},  # 不显示纵坐标刻度标签
        yaxis_tickmode='linear',
        yaxis_dtick=1
    )
    fig.write_html('templates/bar_chart.html')
