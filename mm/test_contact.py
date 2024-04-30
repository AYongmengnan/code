import re

text = """
Office number 6980 6180 Monday to Friday (09:00am to 05:00pm) OR                                        Email your updated Resume to hr-admin@htports.com or siteadmin@hiaptong.com 

Interested applicants please Telegram me @MinminJoy or Wa.me/6598732245 and look for JOYCE HE

Posted By:    Varick Lee Zhao Yi
Contact:    +65 81579715
Email:    varickzy.lee@recruitfirst.co
    R2197221
https://about.recruitfirst.co/varickzy.lee

Office number 6980 6180 Monday to Friday (09:00am to 05:00pm) OR     Email your updated Resume to hr-admin@htports.com or siteadmin@hiaptong.com

Office number 6980 6180 Monday to Friday (09:00am to 05:00pm) OR                                        Email your updated Resume to hr-admin@htports.com or siteadmin@hiaptong.com


Interested candidate click to apply❗️

Just a short 2 minute might change your career path❗️

Contact Ted @heeeearma via 88751691 Whatsapp  !!
"""

# 匹配电话号码的正则表达式
phone_pattern = r'\b(?:\+?65\s*[\d\-]+|6\d{7}|8\d{7}|9\d{7}|\d{4}[\s\-]?\d{4}|\d{8}|\d{4}\^\d{4}|\d{4}\*\d{4}|\+\d{6,10})\b'

# 匹配电子邮件地址的正则表达式
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# 匹配Telegram的正则表达式
telegram_pattern =  r'(?<!\w)@[\w\d_]+'

# 匹配WhatsApp的正则表达式
whatsapp_pattern = r'Wa\.me\/(\d+)'

# 查找匹配的电话号码
phone_numbers = re.findall(phone_pattern, text)
# print("电话号码:", [number[0] or number[1] for number in phone_numbers])
print("电话号码:", phone_numbers)

# 查找匹配的电子邮件地址
emails = re.findall(email_pattern, text)
print("电子邮件地址:", emails)

# 查找匹配的Telegram用户名
telegram_usernames = re.findall(telegram_pattern, text)
print("Telegram用户名:", telegram_usernames)

# 查找匹配的WhatsApp号码
whatsapp_numbers = re.findall(whatsapp_pattern, text)
print("WhatsApp号码:", whatsapp_numbers)
