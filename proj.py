import os, web
from jinja2 import Environment, FileSystemLoader
from passlib.hash import pbkdf2_sha256

import sys; sys.path.insert(0, '/home/alyx/.secrets')
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
    '/', 'login',
    '/login', 'login',
    '/signup', 'signup',
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
                return render_template('home.html', email=session.email)
        except:
            pass
        raise web.seeother('/')

class home:
    def GET(self):
        return "hello"

class logout:
    def POST(self):
        session.loggenIn=False
        session.email=None
        return render_template('login.html')

if __name__ == "__main__":
    app.run()
else:
    application = app.wsgifunc()
