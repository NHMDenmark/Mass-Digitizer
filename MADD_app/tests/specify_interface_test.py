import specify_interface as s
from getpass import getpass

# global variables 
# institutions = json.load(open('bootstrap/institutions.json'))
baseURL = 'https://specify-test.science.ku.dk/' # institutions[0]['URL']
loginURL = baseURL + 'context/login/'
collections = {}

print()
print('**************** Specify Interface test run ****************')
# Connect to Specify7 API
s.initInstitution(baseURL)
# First step is to get a CSRF token 
csrftoken = s.getCSRFToken()
# Ask for username and password from user
print('get username/password from input')
username = input('Enter username: ')
passwd = getpass('Enter password: ')
print('username: "%", password: "%"', username, passwd)
# Next step is to use csrf token to log in 
csrftoken = s.login(username, passwd, csrftoken)
#verify session to check all is OK 
if s.verifySession(csrftoken):
  # query some random collection object 
  s.queryCollObject(501269, csrftoken)
  collobj = s.querySpecifyObject('collectionobject', 501269, csrftoken)
  print(collobj['catalognumber'])

#log out
s.logout(csrftoken)





