import os, web
from jinja2 import Environment, FileSystemLoader
from passlib.hash import pbkdf2_sha256

import getpass
path = '/home/'+getpass.getuser()+'/.secrets'
import sys; sys.path.insert(0, path)
import psqlauth

web.config.debug = False

def render_template(template_name, **context):
    extensions = context.pop('extensions', [])
    globals = context.pop('globals', {})

    jinja_env = Environment(autoescape=True,
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__),
                                             'templates')),
                                extensions=extensions)
    jinja_env.globals.update(globals)

    web.header('Content-Type','text/html; charset=utf-8', unique=True)
    web.header('Cache-Control',
               'no-cache, max-age=0, must-revalidate, no-store',
               unique=True
    )

    return jinja_env.get_template(template_name).render(context)

urls = (
    '/', 'index',
    '/login', 'login',
    '/home', 'home',
    '/logout', 'logout'
)

db = web.database(dbn='postgres', user=psqlauth.user, pw=psqlauth.pw,
                  db=psqlauth.db)

app = web.application(urls, globals())

session = web.session.Session(app,
          web.session.DiskStore('/var/lib/php/session'),
              initializer={'loggedIn': False, 'email' : ''}
          )

class index:
    def GET(self):
        if session.loggedIn:
            raise web.seeother('/home')
        else:
            raise web.seeother('/login')

class login:
    def GET(self):
        if session.loggedIn:
            raise web.seeother('/home')
        else:
            return render_template('login.html')

    def POST(self):
        email, passwd = web.input().email, web.input().passwd
        try:
            query = 'SELECT * FROM "USER" WHERE email=$em;'
            vars = {'em':email}
            result = db.query(query, vars)[0]
            if pbkdf2_sha256.verify(passwd, result['passwd']):
                session.loggedIn = True
                session.email = email
                #raise web.seeother('/home')
                #posts = list(db.query('SELECT * FROM "POST" WHERE us_id=1 ORDER BY pt_time asc'))
                #return render_template('home.html', email=session.email, posts=posts)
        except:
            pass
        raise web.seeother('/')

class home:
    def GET(self):
        if session.loggedIn:
            userID = db.query('SELECT us_id FROM "USER" WHERE email=\''+session.email+'\';')
            posts = list(db.query('SELECT * FROM "POST" WHERE us_id='+str(userID[0].us_id)+' ORDER BY pt_time asc'))
            return render_template('home.html', email=session.email, posts=posts)
        else:
            raise web.seeother('/login')

class logout:
    def POST(self):
        session.loggedIn=False
        session.email=None
        return render_template('login.html')

if __name__ == "__main__":
    app.run()
else:
    application = app.wsgifunc()
