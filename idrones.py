from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import urllib, urllib2, json
    
app = Flask(__name__)

BROWSER_ID_URL = "https://browserid.org/verify"
LOCAL_SERVER = "http://localhost:5000"

@app.route("/")
def show_entries():
    email = session.get('email', None)
    return render_template('index.html', id=email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = urllib.urlencode({'assertion': request.form['assertion'],
                             'audience': LOCAL_SERVER})
    result = json.loads(urllib2.urlopen(BROWSER_ID_URL, data).readline())
    #app.logger.debug(str(result))
    if result['status'] == 'okay' and result['audience'] == LOCAL_SERVER:
        session['email'] = result['email']
        flash('You were logged in')
    return redirect(url_for('show_entries'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.config.from_pyfile('idrones_webapp.cfg')
    app.run()
