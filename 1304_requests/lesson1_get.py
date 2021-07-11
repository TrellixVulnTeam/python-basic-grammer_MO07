import requests


payload = {'key1': 'value1', 'key2': 'value2'}

r = requests.get('http://httpbin.org/get', params=payload)  # paramsパラメータにpayloadを渡すだけ！！

print(r.status_code)
print(r.text)
print(r.json())
