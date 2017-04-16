""" Basic todo list using webpy 0.3 """
import web
import json
import os
from tenant_repo_manager import CheckRepo, CreateRepo, getUsers, getUserIndex, createUser, returnOwl, returnSparql
from QueryProcesser import myQuery
from cache import loadCache, saveCache, getresult, update

### Url mappings
urls = (
    '/', 'Index',
    '/pf', 'platform',
    '/login', 'Login',
    '/logout', 'Logout',
    '/del/(\d+)', 'Delete',
)
render = web.template.render('templates', base='base')
app = web.application(urls, locals())
session = web.session.Session(app, web.session.DiskStore('sessions'))

# urls = ('/', 'cpuload')
# render = web.template.render('templates/')
# app = web.application(urls, globals())

allowed = (
    ['user','pass'],
    ['saumil','shah'],
)
usernamex = 'SS'
vpath = 'static/Cloud/'

onto_form = web.form.Form(
    web.form.Textbox('username', web.form.notnull),
    web.form.Password('password', web.form.notnull),
    web.form.Button('Login'),
    web.form.Dropdown('french', ['mustard', 'fries', 'wine']),
    )

class Login():

    login_form = web.form.Form(
        web.form.Textbox('username', web.form.notnull),
        web.form.Password('password', web.form.notnull),
        web.form.Button('Login'),
        )

    def GET(self):
        f = self.login_form()
        return render.login(f)

    def POST(self):
        allowed = getUsers()
        print '\n All Users', allowed

        if not self.login_form.validates():
            print '\n\n{{{{{{{{{{{}}}}}}}}}}'
            print '\n\nGuess, I was here...!'
            # return render.login(self.login_form)
            # return render.platform(my_form(), username, ["Car", "Bike", 'Movie'])
            # platform.GET(platform);
            x='SS'
            raise web.redirect('/pf?user=%s' % x)
            # raise web.seeother('/pf/%s' % x)

        username = self.login_form['username'].value
        password = self.login_form['password'].value

        # if [username,password] in allowed:
        #     session.logged_in = True
        #     usernamex = username
        #     print '\n##################'
        #     print "Ux assigned"
        #     print '##################\n'
        #
        #
        #     vxpath = 'Cloud/U' + str(allowed.index([username,password]))
        #     raise web.redirect('/pf?user=%s:%s' % (username, vxpath))
        #     # raise web.seeother('/pf', usernamex)
        #
        # else:
        #     print 'User Not Found!\n'
        #     raise web.seeother('/')

        if [username,password] in allowed:
            uid = str(allowed.index([username,password]) + 1)
            files = []

            session.logged_in = True
            usernamex = username
            print '##################'
            print "Ux assigned"
            print '##################\n'

            if CheckRepo(uid):
                print '\nUser Repo exists...for UID :'+uid+'\tUsername :',username
                # files = os.listdir(vpath+uid)
                root, dirs, files = os.walk(vpath+uid).next()
                print '\n\nPath ---',root
                print '\nDirs ---',dirs
                print '\nFiles ---',files

                for dirx in dirs:
                    rootd, dirsd, filesd = os.walk(vpath+uid+'/'+dirx).next()
                    print '\n\n\tPathd x--',rootd
                    print '\n\tDirsd x--',dirsd
                    print '\n\tFilesd x--',filesd

                    files = files + ['*UPS*']+ filesd

            else:
                print '\n\nUser Repo does not exist!!! \tCreating User Repository...'
                print 'User Repo created...for UID :'+uid+'\tUsername :'+username+'\tLocated at : '+vpath+uid
                CreateRepo(uid)

            vxpath = 'static/Cloud/U' + uid
            filex = '^'.join(files)
            print "\nvxpath : "+vxpath
            raise web.redirect('/pf?user=%s:%s:%s' % (username, vxpath, filex))

        else:
            print '\n\nUser NOT Found!'
            createUser(allowed, username,password);
            raise web.seeother('/')

        return render.login(self.login_form)

