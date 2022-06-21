# -*- coding: utf-8 -*-
import requests
import json 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from getpass import getpass

# global variables 
institutions = json.load(open('bootstrap/institutions.json'))
baseURL = institutions[0]['URL']
loginURL = baseURL + 'context/login/'
collections = {}

# Create a session for storing cookies 
spSession = requests.Session() 

def getCSRFToken():
  # Specify7 requires a token to prevent Cross Site Request Forgery 
  # This will also return a list of the institution's collections 
  print('get CSRF token')
  response = spSession.get(loginURL, verify=False)
  csrftoken = response.cookies.get('csrftoken')
  # collections = json.load(response.text)
  print('response: ' + str(response.status_code) + " " + response.reason)
  print('CSRF Token: ', csrftoken)
  # print(collections[0])
  print('----------')
  return csrftoken

def login(username, passwd, csrftoken):
  # username and password should be passed to the login function along with CSRF token 
  # after successful login a new CSRF token is issued that should be used for the continuing session 
  print('log in using CSRF token & username/password')
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  response = spSession.put(baseURL + "context/login/", json={"username": username, "password": passwd, "collection": 851970}, headers=headers, verify=False)
  csrftoken = response.cookies.get('csrftoken') # Keep and use new CSRF token after login
  print('response: ' + str(response.status_code) + " " + response.reason)
  print('New CSRF Token: ', csrftoken)
  print('----------')
  return csrftoken

def verifySession(csrftoken):
  # Attempt to retrieve data on the current user being logged in as a way to verify the session  
  # The CSRF token is required for security reasons 
  print('verify session')
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  response = spSession.get(baseURL + "context/user.json", headers=headers)
  print('response: ' + str(response.status_code) + " " + response.reason)
  if response.status_code > 299:
    # print(response.text)
    print('something went wrong...')
  else:
    print('user id: ' + str(response.json()['id']))
  print('----------')

def queryCollObject(collectionObjectId, csrftoken):
  # Collection Objects can be queried using their primary key, which is not the same as catalog number  
  # The CSRF token is required for security reasons 
  print('query object')
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  response = spSession.get(baseURL + "api/specify/collectionobject/" + str(collectionObjectId)  + "/", headers=headers)
  print('response: ' + str(response.status_code) + " " + response.reason)
  print('catalog number: ' + response.json()['catalognumber'])
  print('----------')

def logout(csrftoken):
  # Logging out closes the session on both ends 
  # The CSRF token is required for security reasons 
  print('log out')
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  response = spSession.put(baseURL + "context/login/", data="{\"username\": null, \"password\": null, \"collection\": 688130}", headers=headers)
  print(str(response.status_code) + " " + response.reason)
  print('----------')


#Connect to Specify7 API
# First step is to get a CSRF token 
csrftoken = getCSRFToken()
# Ask for username and password from user
print('get username/password from input')
username = input()
passwd = getpass()
print('username: "%", password: "%"', username, passwd)
# Next step is to use csrf token to log in 
csrftoken = login(username, passwd, csrftoken)
#verify session to check all is OK 
verifySession(csrftoken)
# query some random collection object 
queryCollObject(501269, csrftoken)
#log out
logout(csrftoken)


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




