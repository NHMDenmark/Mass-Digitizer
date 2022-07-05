from cgi import test
from queue import Empty
import pytest
import sys, random, json
from getpass import getpass
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import data_access as db

# global variables 
filepath = str(Path(__file__).parent.parent.joinpath('bootstrap').joinpath('institutions.json'))
institutions = json.load(open(filepath))

def test_data_access():
  print('*** Data Access test run ***')
  assert True
  

  

test_data_access()



