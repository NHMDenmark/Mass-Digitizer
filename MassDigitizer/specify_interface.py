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

#TODO Make into singleton class ??? 

from queue import Empty
import requests
import json 
import urllib3
from pathlib import Path

import global_settings as gs
import util 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# global variables 
filepath = str(Path(__file__).parent.joinpath('bootstrap').joinpath('institutions.json'))
#print('Initializing Specify Interface institutions with path: %s' % filepath)
institutions = json.load(open(filepath))
#baseURL = gs.baseURL
#loginURL = baseURL + 'context/login/'
collections = {}

# Create a session for storing cookies 
spSession = requests.Session() 

def getCSRFToken():
  # Specify7 requires a token to prevent Cross Site Request Forgery 
  # This will also return a list of the institution's collections 
  # CONTRACT
  #   Returns csrftoken (String)
  print('Get CSRF token from ', gs.baseURL)
  response = spSession.get(gs.baseURL + 'context/login/', verify=False)
  csrftoken = response.cookies.get('csrftoken')
  print(' - CSRF Token: %s' % csrftoken)
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  #print('------------------------------')
  return csrftoken

def specifyLogin(username, passwd, collection_id):
    # Function for logging in to the Specify7 API and getting the CSRF token necessary for further interactions in the session 
    # CONTRACT
    #   username (String): Specify account user name  
    #   passwd (String) : Specify account password  
    #   RETURNS (String) : The CSRF token necessary for further interactions in the session 
    print('Connecting to Specify7 API at: ' + gs.baseURL)
    csrftoken = getCSRFToken()
    csrftoken = login(username, passwd, collection_id, csrftoken)
    if verifySession(csrftoken):
        return csrftoken
    else:
        return '' 

def login(username, passwd, collectionid, csrftoken):
  # Username and password should be passed to the login function along with CSRF token 
  # After successful login a new CSRF token is issued that should be used for the continuing session 
  # CONTRACT 
  #   username (String): The Specify account's username 
  #   passwd (String): The password for the Specify account
  #   csrftoken (String): The CSRF token is required for security reasons  
  print('Log in using CSRF token & username/password')
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': gs.baseURL}
  response = spSession.put(gs.baseURL + "context/login/", json={"username": username, "password": passwd, "collection": collectionid}, headers=headers, verify=False) 
  csrftoken = response.cookies.get('csrftoken') # Keep and use new CSRF token after login
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  print(' - New CSRF Token: ', csrftoken)
  #print('------------------------------')
  return csrftoken

def specifyLogout(csrftoken):
    # Function for logging out of the Specify7 API again 
    # CONTRACT
    #   csrftoken (String) : The CSRF token required during logging in for the session 
    print('logging out of Specify...')
    logout(csrftoken)

def verifySession(csrftoken):
  # Attempt to fetch data on the current user being logged in as a way to verify the session  
  # CONTRACT 
  #   csrftoken (String): The CSRF token is required for security reasons
  #   RETURNS boolean to indicate session validity
  print('Verify session')
  validity = Empty
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': gs.baseURL}
  response = spSession.get(gs.baseURL + "context/user.json", headers=headers)
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

def getCollObject(collectionObjectId, csrftoken):
  # Fetches collection objects from the Specify API using their primary key 
  # CONTRACT 
  #   collectionObjectId (Integer): The primary key of the collectionObject, which is not the same as catalog number  
  #   csrftoken (String): The CSRF token is required for security reasons 
  #   RETURNS fetched object 
  print('Query collection object')
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': gs.baseURL}
  response = spSession.get(gs.baseURL + "api/specify/collectionobject/" + str(collectionObjectId)  + "/", headers=headers)
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  if response.status_code < 299:
    object = response.json()
    print(' - Catalog number: %s' % response.json()['catalognumber'])
  else:
    object = {}
  #print('------------------------------')
  return object 

def getSpecifyObject(objectName, objectId, csrftoken):
  # Generic method for fetching objects from the Specify API using their primary key
  # CONTRACT 
  #   objectName (String): The API's name for the object to be fetched  
  #   objectId (Integer): The primary key of the object
  #   csrftoken (String): The CSRF token is required for security reasons  
  #   RETURNS fetched object 
  #print('Fetching ' + objectName + ' object on id: ' + str(objectId))
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': gs.baseURL, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}
  apiCallString = "%sapi/specify/%s/%d/" %(gs.baseURL, objectName, objectId)
  #print(apiCallString)
  response = spSession.get(apiCallString, headers=headers)
  #print(' - Response: %s %s' %(str(response.status_code), response.reason))
  #print(' - Referer: %s' % response.request.headers['referer'])
  if response.status_code < 299:
    object = response.json()
  else: 
    object = Empty
  #print('------------------------------')
  return object 

