import re

# 输入字符串
input_str = "00:32:10"

# 定义正则表达式
time_pattern = r'(\d{2}:\d{2}:\d{2})'
value_pattern = r'(-\d+)?$'

# 使用正则表达式进行匹配
time_match = re.search(time_pattern, input_str)
value_match = re.search(value_pattern, input_str)

# 提取匹配的结果
time_result = time_match.group(1) if time_match else None
value_result = int(value_match.group(1)) if value_match and value_match.group(1) else None

# 输出结果
print("时间:", time_result)
print("数值:", value_result)
