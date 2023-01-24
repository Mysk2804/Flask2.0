import requests


# response = requests.patch('http://127.0.0.1:5000/advertisement/',
#                         json={'title': 'My advertisement58',
#                               'description': 'Устаноdfasfasdfadsfasd!',
#                               'owner': 'Vasiliy Pypkin2'
#                               })
response = requests.get('http://127.0.0.1:5000/advertisement/1')

print(response.status_code)
print(response.json())
