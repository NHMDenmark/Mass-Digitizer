# -*- coding: utf-8 -*-
"""
  Created on August 17, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Automate merging duplicates through the Specify API 
"""

from getpass import getpass

import specify_interface as sp
import global_settings as gs 

gs.baseURL = 'https://specify-test.science.ku.dk/'

def merge(source_target_tuple_list, spusername, sppassword, collection_id):
    #TODO function contract   
    # 

    token = sp.specifyLogin(spusername, sppassword, collection_id)
    if token == '': return 'Authentication error!'
    
    for duplicate in source_target_tuple_list: 
        source_taxon_id = duplicate[0]
        target_taxon_id = duplicate[1]
        print('merging %s with %s ...'%(source_taxon_id, target_taxon_id))
        print(sp.mergeTaxa(source_taxon_id, target_taxon_id, token))

def testcode():
    # duplicate1 = (8888888,8888888)
    # duplicate2 = (9999999,9999999)

    # duplicate_list = [duplicate1, duplicate2]

    # merge(duplicate_list,'fedor.steeman',input('password:'), 688130)

    max_tries = 10
    while max_tries > 0:
        token = sp.specifyLogin(input('Enter username: '), getpass('Enter password: '), 688130)
        if token != '': break
        else:
            print('Login failed...')
            if input('Try again? (y/n)') == 'n': break
        max_tries = max_tries - 1
        print('Attempts left: %i' % max_tries)

    if token != '':
        source_taxon_id = input('enter source taxon id:')
        target_taxon_id = input('enter target taxon id:')

        sp.mergeTaxa(source_taxon_id, target_taxon_id, token)

    print('exiting...')


testcode()