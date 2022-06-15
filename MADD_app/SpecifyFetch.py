# -*- coding: utf-8 -*-
  
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

baseUrl = "https://specify-test.science.ku.dk/"
loginUrl = baseUrl + "context/login/"
username = 'test'
password = 'testtest'

#Connect to Specify7 API
# First step is to get a CSRF token 
csrftoken = requests.get(loginUrl, verify=False).cookies.get('csrftoken')
print('CSRF Token: ', csrftoken)

# Next step is to use token to log in 
headers = {'content-type': 'application/json', 'X-CSRFToken': csrftoken, 'Referer' : baseUrl }
data = {"username" : "test", "password" : "testtest", "collection": 4}
response = requests.put(loginUrl, data=data, headers=headers, verify=False)

print('REQUEST: ', response.request.headers)
print('RESPONSE: ', response.status_code)
print(response.headers)
print()
print('***closer look at prepared request***')
print(response.request.method)
print(response.request.headers['Content-Type'])
print(response.request.headers['Referer'])
print(response.request.headers['X-CSRFToken'])
print(response.request.body)



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




