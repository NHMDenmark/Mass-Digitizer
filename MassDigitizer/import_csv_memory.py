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

  PURPOSE: To make a large (1M+) table available in SQLite in :memory: in order to gain speed. Initial result takes < 40 miliseconds - from there
  all operations should go into native fast data structures such as dictionaries. On subsequent keystrokes the list of candidates will shrink as accuracy increases."""

import csv, sqlite3
import time
import taxonomy_shrinker

con = sqlite3.connect(":memory:")
# sets the DB to be in memory exclusively
cur = con.cursor()
####This part is necessary due to the nature of in-memory SQLite, since the DB disappears at session end.####

def make_taxonomylite(hc):
    # cur.execute('CREATE TABLE pow ("taxon_name","family","authors","status");') # use your column names here
    cur.execute('CREATE TABLE IF NOT EXISTS botany ("taxon_full_name", "author");')

    with open(r'C:\Users\bxq762\Documents\exports\plant_taxonomy\botany_fullname_author.csv', 'r', encoding='utf-8-sig') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        to_table = csv.reader(fin, delimiter=';') # comma is default delimiter
        # for i in dr:
        #     print(i)
        # dr = dict(dr)
        # two = {k: dr[k] for k, _ in zip(dr, range(2))}
        # print('first 2 : ', two)
        insert_records = "INSERT INTO botany (taxon_full_name, author) values (?, ?)"
        # for j in dr:
        #     print(j)
        #     break
        # to_db = [(i['taxon_name'], i['family'], i['authors'], i['status']) for i in dr]
        # to_db = [(i['taxontreedefid'], i['rank_'], i['taxon_full_name'], i['author']) for i in dr]

        # to_db = [(i['taxon_full_name']) for i in dr]

        start = time.time()
        cur.executemany(insert_records, to_table)
        con.commit()
        end = time.time()
        print('exe time for SQLite "botany" taxonomy build is= ', end - start)
        select = "SELECT * FROM botany LIMIT 10;"
        rows = cur.execute(select).fetchall()

        # Output to the console screen
        for r in rows:
            print(r)
####This needs only run once at the start of session####

make_taxonomylite('placeholder')

def run_query(name_part):
    #name_part: string to be queried by
    #return: a dict of names

    input_field = name_part
    query = "SELECT bot.taxon_full_name FROM botany bot WHERE bot.taxon_full_name LIKE '{}%';".format(input_field)

    out = cur.execute(query)


    taxon_dict = {}
    for j in out:
        # print('initial result', j)
        taxon_dict[j[0]] = ''
        # taxon_dict[j[0]] = j[1]
        # first_pair = next(iter((taxon_dict.items())))
        # print('First pair: ', taxon_dict)
        # break

    return taxon_dict
# FOR DEMO PURPOSE
# res = run_query('Cor')
# print('length - - ', len(res))
# res2 = taxonomy_shrinker.refine_taxon_dict(res, 'Cora')
# print('length of new taxonomy - - ', len(res2))
####END FOR DEMO



