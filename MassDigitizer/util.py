# -*- coding: utf-8 -*-
"""
  Created on June 24, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Assemblage of generic utility functions used across the application. 
"""

from hashlib import new
from os import system, name

def clear():
   # Clear CLI screen 
   # for windows
   if name == 'nt':
      _ = system('cls')

   # for mac and linux
   else:
    _ = system('clear')

def shrink_dict(original_dict, input_string):
   # TODO Complete function contract
   # Filter entries in dictionary based on initial string (starts with)

   shrunken_dict = {}
   print('Dictionary length = ', len(original_dict))
   for j in original_dict:
      if j[0:len(input_string)] == input_string:
         shrunken_dict[j] = original_dict[j]
   return shrunken_dict

def convert_dbrow_list(list, addEmptyRow=False):
   # TODO complete function contract
   # Converts datarow list to name array 
   new_list = []
   if addEmptyRow: new_list.append('-please select-')
   for item in list:
      new_list.append(item['name'])

   return new_list

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
    print('------------END------------')

