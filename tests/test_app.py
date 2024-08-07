import requests

name = 'bin lad'
api_url = 'https://api.api-ninjas.com/v1/historicalfigures?name={}'.format(name)
response = requests.get(api_url, headers={'X-Api-Key': '4V0+k088YgezZZU9RdXn2A==u2EZJmHV0zegyvS9'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)