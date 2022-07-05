from queue import Empty
import pytest
import sys, random, json
from getpass import getpass
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import specify_interface as s

# global variables 
filepath = str(Path(__file__).parent.parent.joinpath('bootstrap').joinpath('institutions.json'))
print(' -> %s' % filepath)
institutions = json.load(open(filepath))
baseURL = institutions[0]['URL']
loginURL = baseURL + 'context/login/'
collections = {}

def test_specify_interface():
  print('*** Specify Interface test run ***')

  # Connect to Specify7 API
  s.initInstitution(baseURL)

  # First step is to get a CSRF token 
  csrftoken = s.getCSRFToken()
  assert csrftoken != ''

  # Ask for username and password from user
  print(' - get username/password from input')
  username = input('Enter username: ')
  passwd = getpass('Enter password: ')

  # Next step is to use csrf token to log in 
  csrftoken = s.login(username, passwd, csrftoken)
  assert csrftoken != ''

  #verify session to check all is OK 
  sessionVerified = s.verifySession(csrftoken)
  assert sessionVerified == True

  if sessionVerified:
    # query some random collection object
    offset = random.randint(0,500000) 
    collectionObjects = s.fetchSpecifyObjects('collectionobject', csrftoken, 10, offset)
    print(' - fetched %s objects' % str(len(collectionObjects)))
    randomCollObjectNr = random.randint(0,9)
    collectionObjectId = collectionObjects[randomCollObjectNr]['id'] #501269 
    collobj = s.fetchCollObject(collectionObjectId, csrftoken)
    assert collobj is not None 
    assert collobj is not Empty
    print(' - Successully retrieved collection object - %s:"%s"' %(collobj['id'], collobj['catalognumber']))

  #log out
  s.logout(csrftoken)

test_specify_interface()



