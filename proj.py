
import os, web
from jinja2 import Environment, FileSystemLoader
from passlib.hash import pbkdf2_sha256
from datetime import date, datetime, timedelta

import socket, getpass
if socket.gethostname()=='arch4alyx' or socket.gethostname()=='Vera':
    path = '/home/alyx/.secrets'
    homedir = '/home/alyx/'
elif getpass.getuser()=='alyx':
    path = '/Users/alyx/.secrets'
    homedir = '/Users/alyx/'
elif socket.gethostname()=='phoenix.goucher.edu':
    path = '/home/sqlfreakz/.secrets'
    homedir = '/home/sqlfreakz/'
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
    '/ursvp/(\d*)', 'ursvp',
    '/follow/(\d*)', 'follow',
    '/ufollow/(\d*)', 'ufollow',
    '/images/(.*)', 'images',
    '/newuser', 'newuser',
    '/search', 'search',
    '/newevent', 'newevent'
)

db = web.database(dbn='postgres', user=psqlauth.user, pw=psqlauth.pw,
                  db=psqlauth.db)

app = web.application(urls, globals())

weekdays = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}
months = {
    1:  "Jan",
    2:  "Feb",
    3:  "Mar",
    4:  "Apr",
    5:  "May",
    6:  "Jun",
    7:  "Jul",
    8:  "Aug",
    9:  "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


# the outer if else block is a fix for sessions not working in debug mode
# source: http://webpy.org/cookbook/session_with_reloader
# the inner if determines the path of the sessions directory,
# depending on the server (/var/lib for phoenix)
if web.config.get('_session') is None:
    if socket.gethostname()=='phoenix.goucher.edu':
        seshdir = '/var/lib/php/session'
    else:
        seshdir = homedir+'public_html/wsgi/sessions'

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


class newuser:
    def GET(self):
        if session.loggedIn:
            raise web.seeother('/home')
        else:
            return render_template('newuser.html')

    def POST(self):
        fname, lname, email, passwd, dob = web.input().fname, web.input().lname, \
                web.input().email, web.input().passwd, web.input().dob
        try:
            born = datetime.strptime(dob, '%Y-%m-%d')
            today = date.today()
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            query = ('INSERT INTO "USER" '
                     '(first_name, last_name, email, passwd, dob, age) '
                     'VALUES ($fn, $ln, $em, $pw, $bd, $ag) '
                     'RETURNING us_id;')
            vars = {'fn':fname, 'ln':lname, 'em':email,
                    'pw':pbkdf2_sha256.hash(passwd), 'bd':dob, 'ag':age}
            db.query(query, vars)
            query = 'SELECT * FROM "USER" WHERE email=$email;'
            vars = {'email':email}
            user = db.query(query, vars)[0]
            session.loggedIn = True
            session.email = email
            session.user = user
        except:
            pass
        raise web.seeother('/newuser')


class home:
    def GET(self):
        if session.loggedIn:
            query = ('SELECT * FROM "POST" '
                     'WHERE us_id IN (SELECT us_id FROM "USER" WHERE email=$em) '
                     'OR us_id IN (SELECT flwe_id FROM "FOLLOW" WHERE flwr_id = '
                     '(SELECT us_id FROM "USER" WHERE email=$em))'
                     'ORDER BY pt_time desc;')
            vars = {'em':session.email}
            posts = list(db.query(query, vars))
            query = ('SELECT us_id, pic_name '
                     'FROM (SELECT us_id, pic_name '
                     'FROM "PICS" INNER JOIN '
                     '("POST" NATURAL JOIN "USER") '
                     'ON prof_pic = pic_id) AS "ALL" '
                     'INNER JOIN '
                     '(SELECT flwe_id FROM "FOLLOW" '
                     'WHERE flwr_id = $uid OR flwe_id = $uid) '
                     'AS "FLWES" ON "ALL".us_id = "FLWES".flwe_id;')
            vars = {'uid':session.user['us_id']}
            picQ = list(db.query(query, vars))
            pics = dict()
            for pic in picQ:
                pics[pic['us_id']] = pic['pic_name']
            return render_template('home.html', posts=posts, pics=pics, user=session.user,
                    weekdays=weekdays, today=datetime.today(), months=months, yest=timedelta(1))
        else:
            raise web.seeother('/login')

    def POST(self):
        post_text = web.input().ptxt
        try:
            flnm = session.user['first_name'] + ' ' + session.user['last_name']
            query = ('INSERT INTO "POST" '
                     '(us_id, pt_fullname, pt_txt) '
                     'VALUES ($uid, $name, $txt);')
            vars = {'uid':session.user['us_id'], 'name':flnm, 'txt':post_text}
            db.query(query, vars)
        except:
            pass
        raise web.seeother('/home')


class newevent:
    def GET(self):
        if session.loggedIn:
            return render_template('newevent.html')
        else:
            raise web.seeother('/')

    def POST(self):
        name, desc, date, time, street, city, state, zip = web.input().name, web.input().desc, web.input().date, \
                web.input().time, web.input().street, web.input().city, web.input().state, web.input().zip
        try:
            query = ('INSERT INTO "EVENT" '
                     '(ev_name, ev_desc, ev_time, ev_street, ev_city, ev_state, ev_zip) '
                     'VALUES ($nm, $ds, $tm, $sr, $ct, $st, $zp) RETURNING ev_id;')
            vars = {'nm':name, 'ds':desc, 'tm':'2020-04-20 16:20:00', 'sr':street, 'ct':city, 'st':state, 'zp':zip}
            eid = str(db.query(query, vars)[0]['ev_id'])
        except:
            pass
        raise web.seeother('/event/'+eid)


class search:
    def GET(self):
        if session.loggedIn:
            i = web.input(srch=None)
            query = ('SELECT us_id, first_name, last_name from "USER" '
                     'WHERE UPPER(first_name) LIKE UPPER($str) OR '
                     'UPPER(last_name) LIKE UPPER($str);')
            vars = {'str':'%'+web.input().srch+'%'}
            users = db.query(query, vars)
            query = ('SELECT ev_id, ev_name from "EVENT" '
                     'WHERE UPPER(ev_name) LIKE UPPER($str);')
            events = db.query(query, vars)
            return render_template('search.html', users=users, events=events)
        else:
            raise web.seeother('/login')


class profile:
    def GET(self, uid):
        if session.loggedIn:
            query = 'SELECT * FROM "USER" WHERE us_id=$uid;'
            vars = {'uid':uid, 'mid':session.user['us_id']}
            prof = db.query(query, vars)[0]
            query = ('SELECT * FROM "EVENT" '
                     'WHERE ev_id IN (SELECT ev_id FROM "RSVP" WHERE us_id=$uid) '
                     'ORDER BY ev_time asc;')
            events = list(db.query(query, vars))
            query = ('SELECT * FROM "USER" '
                     'WHERE us_id IN (SELECT flwe_id FROM "FOLLOW" WHERE flwr_id=$uid) '
                     'ORDER BY first_name asc;')
            following = list(db.query(query, vars))
            query = ('SELECT CASE WHEN EXISTS '
                     '(SELECT flwe_id FROM "FOLLOW" WHERE flwr_id=$mid'
                     ' AND flwe_id=$uid) '
                     'THEN CAST(1 AS BIT) '
                     'ELSE CAST(0 AS BIT) END;')
            isFollowed = bool(int(db.query(query, vars)[0]['case']))
            isMe = (int(uid) == session.user['us_id'])
            query = ('SELECT pic_name FROM "PICS" '
                     'WHERE pic_id=$pid;')
            vars = {'pid':prof['prof_pic']}
            pic = db.query(query, vars)[0]['pic_name']
            return render_template('profile.html', prof=prof, events=events, pic=pic,
                        uid=uid, following=following, isFollowed=isFollowed, isMe=isMe)
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
            query = 'SELECT * FROM "EVENT" WHERE ev_id=$eid'
            event = db.query(query, vars)[0]
            return render_template('event.html', attending=attending, eid=eid, going=going, event=event)
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


class follow:
    def POST(self, uid):
        query = ('INSERT INTO "FOLLOW"(flwr_id, flwe_id)'
                 'VALUES ($frid, $feid);')
        vars = {'frid':session.user['us_id'], 'feid':uid}
        db.query(query, vars)
        raise web.seeother('/profile/'+uid)


class ufollow:
    def POST(self, uid):
        query = ('DELETE FROM "FOLLOW" '
                 'WHERE flwr_id=$frid AND flwe_id=$feid;')
        vars = {'frid':session.user['us_id'], 'feid':uid}
        db.query(query, vars)
        raise web.seeother('/profile/'+uid)


class images:
    def GET(self, img):
        ext = img.split(".")[-1]
        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "jpeg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"
        }
        if img in os.listdir(homedir+'public_html/wsgi/images'):
            web.header("Content-Type","attachment; Content-Type", cType[ext])
            return open('images/%s'%img, "rb").read()
        else:
            raise web.notfound()


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