def postSpecifyObject(objectName, objectId, specifyObject, csrftoken):
  # TODO not yet working 
  #   RETURNS posted object 
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'referer': gs.baseURL}
  apiCallString = "%sapi/specify/%s/%d/" %(gs.baseURL, objectName, objectId)
  print(apiCallString)
  # TODO API PUT command throws 403 Error ("Forbidden")
  response = spSession.post(apiCallString, headers=headers, data=specifyObject)
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  if response.status_code < 299:
    object = response.json()
  else: 
    object = Empty
  return object 

def putSpecifyObject(objectName, objectId, specifyObject, csrftoken):
  # TODO not yet working 
  #   RETURNS put object 
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'referer': gs.baseURL}
  apiCallString = "%sapi/specify/%s/%d/" %(gs.baseURL, objectName, objectId)
  print(apiCallString)
  # TODO API PUT command throws 403 Error ("Forbidden")
  response = spSession.put(apiCallString, headers=headers, data=specifyObject)
  print(' - Response: %s %s' %(str(response.status_code), response.reason))
  if response.status_code < 299:
    object = response.json()
  else: 
    object = Empty
  return object 

def getSpecifyObjects(objectName, csrftoken, limit=100, offset=0, filters={}):
  # Generic method for fetching object sets from the Specify API based on object name 
  # CONTRACT 
  #   objectName (String): The API's name for the objects to be queried  
  #   csrftoken (String): The CSRF token is required for security reasons
  #   limit (Integer): Maximum amount of records to be retrieve at a time. Default value: 100 
  #   offset (Integer): Offset of the records to be retrieved for enabling paging. Default value: 0 
  #   filters (Dictionary) : Optional filters as a key, value pair of strings 
  #   RETURNS fetched object set 
  #print('Fetching "%s" with limit %d and offset %d ' %(objectName, limit, offset))
  objectSet = {}
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': gs.baseURL}
  filterString = ""
  for key in filters:
    filterString += '&' + key + '=' + filters[key]
  apiCallString = "%sapi/specify/%s/?limit=%d&offset=%d%s" %(gs.baseURL, objectName, limit, offset, filterString)
  #print("   -> " + apiCallString)

  response = spSession.get(apiCallString, headers=headers)
  #print(' - Response: %s %s' %(str(response.status_code), response.reason))
  if response.status_code < 299:
    objectSet = json.loads(response.text)['objects'] # get collections from json string and convert into dictionary
    #print(' - Received %d object(s)' % len(objectSet))
  
  return objectSet 

def directAPIcall(callString, csrftoken):
  # Generic method for allowing a direct call to the API using a call string that is appended to the baseURL
  # CONTRACT
  #   callString (String): The string to the appended to the base URL of the API
  #   csrftoken (String): The CSRF token is required for security reasons  
  #   RETURNS response object  
  apiCallString = "%s%s" %(gs.baseURL, callString)
  print(apiCallString)
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': gs.baseURL}
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
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': gs.baseURL}
  response = spSession.put(gs.baseURL + "context/login/", data="{\"username\": null, \"password\": null, \"collection\": 688130}", headers=headers)
  print(' - %s %s ' %(str(response.status_code), response.reason))
  #print('------------------------------')

def getInitialCollections():
  # Specify7 will return a list of the institution's collections upon initial contact
  # CONTRACT
  #   RETURNS collections list (dictionary)
  print('Get initial collections')
  response = spSession.get(gs.baseURL + "context/login/", verify=False)
  print(' - Response: ' + str(response.status_code) + " " + response.reason)
  collections = json.loads(response.text)['collections'] # get collections from json string and convert into dictionary
  collections = {k: v for v, k in collections.items()} # invert keys and values that for some reason are delivered switched around 
  print(' - Received %d collection(s)' % len(collections))
  #print('------------------------------')
  return collections

def mergeTaxa(source_id, target_id, csrftoken):
  # TODO 
  #   Example: 
  #     POST URL:   https://specify-test.science.ku.dk/api/specify_tree/taxon/367622/merge/ 
  #     POST DATA:  target: "432192"  
  #   RETURNS response object 
  headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'referer': gs.baseURL, } 
  apiCallString = "%sapi/specify_tree/taxon/%s/merge/?target=%s"%(gs.baseURL, source_id, target_id)
  print(" - API call: %s"%apiCallString)

  #print(spSession.cookies)

  input('ready?')
  response = spSession.post(apiCallString, headers=headers, json={"target": target_id}) 

  #print(response.request.body)
  util.pretty_print_POST(response.request)
  #print('---------------------------')
  print(' - Response: %s %s' %(str(response.status_code), response.reason))

  if response.status_code < 299:
    object = response.json()
  else: 
    object = Empty
  return object  



#util.clear()
#getInitialCollections()