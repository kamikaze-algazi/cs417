import os, web
from jinja2 import Environment, FileSystemLoader
from passlib.hash import pbkdf2_sha256

import socket, getpass
if getpass.getuser()=='alyx':
    path = '/Users/alyx/.secrets'
elif socket.gethostname()=='phoenix.goucher.edu':
    path = '/home/sqlfreakz/.secrets'
elif socket.gethostname()=='arch4alyx':
    path = '/home/alyx/.secrets'
import sys; sys.path.insert(0, path)
import psqlauth

#web.config.debug = False

###################### BEGIN HELPER METHODS ######################

# helper method to render a template in the templates/ directory
#
# `template_name': name of template file to render
#
# `**context': a dictionary of variable names mapped to values
# that is passed to Jinja2's templating engine
#
# WARNING: DO NOT CHANGE THIS METHOD
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

##################### END HELPER METHODS #####################

urls = (
    '/', 'index',
    '/login', 'login',
    '/home', 'home',
    '/profile/(\d*)', 'profile',
    '/logout', 'logout',
    '/event/(\d*)', 'event',
    '/rsvp/(\d*)', 'rsvp',
    '/ursvp/(\d*)', 'ursvp'
)

db = web.database(dbn='postgres', user=psqlauth.user, pw=psqlauth.pw,
                  db=psqlauth.db)

app = web.application(urls, globals())

# the outer if else block is a fix for sessions not working in debug mode
# source: http://webpy.org/cookbook/session_with_reloader
# the inner if determines the path of the sessions directory,
# depending on the server (/var/lib for phoenix)
if web.config.get('_session') is None:
    if getpass.getuser()=='alyx':
        seshdir = '/Users/alyx/public_html/wsgi/sessions'
    elif socket.gethostname()=='phoenix.goucher.edu':
        seshdir = '/var/lib/php/session'
    elif socket.gethostname()=='arch4alyx':
        seshdir = '/home/alyx/public_html/wsgi/sessions'

    session = web.session.Session(app,
              web.session.DiskStore(seshdir),
              initializer={'loggedIn': False, 'email' : '', 'user' : None})
    web.config._session = session
else:
    session = web.config._session




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
                session.user = result
        except:
            pass
        raise web.seeother('/')

class home:
    def GET(self):
        if session.loggedIn:
            query = ('SELECT * FROM "POST" '
                     'WHERE us_id IN (SELECT us_id FROM "USER" WHERE email=$em) '
                     'OR us_id IN (SELECT flwe_id FROM "FOLLOW" WHERE flwr_id = '
                     '(SELECT us_id FROM "USER" WHERE email=$em))'
                     'ORDER BY pt_time asc;')
            vars = {'em':session.email}
            posts = list(db.query(query, vars))
            return render_template('home.html', posts=posts, user=session.user)
        else:
            raise web.seeother('/login')

class profile:
    def GET(self, uid):
        if session.loggedIn:
            query = 'SELECT * FROM "USER" WHERE us_id=$uid;'
            vars = {'uid':uid}
            prof = db.query(query, vars)[0]
            query = ('SELECT * FROM "EVENT" '
                     'WHERE ev_id IN (SELECT ev_id FROM "RSVP" WHERE us_id=$uid) '
                     'ORDER BY ev_time asc;')
            events = list(db.query(query, vars))
            return render_template('profile.html', prof=prof, events=events)
        else:
            raise web.seeother('/login')

class event:
    def GET(self, eid):
        if session.loggedIn:
            query = ('SELECT CASE WHEN EXISTS '
                     '(SELECT ev_id FROM "RSVP" WHERE us_id=$uid'
                     ' AND ev_id=$eid) '
                     'THEN CAST(1 AS BIT) '
                     'ELSE CAST(0 AS BIT) END;')
            vars = {'uid':session.user['us_id'], 'eid':eid}
            going = int(db.query(query, vars)[0]['case'])
            query = ('SELECT * FROM "USER" '
                     'WHERE us_id IN (SELECT us_id FROM "RSVP" WHERE ev_id=$eid) '
                     'ORDER BY first_name asc;')
            attending = list(db.query(query, vars))
            return render_template('event.html', attending=attending, eid=eid, going=going)
        else:
            raise web.seeother('/login')

class rsvp:
    def POST(self, eid):
        query = ('INSERT INTO "RSVP"(us_id, ev_id) '
                 'VALUES ($uid, $eid);')
        vars = {'uid':session.user['us_id'], 'eid':eid}
        db.query(query, vars)
        raise web.seeother('/event/'+eid)

class ursvp:
    def POST(self, eid):
        query = ('DELETE FROM "RSVP" '
                 'WHERE us_id=$uid AND ev_id=$eid;')
        vars = {'uid':session.user['us_id'], 'eid':eid}
        db.query(query, vars)
        raise web.seeother('/event/'+eid)

class logout:
    def POST(self):
        session.loggedIn=False
        session.email=None
        session.kill()
        return render_template('login.html')

if __name__ == "__main__":
    app.run()
else:
    application = app.wsgifunc()
