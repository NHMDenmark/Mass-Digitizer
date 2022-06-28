# -*- coding: utf-8 -*-
"""
  Created on Tuesday June 14, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Interface to the Specify API
"""
import requests
import json 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from asyncio.windows_events import NULL
import util

# global variables 
# institutions = json.load(open('bootstrap/institutions.json'))
baseURL = 'https://specify-test.science.ku.dk/' # institutions[0]['URL']
loginURL = baseURL + 'context/login/'
collections = {}

# Create a session for storing cookies 
spSession = requests.Session() 

def initInstitution(_baseURL):
  # Set up baseURL for relevant institution
  # CONTRACT 
  #    _baseURL (String): institution's base URL 
  print('Set base URL: ' + _baseURL)
  baseURL = _baseURL
  loginURL = baseURL + 'context/login/'
  #print('------------------------------')

def getCSRFToken():
  # Specify7 requires a token to prevent Cross Site Request Forgery 
  # This will also return a list of the institution's collections 
  # CONTRACT
  #   Returns csrftoken (String)
  print('Get CSRF token')
  response = spSession.get(loginURL, verify=False)
  csrftoken = response.cookies.get('csrftoken')
  print(' - CSRF Token: %s' % csrftoken)
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  #print('------------------------------')
  return csrftoken

def login(username, passwd, csrftoken):
  # Username and password should be passed to the login function along with CSRF token 
  # After successful login a new CSRF token is issued that should be used for the continuing session 
  # CONTRACT 
  #   username (String): The Specify account's username 
  #   passwd (String): The password for the Specify account
  #   csrftoken (String): The CSRF token is required for security reasons  
  print('Log in using CSRF token & username/password')
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  response = spSession.put(baseURL + "context/login/", json={"username": username, "password": passwd, "collection": 851970}, headers=headers, verify=False)
  csrftoken = response.cookies.get('csrftoken') # Keep and use new CSRF token after login
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  print(' - New CSRF Token: ', csrftoken)
  #print('------------------------------')
  return csrftoken

def verifySession(csrftoken):
  # Attempt to fetch data on the current user being logged in as a way to verify the session  
  # CONTRACT 
  #   csrftoken (String): The CSRF token is required for security reasons
  #   Returns boolean to indicate session validity
  print('Verify session')
  validity = NULL
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  response = spSession.get(baseURL + "context/user.json", headers=headers)
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  if response.status_code > 299:
    # print(response.text)
    print(' - Invalid session')
    validity = False 
  else:
    print(' - Session verified. User id: ' + str(response.json()['id']))
    validity = True
  #print('------------------------------')
  return validity

def fetchCollObject(collectionObjectId, csrftoken):
  # Fetches collection objects from the Specify API using their primary key 
  # CONTRACT 
  #   collectionObjectId (Integer): The primary key of the collectionObject, which is not the same as catalog number  
  #   csrftoken (String): The CSRF token is required for security reasons 
  print('Query collection object')
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  response = spSession.get(baseURL + "api/specify/collectionobject/" + str(collectionObjectId)  + "/", headers=headers)
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  print(' - Catalog number: %s' & response.json()['catalognumber'])
  #print('------------------------------')

def fetchSpecifyObject(objectName, objectId, csrftoken):
  # Generic method for fetching objects from the Specify API using their primary key
  # CONTRACT 
  #   objectName (String): The API's name for the object to be fetched  
  #   objectId (Integer): The primary key of the object
  #   csrftoken (String): The CSRF token is required for security reasons  
  #   RETURNS fetched object 
  print('Fetching ' + objectName + ' object on id: ' + str(objectId))
  object = {}
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  apiCallString = "%sapi/specify/%s/%d/" %(baseURL, objectName, objectId)
  print(apiCallString)
  response = spSession.get(apiCallString, headers=headers)
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  if response.status_code < 299:
    object = response.json()
  #print('------------------------------')
  return object 

def fetchSpecifyObjects(objectName, csrftoken, limit=100, offset=0, filters={}):
  # Generic method for fetching object sets from the Specify API based on object name 
  # CONTRACT 
  #   objectName (String): The API's name for the objects to be queried  
  #   csrftoken (String): The CSRF token is required for security reasons
  #   limit (Integer): Maximum amount of records to be retrieve at a time. Default value: 100 
  #   offset (Integer): Offset of the records to be retrieved for enabling paging. Default value: 0 
  #   filters TODO 
  #   RETURNS fetched object set 
  print('Fetching "%s" with limit %d and offset %d ' %(objectName, limit, offset))
  objectSet = {}
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  filterString = ""
  for key in filters:
    filterString += '&' + key + '=' + filters[key]
  apiCallString = "%sapi/specify/%s/?limit=%d&offset=%d%s" %(baseURL, objectName, limit, offset, filterString)
  print(" -> " + apiCallString)
  response = spSession.get(apiCallString, headers=headers)
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  if response.status_code < 299:
    objectSet = json.loads(response.text)['objects'] # get collections from json string and convert into dictionary
    print(' - Received %d object(s)' % len(objectSet))
  #print('------------------------------')
  return objectSet 

def directAPIcall(callString, csrftoken):
  # Generic method for allowing a direct call to the API using a call string that is appended to the baseURL
  # CONTRACT
  #   callString (String): The string to the appended to the base URL of the API
  #   csrftoken (String): The CSRF token is required for security reasons
  apiCallString = "%s%s" %(baseURL, callString)
  print(apiCallString)
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  response = spSession.get(apiCallString, headers=headers)
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  
  if response.status_code < 299:
    return json.loads(response.text)
  return {}

def logout(csrftoken):
  # Logging out closes the session on both ends 
  # CONTRACT 
  #   csrftoken (String): The CSRF token is required for security reasons
  print('Log out')
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': baseURL}
  response = spSession.put(baseURL + "context/login/", data="{\"username\": null, \"password\": null, \"collection\": 688130}", headers=headers)
  print(' - %s %s ' %(str(response.status_code), response.reason))
  #print('------------------------------')

def getInitialCollections():
  # Specify7 will return a list of the institution's collections upon initial contact
  # CONTRACT
  #   RETURNS collections list (dictionary)
  print('Get initial collections')
  response = spSession.get(loginURL, verify=False)
  print(' - Response: ' + str(response.status_code) + " " + response.reason)
  collections = json.loads(response.text)['collections'] # get collections from json string and convert into dictionary
  collections = {k: v for v, k in collections.items()} # invert keys and values that for some reason are delivered switched around 
  print(' - Received %d collection(s)' % len(collections))
  #print('------------------------------')
  return collections

#util.clear()
#getInitialCollections()