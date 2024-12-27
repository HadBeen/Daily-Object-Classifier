import requests

url = "http://api.conceptnet.io/c/en/dog"
response = requests.get(url)
data = response.json()

print(data)
