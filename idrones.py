from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from mongo import MongoInterface
from functools import wraps
import urllib, urllib2, json
    
app = Flask(__name__)

BROWSER_ID_URL = "https://browserid.org/verify"
LOCAL_SERVER = "http://localhost:5000"

@app.before_request
def before_request():
    g.db = MongoInterface()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route("/")
def show_entries():
    email = session.get('email', None)
    last_login = g.db.get_login_time(email)
    return render_template('index.html', id=email, last_login=last_login)

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = urllib.urlencode({'assertion': request.form['assertion'],
                             'audience': LOCAL_SERVER})
    result = json.loads(urllib2.urlopen(BROWSER_ID_URL, data).readline())
    #app.logger.debug(str(result))
    if result['status'] == 'okay' and result['audience'] == LOCAL_SERVER:
        session['email'] = result['email']
        g.db.set_login_time(session['email'])
        flash('You were logged in')
    return redirect(url_for('show_entries'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwds):
        if session.get('email', None) == None:
            return redirect(url_for('show_entries'))
        return f(*args, **kwds)
    return decorated_function

@app.route('/discoveries')
@login_required
def discoveries():
    email = session.get('email', None)
    ds = g.db.get_discoveries(email)
    return render_template('discoveries.html', id=email, discoveries=ds)

@app.route('/events')
@login_required
def events():
    email = session.get('email', None)
    evs = g.db.get_events(email)
    return render_template('events.html', id=email, events=evs)

@app.route('/resources')
@login_required
def resources():
    email = session.get('email', None)
    rcs = g.db.get_resources(email)
    return render_template('resources.html', id=email, resources=rcs)

if __name__ == '__main__':
    app.config.from_pyfile('idrones_webapp.cfg')
    app.run()