class platform:

    my_form = web.form.Form(
        web.form.Dropdown('Select an Ontology : ', args=['a','b','c'], _class='xtables', id='xtables'),
        web.form.Textarea(name='Input Query : ',value='Write your text in Textarea', class_='qfield', id='qfield', cols="50", rows="5",style="background-color:#FCF5D8;color:dimgrey;font-family:Courier"),
        )

    def GET(self):
        print 'In platform Class GET'
        params  = web.input()
        userx = params['user'].split(':')[0]
        vpath = params['user'].split(':')[1]

        print "\n@@@@@@@@ Raincheck : ",params['user'].split(':')[2]
        [optionxx1, optionxx2] = params['user'].split(':')[2].split('*UPS*')

        optionx1 = optionxx1.split('^')
        optionx2 = optionxx2.split('^')

        useridx = vpath.split('static/Cloud/U')
        print useridx
        print "\noptionx1 : ",optionx1
        print "\noptionx2 : ",optionx2

        options1 = returnOwl(optionx1)
        options_srq1 = returnSparql(optionx1)

        options2 = returnOwl(optionx2)
        options_srq2 = returnSparql(optionx2)

        # options = ['file1.owl', 'file2.owl', 'file3.owl']
        print '\nPRM : ',params, type(params)
        print 'USR : ',userx
        print 'UID : ',useridx
        print 'VPT : ',vpath

        print '\nOpt1 : ',options1
        print 'Opt-Srq1 : ',options_srq1

        print '\nOpt2 : ',options2
        print 'Opt-Srq2 : ',options_srq2


        my_form = web.form.Form(
            # web.form.Dropdown('Select an Ontology : ', args=options, _class='xtables', id='xtables'),
            web.form.GroupedDropdown('Select an Ontology : ',_class='xtables', id='xtables',
            args=(('Default Ontologies',(options1)),('Upload Ontologies',(options2)))),

            web.form.Textarea(name='Input Query : ',value="""SELECT * WHERE {
                    ?s ?p ?o
                    }
                    limit 10""", class_='qfield', id='qfield', cols="50", rows="5",style="background-color:#FCF5D8;color:dimgrey;font-family:Courier"),
                                # web.form.Dropdown('Select an Ontology : ', args=options1, _class='xtables', id='xtables1'),

                                web.form.GroupedDropdown('Select an Ontology : ', _class='xtables', id='xtables1',
                                args=(('Default Ontologies',(options1)),('Upload Ontologies',(options2)))),

                                # web.form.Dropdown('Select a Sparql File : ', args=options_srq1, _class='ytables', id='ytables'),
                                web.form.GroupedDropdown('Select a Sparql File : ', _class='ytables', id='ytables',
                                args=(('Default Queries',(options_srq1)),('Upload Queries',(options_srq2)))),

                                web.form.Textarea(name='Input Query : ',value="""SELECT * WHERE {
                    ?s ?p ?o
                    }
                    limit 5""", class_='qfield', id='qfield1', cols="50", rows="5",style="background-color:#FCF5D8;color:dimgrey;font-family:Courier"),
            # web.form.File('Choose an Ontology : ', args=options, _class='upload', id='upload'),
            # web.form.File(name='myfile'),
            )

        print 'My Form : ',my_form

        return render.platform(my_form(), userx)


    def POST(self):
        print '\nSomeone submitted a Query...'
        form = self.my_form()
        form.validates()
        print 'Form : ',form

        try:
            sz = form.value['data_tx']
            x = str(sz)
            print 'X : ',x
            # s = web.input(xtables = [])
            # dval = str(s.xtables)

            typeX = x.split('^')[0]

            if typeX == '0':
                print 'Type : ',typeX,' Saving'
                username = x.split('^')[1].split('|')[0][0:-2]
                [dval, q] = x.split('^')[1].split('|')[1].split('~')

                uid = str(getUserIndex(username))

                print "Loading Cache..."
                cache = loadCache(vpath+uid+'/cache.pickle')
                print "Saving Cache..."
                saveCache(cache,vpath+uid+'/cache.pickle')
                print "Cache Saved!"
                return json.dumps("Data Saved, "+username+"!")

            elif typeX == '1':
                print 'Type : ',typeX,' Query'
                username = x.split('^')[1].split('|')[0][0:-2]
                [dval, q] = x.split('^')[1].split('|')[1].split('~')

                print 'Username : ', username
                print 'Dropdown : ', dval
                print 'UserQuery : ', q

                onto_file = vpath+str(getUserIndex(username))+'/'+dval
                print 'onto_file_path : ',onto_file

                uid = str(getUserIndex(username))
                cache = loadCache(vpath+uid+'/cache.pickle')
                saveCache(cache,vpath+uid+'/cache.pickle')

                answer = getresult(cache,onto_file+q)

                if answer == None:
                    print "\n******Answer None!!!"
                    js = myQuery(q, onto_file)
                else:
                    print "\n******Answer NOTNone!!!"
                    js = answer
                print '\nAnswer : ',js

                cacheU = update(cache, onto_file+q, js)
                saveCache(cacheU, vpath+uid+'/cache.pickle')
                return json.dumps("Selected File : "+dval+"\nAnswer to Query : "+js)

            # elif typeX == '2':
            #     print 'Type : ',typeX,' Upload'
            #     username = x.split('^')[1].split('|')[0][0:-2]
            #
            #
            #     x = web.input(myfile={})
            #     print "\n\n^^^^^^^^^^^^^X : ",x
            #     filedir = '/Users/hellosaumil/Desktop/UF'                 # change this to the directory you want to store the file in.
            #     if 'myfile' in x:                                         # to check if the file-object is created
            #
            #         web.debug(x['myfile'].filename) # This is the filename
            #         web.debug(x['myfile'].value) # This is the file contents
            #
            #         filepath=x.myfile.filename.replace('\\','/')          # replaces the windows-style slashes with linux ones.
            #         print "\nFilename1 : ",filepath
            #
            #         filename=filepath.split('/')[-1]                      # splits the and chooses the last part (the filename with extension)
            #         print "\nFilename2 : ",filename
            #         fout = open(filedir +'/'+ filename,'w+')               # creates the file where the uploaded file should be stored
            #         fout.write(x.myfile.file.read())                      # writes the uploaded file to the newly created file.
            #         fout.close()                                          # closes the file, upload complete.
            #
            #     return json.dumps("File(s) Uploaded Successfully, "+username+"!")
            else:
                return json.dumps("Invalid Request, "+username+"!")

        except Exception as e:
            print "******** Exception : ", e

            typeX = '2'
            print 'Type : ',typeX,' Upload'
            # username = x.split('^')[1].split('|')[0][0:-2]


            x = web.input(myfile={})
            print "\n\n^^^^^^^^^^^^^X : ",x
            # filedir = '/Users/hellosaumil/Desktop/UF'                 # change this to the directory you want to store the file in.
            if 'myfile' in x:                                         # to check if the file-object is created


                print "File Contents : ", x['myfile'].value # This is the file contents
                # uid = x['user'].split(':')[1].split('/')[1][1:]
                uid = x['user'].split(':')[1].split('/')[2][1:]
                username = x['user'].split(':')[0].title()

                print "UID : "+uid+" - Username : "+username
                filedir = vpath+uid+"/uploads"
                print "\nFile-Dir : ",filedir

                filepath=x.myfile.filename.replace('\\','/')          # replaces the windows-style slashes with linux ones.
                print "\nFile-Path : ",filepath

                filename=filepath.split('/')[-1]                      # splits the and chooses the last part (the filename with extension)
                print "File-Name : ",filename
                fout = open(filedir +'/'+ filename,'w+')               # creates the file where the uploaded file should be stored
                fout.write(x.myfile.file.read())                      # writes the uploaded file to the newly created file.
                fout.close()                                          # closes the file, upload complete.

                print "File Uploaded Successfully at "+vpath+uid+", "+username+"!"

                root, dirs, files = os.walk(vpath+uid).next()
                print '\n\nPath $---',root
                print '\nDirs $---',dirs
                print '\nFiles $---',files

                for dirx in dirs:
                    rootd, dirsd, filesd = os.walk(vpath+uid+'/'+dirx).next()
                    print '\n\n\tPathd $x--',rootd
                    print '\n\tDirsd $x--',dirsd
                    print '\n\tFilesd $x--',filesd

                    files = files + ['*UPS*']+ filesd

                vxpath = 'static/Cloud/U' + uid
                filex = '^'.join(files)

                raise web.redirect('/pf?user=%s:%s:%s' % (username, vxpath, filex))
            # return json.dumps("File(s) Uploaded Successfully, "+username+"!")

class Index:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, description="I need to:"),
        web.form.Button('Add todo'),
    )

    def GET(self):
        if session.get('logged_in', False):
            """ Show page """
            todos = model.get_todos()
            form = self.form()
            return render.index(todos, form)
        else:
            raise web.seeother('/login')


    def POST(self):
        """ Add new entry """
        form = self.form()
        form.validates()

        if not form.validates():
            print '\n\n[[[[[[[[[[[[]]]]]]]]]]]]'

            print '\nSomething\'s Up!'
            todos = model.get_todos()
            return render.index(todos, form)

        model.new_todo(form.d.title)
        raise web.seeother('/')

class Logout:
    def GET(self):
        print "\n========================"
        print "Logging User out...   "
        session.logged_in = False
        raise web.seeother('/login')

class Delete:

    def POST(self, id):
        """ Delete based on ID """
        id = int(id)
        model.del_todo(id)
        raise web.seeother('/')

app = web.application(urls, globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
    web.config._session = session
else:
    session = web.config._session

if __name__ == '__main__':
    app.run()
