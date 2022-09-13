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
import util

gs.baseURL = 'https://specify-test.science.ku.dk/'

""" def merge(source_taxon_id, target_taxon_id):
    
    sp.mergeTaxa(source_taxon_id, target_taxon_id)

    pass """

# TEST CODE
#util.clear()

# Save SSL keys to "sslkeylog.txt" in this directory
# Note that you only have to do this once while this is in scope
#sslkeylog.set_keylog("sslkeylog.txt")

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
    #collectionid = input('choose collection:')
    #sp.choose_collection(collectionid,token)

    source_taxon_id = 367103 #input('enter source taxon id:')
    target_taxon_id = 367558 #input('enter target taxon id:')

    sp.mergeTaxa(source_taxon_id, target_taxon_id, token)

print('exiting...')