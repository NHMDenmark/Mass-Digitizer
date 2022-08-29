# TODO description

# Specify 
baseURL = ''

# database 
db_in_memory = False

# session 
institutionId = 0
institutionName = '-not set-'
collectionId = 0
collectionName = '-not set-'
spUserName = '-not set-'
spUserId = -1
csrfToken = ''

def clearSession():
    institutionId = 0
    institutionName = '-not set-'
    collectionId = 0
    collectionName = '-not set-'
    spUserName = '-not set-'
    csrfToken = ''
