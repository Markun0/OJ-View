import base64
from PIL import Image
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import io
import OCR  # 假设你有一个OCR模块
import tempfile  # 用于创建临时文件
from bs4 import BeautifulSoup  # 引入BeautifulSoup
import os
import mywebsql

class CatchProcession:
    def __init__(self, log_id, passwd):
        self.log_id = log_id
        self.passwd = passwd
        options = Options()
        chrome_driver_path = r'C:\Users\86133\PycharmProjects\pythonProject1\chromedriver\chromedriver.exe'
        service = Service(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        url = 'http://10.11.219.21/#/login'
        self.driver.set_window_size(1200, 800)  # 设置浏览器大小
        self.driver.get(url)

    def auto_doit(self):
        self.login_to_system()
        self.perform_search()

    def login_to_system(self):
        try:
            while True:
                # 等待用户名输入框
                username_field = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/div/form/div[1]/div/div[1]/input'))
                )
                username_field.clear()
                username_field.send_keys(self.log_id)

                # 等待密码输入框
                password_field = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/div/form/div[2]/div/div[1]/input'))
                )
                password_field.clear()
                password_field.send_keys(self.passwd)

                # 等待验证码图片
                captcha_image_element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/div/form/div[3]/div/div/div[2]/img'))
                )

                # 获取验证码图片的base64数据
                captcha_base64 = self.driver.execute_script(
                    "return arguments[0].src;", captcha_image_element
                ).split(',')[1]

                # 解码base64数据并读取图像
                captcha_image = Image.open(io.BytesIO(base64.b64decode(captcha_base64)))

                # 将图像保存到临时文件
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                    captcha_image_path = tmp_file.name
                    captcha_image.save(captcha_image_path)

                # 使用OCR处理验证码图像
                self.xxx = OCR.BaiduOCR(captcha_image_path).baiduOCR()  # 假设OCR类有一个baiduOCR方法，能处理文件路径
                print(self.xxx)

                # 等待验证码输入框
                verification_code_field = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="login-form"]/div/form/div[3]/div/div/div[1]/div/input'))
                )
                verification_code_field.clear()
                verification_code_field.send_keys(self.xxx)

                # 等待登录按钮
                login_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="login-form"]/div/form/div[4]/div/button[1]'))
                )
                login_button.click()

                # 检查登录是否成功
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="app"]/main/section/div/div[2]/div[1]/div[2]/div[2]/div/div[1]'))
                    )
                    print("Login successful.")
                    break  # 如果登录成功，退出循环
                except:
                    print("Login failed. Retrying...")

            # 进行页面操作
            self.perform_navigation()

        except Exception as e:
            print(f"An error occurred: {e}")

    def perform_navigation(self):
        try:
            # 点击腾班
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, r'//*[@id="app"]/main/section/div/div[2]/div[1]/div[2]/div[2]/div/div[1]'))
            ).click()
            time.sleep(1)

            # 点击对应实验
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, r'//*[@id="app"]/main/section/div/div/div/div[2]/div[1]/div[3]/table/tbody/tr[1]'))
            ).click()
            time.sleep(1)

            # 点击比赛详情
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, r'//*[@id="app"]/main/section/div/section/aside/div[1]/div/ul/li'))
            ).click()
            time.sleep(1)

            # # 点击排行榜
            # WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, r'//*[@id="tab-2"]'))
            # ).click()
            # time.sleep(1)

        except Exception as e:
            print(f"An error occurred during navigation: {e}")

    def perform_search(self):
        row_texts = []
        try:
            while True:
                # 等待table的tbody可见
                tbody = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="pane-2"]/div/div[2]/div[4]/div[2]/table/tbody'))
                )
                time.sleep(1)

                # 获取tbody的HTML内容
                tbody_html = tbody.get_attribute('innerHTML')

                # 使用BeautifulSoup解析HTML
                soup = BeautifulSoup(tbody_html, 'html.parser')

                # 遍历每个tr元素
                for row in soup.find_all('tr'):
                    col_texts = []
                    # 遍历每个td元素
                    for col in row.find_all('td'):
                        # 获取td文本
                        td_text = col.get_text(strip=True)
                        col_texts.append(td_text)

                    row_texts.append(col_texts)
                    # 打印每行的文本内容
                    print("\t".join(col_texts))

                # 查找并点击下一页按钮
                page_numbers = self.driver.find_elements(By.XPATH, '//*[@id="pane-2"]/div/div[3]/ul/li')
                for page in page_numbers:
                    if 'active' in page.get_attribute('class'):
                        current_page_index = page_numbers.index(page)
                        break

                # 点击下一页按钮
                if current_page_index < len(page_numbers) - 1:
                    page_numbers[current_page_index + 1].click()
                    time.sleep(1)  # 等待页面加载
                else:
                    break  # 已经是最后一页，退出循环

        except Exception as e:
            print(f"An error occurred during perform_search: {e}")
        finally:
            mywebsql.clear_and_insert_data(row_texts)
            time.sleep(1)


# def save_list_to_file(row_texts, file_name):
#     try:
#         # 获取当前脚本所在目录
#         current_dir = os.path.dirname(__file__)
#         # 构建文件路径
#         file_path = os.path.join(current_dir, file_name)
#
#         with open(file_path, 'w', encoding='utf-8') as file:
#             for row in row_texts:
#                 file.write(row + '\n')
#         print(f"数据已成功保存到文件: {file_path}")
#     except Exception as e:
#         print(f"保存文件时发生错误: {e}")



