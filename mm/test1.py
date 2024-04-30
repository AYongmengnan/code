import re

# 示例文本
text = """
Feel free to contact by Whatsapp  : Satoshi：8299-7918
Apply NOW or Call us at +6564160506 / 85715393 / 94896696
To Apply,

☎ WhatsApp 9833-5351
☎ Another Phone: 9899 9078
☎ Yet Another Phone: 90174925
☎ Special Phone: 9327^5420
☎ Some Other Phone: 9347*5490
6564160509
✉ Email mtc011@mtcconsulting.com.sg
65 9638 3519
Only shortlisted candidate would be notified
"""


# 定义电话号码的正则表达式模式（包括之前的条件和新的条件）
phone_pattern = r'\b(?:\+?65\s*[\d\-]+|6\d{7}|8\d{7}|9\d{7}|\d{4}[\s\-]?\d{4}|\d{8}|\d{4}\^\d{4}|\d{4}\*\d{4}|\+\d{6,10})\b'

# 使用正则表达式模式提取电话号码
phone_numbers = re.findall(phone_pattern, text)

# 提取电话号码中的数字部分
# cleaned_phone_numbers = []
# for phone_number in phone_numbers:
#     digits = re.sub(r'\D', '', phone_number)  # 去除非数字字符
#     cleaned_phone_numbers.append(digits)

# 输出提取的电话号码
print("Cleaned phone numbers:")
for phone_number in phone_numbers:
    print(phone_number)
