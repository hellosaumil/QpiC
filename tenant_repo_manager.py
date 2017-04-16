import os, csv, shutil
vpath = './static/Cloud/'
def CheckRepo(u_id):
    return os.path.isdir(vpath+u_id)

def CreateRepo(u_id):
    os.makedirs(vpath+u_id)
    os.makedirs(vpath+u_id+"/uploads")
    path = vpath+'Default/'
    files = os.listdir(path)
    for file_name in files:
        shutil.copy(path+file_name, vpath+u_id+'/'+file_name)

def getUsers():
    allowed = []
    with open(vpath+'users.txt', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            allowed.append([row[0],row[1]])
    return allowed

def getUserIndex(username):
    allowed = getUsers()
    for i in range(len(allowed)):
        if(allowed[i][0]==username):
            return i+1

def createUser(allowed, username, password):
    allowed.append([username,password])

    f = open(vpath+'users.txt','a')
    f.write(username+','+password+'\n')
    f.close()
    uid = str(allowed.index([username,password])+1)
    print "New User : ", uid
    CreateRepo(uid)

def returnOwl(alist):
    return [x for x in alist if '.owl' in x.lower()]

def returnSparql(alist):
    return [x for x in alist if '.rq' in x.lower()]

# alist = ['mayank.owl','saumil.owl','_DS','ma']
# print returnOwl(alist)
#
# allowed = [['user1','pass1'],['user2','pass2'],['user3','pass3'],['user4','pass4']]
username = 'saumil'
password = 'shah'

allowed = getUsers()
print '\n All Users', allowed

if [username,password] in allowed:
    uid = str(allowed.index([username,password]) + 1)

    if CheckRepo(uid):
        print '\nUser Repo exists...for UID :'+uid+'\tUsername :',username
        files = os.listdir(vpath+uid)
        print '\nFiles ---', '\n',files

    # return files
    else:
        print '\n\nUser Repo does not exist!!! \tCreating User Repository...'
        print 'User Repo created...for UID :'+uid+'\tUsername :'+username+'\tLocated at : '+vpath+uid
        CreateRepo(uid)

else:
    print '\n\nUser NOT Found!'
    createUser(allowed, username,password);
