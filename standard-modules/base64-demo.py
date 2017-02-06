import base64

str = 'hello world'

base64_str = base64.b64encode(bytes(str,encoding='utf8'))
print(base64_str)

print(base64.b64decode(base64_str))