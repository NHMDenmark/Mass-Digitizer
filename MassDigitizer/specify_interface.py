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

# Internal Dependencies
import data_access
import global_settings as gs

db = data_access.DataAccess(gs.databaseName)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SpecifyInterface():
  """
  The Specify Interface class acts as a wrapper around a selection of API functions offered by Specify7. 
  The URL of the specify server to be accessed is set in global_settings.py 
  Interactions with Specify7 require a token to prevent Cross Site Request Forgery (CSRF). 
  In order to log in, an initial CSRF token must be acquired by accessing .../context/login/ (getCSRFToken).
  The initial CSRF token kan be used to subsequently log in using a Specify username/password combination (specifyLogin). 
  """

  def __init__(self, token=None) -> None:
    """ 
    CONSTRUCTOR
    Creates a session for storing cookies  
    """      
    self.spSession = requests.Session() 
    self.csrfToken = ''

  def getCSRFToken(self):
    """ 
    Specify7 requires a token to prevent Cross Site Request Forgery 
    This will also return a list of the institution's collections 
    CONTRACT
       Returns csrftoken (String)
    """   
    print('Get CSRF token from ', gs.baseURL)
    response = self.spSession.get(gs.baseURL + 'context/login/', verify=False)
    csrftoken = response.cookies.get('csrftoken')
    #print(' - Response: %s %s' %(str(response.status_code), response.reason))
    #print(' - CSRF Token: %s' % csrftoken)
    #print('------------------------------')
    return csrftoken

  def specifyLogin(self, username, passwd, collection_id):
      """ 
      Function for logging in to the Specify7 API and getting the CSRF token necessary for further interactions in the session 
      CONTRACT
        username (String) : Specify account user name  
        passwd   (String) : Specify account password  
        RETURNS  (String) : The CSRF token necessary for further interactions in the session 
      """
      print('Connecting to Specify7 API at: ' + gs.baseURL)
      token = self.login(username, passwd, collection_id, self.getCSRFToken())
      #print(' - Log in CSRF Token: %s' % token)
      if self.verifySession(token):
          return token
      else:
          return '' 

  def login(self, username, passwd, collectionid, csrftoken):
    """ 
    Username and password should be passed to the login function along with CSRF token 
    After successful login a new CSRF token is issued that should be used for the continuing session 
    CONTRACT 
      username  (String) : The Specify account's username 
      passwd    (String) : The password for the Specify account
      csrftoken (String) : The CSRF token is required for security reasons  
    """
    print('Log in using CSRF token & username/password')
    headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer': gs.baseURL}
    response = self.spSession.put(gs.baseURL + "context/login/", json={"username": username, "password": passwd, "collection": collectionid}, headers=headers, verify=False) 
    csrftoken = response.cookies.get('csrftoken') # Keep and use new CSRF token after login
    print(' - Response: %s %s' %(str(response.status_code), response.reason))
    print(' - New CSRF Token: ', csrftoken)
    #print('------------------------------')
    return csrftoken

  def verifySession(self, token):
    """ 
    Attempt to fetch data on the current user being logged in as a way to verify the session  
    CONTRACT 
      token (String) : The CSRF token is required for security reasons
      RETURNS boolean to indicate session validity
    """  
    print('Verify session')
    validity = None

    headers = {'content-type': 'application/json', 'X-CSRFToken': self.csrfToken, 'Referer': gs.baseURL}
    print(gs.baseURL + "context/user.json", headers)

    headers = {'content-type': 'application/json', 'X-CSRFToken': token, 'Referer': gs.baseURL}

    response = self.spSession.get(gs.baseURL + "context/user.json", headers=headers)
    print(' - Response: %s %s' %(str(response.status_code), response.reason))
    if response.status_code > 299:
      # print(response.text)
      print(' - Invalid session')
      validity = False 
    else:
      print(' - Session verified. User id: ' + str(response.json()['id']))
      validity = True
      self.csrfToken = token
    #print('------------------------------')
    return validity

  def specifyLogout(self):#, csrftoken):
      """ 
      Function for logging out of the Specify7 API again 
      CONTRACT
        NOTE DEPRECATED: csrftoken (String) : The CSRF token required during logging in for the session 
      """
      print('logging out of Specify...')
      self.logout(self.csrftoken)

  def getCollObject(self, collectionObjectId):#, csrftoken):
    """ 
    Fetches collection objects from the Specify API using their primary key 
    CONTRACT 
      collectionObjectId (Integer) : The primary key of the collectionObject, which is not the same as catalog number  
      NOTE DEPRECATED: csrftoken          (String)  : The CSRF token is required for security reasons 
      RETURNS fetched object 
    """   
    print('Query collection object')
    headers = {'content-type': 'application/json', 'X-CSRFToken': self.csrfToken, 'Referer': gs.baseURL}
    response = self.spSession.get(gs.baseURL + "api/specify/collectionobject/" + str(collectionObjectId)  + "/", headers=headers)
    print(' - Response: %s %s' %(str(response.status_code), response.reason))
    if response.status_code < 299:
      object = response.json()
      catalogNr = response.json()['catalognumber']
      print(f' - Catalog number: {catalogNr}')
    else:
      object = {}
    #print('------------------------------')
    return object 

  def getSpecifyObjects(self, objectName, limit=100, offset=0, filters={}):
    """ 
    Generic method for fetching object sets from the Specify API based on object name 
    CONTRACT 
      objectName (String)     : The API's name for the objects to be queried  
      NOTE DEPRECATED: csrftoken  (String)     : The CSRF token is required for security reasons
      limit      (Integer)    : Maximum amount of records to be retrieve at a time. Default value: 100 
      offset     (Integer)    : Offset of the records to be retrieved for enabling paging. Default value: 0 
      filters    (Dictionary) : Optional filters as a key, value pair of strings 
      RETURNS fetched object set 
    """ 
    #print('Fetching "%s" with limit %d and offset %d ' %(objectName, limit, offset))
    objectSet = {}
    headers = {'content-type': 'application/json', 'X-CSRFToken': self.csrfToken, 'Referer': gs.baseURL}
    filterString = ""
    for key in filters:
      filterString += '&' + key + '=' + filters[key]
    apiCallString = f'{gs.baseURL}api/specify/{objectName}/?limit={limit}&offset={offset}{filterString}'
    #print("   -> " + apiCallString)

    response = self.spSession.get(apiCallString, headers=headers)
    #print(' - Response: %s %s' %(str(response.status_code), response.reason))
    if response.status_code < 299:
      objectSet = json.loads(response.text)['objects'] # get collections from json string and convert into dictionary
      #print(' - Received %d object(s)' % len(objectSet))
    
    return objectSet 

  def getSpecifyObject(self, objectName, objectId):#, csrftoken):
    """ 
    Generic method for fetching objects from the Specify API using their primary key
    CONTRACT 
      objectName (String)  : The API's name for the object to be fetched  
      objectId   (Integer) : The primary key of the object
      NOTE DEPRECATED: csrftoken  (String)  : The CSRF token is required for security reasons  
      RETURNS fetched object 
    """ 
    #print('Fetching ' + objectName + ' object on id: ' + str(objectId))
    headers = {'content-type': 'application/json', 'X-CSRFToken': self.csrfToken, 'Referer': gs.baseURL}
    apiCallString = f'{gs.baseURL}api/specify/{objectName}/{objectId}/' 
    #print(apiCallString)
    response = self.spSession.get(apiCallString, headers=headers, verify=False)
    #print(' - Response: %s %s' %(str(response.status_code), response.reason))
    #print(' - Referer: %s' % response.request.headers['referer'])
    if response.status_code < 299:
      object = response.json()
    else: 
      object = None
    #print()
    #util.pretty_print_POST(response.request)
    #print()
    return object 

  def putSpecifyObject(self, objectName, objectId, specifyObject):#, csrftoken):
    """ 
    Generic method for putting changes to an existing object to the Specify API using their primary key 
    CONTRACT 
      objectName    (String)  : The API's name for the object to be fetched  
      objectId      (Integer) : The primary key of the object 
      specifyObject (JSON)    : The (possibly altered) state of the object 
      NOTE DEPRECATED: csrftoken     (String)  : The CSRF token is required for security reasons  
      RETURNS response status code (String)
    """
    headers = {'content-type': 'application/json', 'X-CSRFToken': self.csrfToken, 'referer': gs.baseURL}
    apiCallString = "%sapi/specify/%s/%d/" %(gs.baseURL, objectName, objectId)
    #print(apiCallString)
    #print(specifyObject)
    # TODO API PUT command throws 500 Error ("Internal Server Error")
    response = self.spSession.put(apiCallString, data=json.dumps(specifyObject), headers=headers)
    #response = requests.put(apiCallString, data=specifyObject, json=specifyObject, headers=headers)
    #print(' - Response: %s %s' %(str(response.status_code), response.reason))
    # if response.status_code < 299:
    #   object = response.json()
    # else: 
    #  object = None
    # return object 
    return response.status_code 

  def postSpecifyObject(self, objectName, specifyObject):#, csrftoken):
    """ 
    Generic method for posting a new object to the Specify API including a primary key
    CONTRACT 
      objectName    (String)  : The API's name for the object to be fetched  
      specifyObject (JSON)    : The state of the object to be created 
      NOTE DEPRECATED: csrftoken     (String)  : The CSRF token is required for security reasons  
      RETURNS response  
    """ 
    headers = {'content-type': 'application/json', 'X-CSRFToken': self.csrfToken, 'referer': gs.baseURL}
    apiCallString = "%sapi/specify/%s/%d/" %(gs.baseURL, objectName)
    print(apiCallString)
    # TODO API PUT command throws 403 Error ("Forbidden")
    response = self.spSession.post(apiCallString, headers=headers, data=specifyObject)
    #print(' - Response: %s %s' %(str(response.status_code), response.reason))
    # if response.status_code < 299:
    #   object = response.json()
    # else: 
    #  object = None
    # return object 
    return response.status_code 

  def directAPIcall(self, callString):#, csrftoken):
    """ 
    Generic method for allowing a direct call to the API using a call string that is appended to the baseURL
    CONTRACT
      callString (String) : The string to the appended to the base URL of the API
      NOTE DEPRECATED: csrftoken  (String) : The CSRF token is required for security reasons  
      RETURNS response object  
    """ 
    apiCallString = "%s%s" %(gs.baseURL, callString)
    print(apiCallString)
    headers = {'content-type': 'application/json', 'X-CSRFToken': self.csrfToken, 'Referer': gs.baseURL}
    response = self.spSession.get(apiCallString, headers=headers)
    print(' - Response: %s %s' %(str(response.status_code), response.reason))
    
    if response.status_code < 299:
      return json.loads(response.text)
    return {} 

  def logout(self):#, csrftoken):
    """ 
    Logging out closes the session on both ends 
    CONTRACT 
      NOTE DEPRECATED: csrftoken (String) : The CSRF token is required for security reasons
    """ 
    print('Log out')
    headers = {'content-type': 'application/json', 'X-CSRFToken': self.csrfToken, 'Referer': gs.baseURL}
    response = self.spSession.put(gs.baseURL + "context/login/", data="{\"username\": null, \"password\": null, \"collection\": 688130}", headers=headers)
    print(' - %s %s ' %(str(response.status_code), response.reason))
    #print('------------------------------')

  def getInitialCollections(self):
    """ 
    Specify7 will return a list of the institution's collections upon initial contact
    CONTRACT
      RETURNS collections list (dictionary)
    """ 
    print('Get initial collections')
    response = self.spSession.get(gs.baseURL + "context/login/", verify=False)
    print(' - Response: ' + str(response.status_code) + " " + response.reason)
    collections = json.loads(response.text)['collections'] # get collections from json string and convert into dictionary
    collections = {k: v for v, k in collections.items()} # invert keys and values that for some reason are delivered switched around 
    print(' - Received %d collection(s)' % len(collections))
    #print('------------------------------')
    return collections

  def mergeTaxa(self, source_id, target_id):#, csrftoken):
    """
    Special function for merging taxa. 
    Merging is done from the source taxon to the target taxon. 
    The source taxon will be deleted and the target taxon and its Specify id will prevail. 
    CONTRACT 
      source_id (int)    : Specify ID of the taxon to be merged into the target taxon 
      target_id (int)    : Specify ID of the taxon to be merged with (the target taxon)
      NOTE DEPRECATED: csrftoken (String) : The CSRF token is required for security reasons
      RETURNS response object 
    """   
    headers = {'X-CSRFToken': self.csrfToken, 'referer': gs.baseURL, } 
    apiCallString = "%sapi/specify_tree/taxon/%s/merge/"%(gs.baseURL, source_id)
    print(" - API call: %s"%apiCallString)

    #input('ready?')
    response = self.spSession.post(apiCallString, headers=headers, data={'target' : target_id }, timeout=480) 

    #print(response.request.body)
    #util.pretty_print_POST(response.request)
    #print('---------------------------')
    #print(' - Response: %s %s %s.' %(str(response.status_code), response.reason, response.text))

    # if response.status_code < 299:
    #   object = response.json()
    # else: 
    #   object = None
    # return object  

    return response

si = SpecifyInterface()
gs.baseURL = "https://specify-test.science.ku.dk/"
tok = si.getCSRFToken()
print(tok)
si.verifySession(tok)