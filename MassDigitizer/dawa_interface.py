# -*- coding: utf-8 -*-
"""
  Created on Wednesday November 30, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Interface to the Danmarks Adresser Web API 
"""

import requests
import json 
import urllib3
from pathlib import Path

# Internal Dependencies
import util 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DawaInterface():
    """
    The DAWA Interface class acts as a wrapper around a selection of API functions offered by Specify7. 
    """

    def __init__(self) -> None:
        """
        ...
        """
        # Create a session for storing cookies 
        self.spSession = requests.Session() 
        self.baseURL = 'https://api.dataforsyningen.dk/'

    def lookupKommune(self, xCoordinate, yCoordinate):
        """
        ...
        """
        apiCallString = self.baseURL + f'kommuner/reverse?x={xCoordinate}&y={yCoordinate}'
        print(apiCallString)
        response = self.spSession.get(apiCallString)

        # If succesful, load into json object 
        if response.status_code < 299:
            return json.loads(response.text)
        else: 
            return None

    def getKommuneName(self, xCoordinate, yCoordinate):
        """
        ...
        """
        
        kommune = self.lookupKommune(xCoordinate, yCoordinate)

        if kommune:
            return kommune['navn']
        else: 
            return ''

da = DawaInterface()
kommuneName = da.getKommuneName(12.58514, 55.68323)
print(f'Result: "{kommuneName}"')
