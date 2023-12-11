import requests

response = requests.get('https://httpbin.org/ip')
print('Your IP is:', response.json()['origin'])
