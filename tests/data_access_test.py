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
  
  # First switch to test database 
  db.setDatabase('test')

  # Try to get collections 
  collections = db.getRows('collection')
  assert len(collections) > 0
  
  # Try to get some taxa
  taxonNames = db.getRows('taxonname')
  assert len(taxonNames) == 100

  # Check random taxon id field and attempt fetch on Id and compare
  r = random.randint(0,99)
  taxonNameId = taxonNames[r]['id']
  taxonSpId = taxonNames[r]['taxonid']
  taxonName = taxonNames[r]['name']
  print('Picked random taxon: -> %s(%s):"%s"' %(str(taxonNameId),str(taxonSpId),taxonName))
  randomTaxon = db.getRowOnId('taxonname', taxonNameId)
  print('Comparing "%s" with "%s"' %(taxonName, randomTaxon['name'] ))
  assert taxonName == randomTaxon['name'] 

  # Attempt taxonName fetch on filters
  filteredTaxonNames = db.getRowsOnFilters('taxonname', {'name':'="%s"' % taxonName}) 
  print('Fetching taxa on name: "%s" results in %s row(s)' %(taxonName, len(filteredTaxonNames) ))
  assert len(filteredTaxonNames) >= 1

  #TODO test insert row 


test_data_access()



