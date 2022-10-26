# -*- coding: utf-8 -*-
"""
  Created on October 14, 2022
  @author: Fedor Alexander Steeman, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

  PURPOSE: Unit testing the data exporter module
"""
import data_exporter
import pytest


def test_exportSpecimens():
    export_file = data_exporter.exportSpecimens('xlsx')
    print('¤¤¤¤¤¤¤'+export_file)
    assert export_file == 'No specimen records to export.'

def test_generteFilename():
    export_path = data_exporter.generateFilename('my_specimens', 'xlsx',
                                                 r"C:\Users\bxq762\Documents\workspace\Mass digitizer\DaSSCo\MassDigitizer\output")
    print('%%%%%%%'+export_path)
    assert export_path

