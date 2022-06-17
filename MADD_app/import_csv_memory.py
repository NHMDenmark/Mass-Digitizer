# -*- coding: utf-8 -*-
"""
  Created on Tuesday June 14, 10:21, 2022
  @author: Jan K. Legind, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  Plants of the World Online taxonomy https://hosted-datasets.gbif.org/datasets/wcvp.zip is used in this exploration.

  PURPOSE: To make a large (1M+) table available in SQLite in :memory: in order to gain speed. Initial result takes < 40 miliseconds - rom there
  all operations should go into native fast data structures such as dictionaries. On subsequent keystrokes the list of candidates will shrink as accuracy increases."""

import csv, sqlite3
import time
import taxonomy_shrinker

con = sqlite3.connect(":memory:")
# sets the DB to be in memory exclusively
cur = con.cursor()
####This part is necessary due to the nature of in-memory SQLite, since the DB disappears at session end.####

def make_taxonomylite(hc):
    cur.execute('CREATE TABLE pow ("taxon_name","family","authors","status");') # use your column names here

    with open('C:/Users/bxq762/Desktop/MADD_APP/powo_uniq.csv', 'r', encoding='utf-8') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['taxon_name'], i['family'], i['authors'], i['status']) for i in dr]

    start = time.time()
    cur.executemany("INSERT INTO pow (taxon_name,family,authors,status) VALUES (?, ?, ?, ?);", to_db)
    con.commit()
    end = time.time()
    print('exe time for SQLite "botany" taxonomy build is= ', end - start)
####This needs only run once at the start of session####

make_taxonomylite('hard coder')

def run_query(name_part):
    #name_part: string to be queried by
    #return: a dict of names

    # input_field = 'Cor'
    input_field = name_part
    query = "SELECT pow.taxon_name from pow WHERE pow.taxon_name LIKE '{}%';".format(input_field)

    out = cur.execute(query)


    taxon_dict = {}
    for j in out:
        # print(j[0])
        taxon_dict[j[0]] = ''

    return taxon_dict
# FOR DEMO PURPOSE
# res = run_query('Cor')
# print('length - - ', len(res))
# res2 = taxonomy_shrinker.refine_taxon_dict(res, 'Cora')
# print('length of new taxonomy - - ', len(res2))
####END FOR DEMO



