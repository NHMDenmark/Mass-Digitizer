# -*- coding: utf-8 -*-
  
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from getpass import getpass

baseURL = "https://specify-test.science.ku.dk/"
loginURL = baseURL + "context/login/"

# Create a session for storing cookies 
sess = requests.Session() 

#Connect to Specify7 API
# First step is to get a CSRF token 
print('get CSRF token')
response = sess.get(loginURL, verify=False)
csrftoken = response.cookies.get('csrftoken')
print('response: ' + str(response.status_code) + " " + response.reason)
print('CSRF Token: ', csrftoken)

# Ask for username and password from user
print('get username/password from input')
username = input()
passwd = getpass()
print('username: "%", password: "%"', username, passwd)

# Next step is to use csrf token to log in 
print('log in using CSRF token & username/password')
headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
response = sess.put(baseURL + "context/login/", json={"username": username, "password": passwd, "collection": 851970}, headers=headers, verify=False)
cookies = response.cookies
csrftoken = response.cookies.get('csrftoken') # Keep and use new CSRF token after login
print('response: ' + str(response.status_code) + " " + response.reason)
print('New CSRF Token: ', csrftoken)

#verify session
print('verify session')
headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
response = sess.get(baseURL + "context/user.json", headers=headers)
print('response: ' + str(response.status_code) + " " + response.reason)
if response.status_code > 299:
  # print(response.text)
  print('something went wrong...')
else:
  print('user id: ' + str(response.json()['id']))

#query object 
print('query object')
response = sess.get(baseURL + "api/specify/collectionobject/501269/", headers=headers)
print('response: ' + str(response.status_code) + " " + response.reason)
print('catalog number: ' + response.json()['catalognumber'])
print()

"""
  Created on Tuesday June 14, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  Plants of the World Online taxonomy https://hosted-datasets.gbif.org/datasets/wcvp.zip is used in this exploration.

  PURPOSE: Fetching and synchronizing with the Specify API
  """




