from flask import *

app = Flask(__name__)
app.jinja_env.line_statement_prefix = '%'


separator = ":"

users = {}


def readusers():
    with open("uva/users.txt", "r") as f:
        for line in f:
            a = line.strip().split(separator)
            users[a[0]] = a[1]

readusers()


def incluseuser(name, passw):
    with open("uva/users.txt", "a") as f:
        f.write(name + separator + passw + "\n")


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/a')
def raptor():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] in users:
            if users[request.form['username']] == request.form['password']:
                session['username'] = request.form['username']
                app.logger.info("El usuario %s se ha conectado" % request.form['username'])
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['username'] not in users:
            session['username'] = request.form['username']
            incluseuser(request.form['username'], request.form['password'])
            readusers()
            app.logger.info("El usuario %s se ha registrado" % request.form['username'])
            return redirect(url_for('index'))
        return redirect(url_for('register'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Register>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'