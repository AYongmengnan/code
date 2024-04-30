import html

def decode_email(encoded_path, encoded_email):
    def decode_email_address(encoded_address, key):
        decoded = ''.join(chr(int(encoded_address[i:i+2], 16) ^ key) for i in range(2, len(encoded_address), 2))
        return html.unescape(decoded)

    start_index = encoded_path.find("#") + 1
    key = int(encoded_email[:2], 16)
    return decode_email_address(encoded_email[start_index:], key)

# 测试
encoded_path = "/cdn-cgi/l/email-protection"
encoded_email = "e38095bc8482919aa3848c8c87898c8180918682978a8c8d90cd808c8ecd9084"
decoded_email = decode_email(encoded_path, encoded_email)
print("Decoded email:",decoded_email)
