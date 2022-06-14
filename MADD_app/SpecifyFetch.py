import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


username = 'test'
password = 'testtest'
csrftoken = requests.request('GET', "https://specify-test.science.ku.dk/context/login/", verify=False).cookies.get('csrftoken')
print('csrftoken: ', csrftoken)
headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer' : 'https://specify-test.science.ku.dk/' }

response = requests.request('PUT', "https://specify-test.science.ku.dk/context/login/", data={'username' : username, 'password' : password, 'collection': 5}, headers=headers,verify=False)
print('RESPONSE: ', response.status_code)










