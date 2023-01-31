# -*- coding: utf-8 -*-
"""
Created on Thu May 26 17:44:00 2022

@authors: Jan K. Legind, NHMD; Fedor A. Steeman NHMD

Copyright 2022 Natural History Museum of Denmark (NHMD)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""


#Central place to manage version numbers
versionNumber = "0.2.9"
# Before compiling exe, please set the version number above


def getVersionNumber():
    return versionNumber


# """This code can be modified to replace the version number in the
# DaSSCo.issfile which has this format:/ #define MyAppVersion "0.2.5" /
# (Please ignore the forward slashes above)"""