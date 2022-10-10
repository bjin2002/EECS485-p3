"""Account functions."""
import uuid
import os
import hashlib
import flask
import insta485


@insta485.app.route('/accounts/login/', methods=['GET'])
def show_login():
    """Show login."""
    # if the user is already logged in, send them back to '/'
    if "logname" in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template('login.html')


@insta485.app.route('/accounts/logout/', methods=['GET', 'POST'])
def logout():
    """Log out user."""
    # if the user is already logged in, send them back to 'login'
    if "logname" in flask.session:
        flask.session.clear()
        return flask.redirect(flask.url_for('show_login'))
    return flask.render_template('login.html')


@insta485.app.route('/accounts/create/', methods=['GET'])
def show_create():
    """Show create page."""
    # if the user is already logged in, send them back to '/accounts/edit/'
    if "logname" in flask.session:
        return flask.redirect(flask.url_for('show_edit'))
    return flask.render_template('create.html')


@insta485.app.route('/accounts/delete/', methods=['GET'])
def show_delete():
    """Show delete page."""
    # if the user is not logged in, abort
    if "logname" not in flask.session:
        flask.abort(403)
    context = {"logname": flask.session['logname']}
    return flask.render_template('delete.html', **context)


@insta485.app.route('/accounts/edit/', methods=['GET'])
def show_edit():
    """Show edit page."""
    # if the user is not logged in, abort
    if "logname" not in flask.session:
        flask.abort(403)
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ?",
        (flask.session['logname'], )
    )
    result = cur.fetchone()
    context = {"logname": flask.session['logname'], "user": result}
    return flask.render_template('edit.html', **context)


@insta485.app.route('/accounts/password/', methods=['GET'])
def show_password():
    """Show password page."""
    # if the user is not logged in, abort'
    if "logname" not in flask.session:
        flask.abort(403)
    context = {"logname": flask.session['logname']}
    return flask.render_template('password.html', **context)


@insta485.app.route('/accounts/', methods=['POST'])
def account_target():
    """Account target."""
    target = flask.request.args.get('target')

    if not target:
        target = "/"

    if flask.request.form['operation'] == 'login':
        login()
    if flask.request.form['operation'] == 'create':
        create()
    if flask.request.form['operation'] == 'delete':
        delete()
        return flask.redirect(target)
    if flask.request.form['operation'] == 'edit_account':
        edit()
    if flask.request.form['operation'] == 'update_password':
        newpassword()
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.redirect(target)

# login function


def login():
    """Login jawnt."""
    # empty username and password chedk
    if (flask.request.form['username'] == ''
       or flask.request.form['password'] == ''):
        flask.abort(400)
    connection = insta485.model.get_db()
    # create query
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ?",
        (flask.request.form['username'], )
    )
    # if there is no password associated with the user
    result = cur.fetchone()
    if not result:
        flask.abort(403)
    # uppity is user password
    uppity = result['password']
    # eppity is entered password
    eppity = flask.request.form['password']
    if not password_check(uppity, eppity):
        flask.abort(403)
    flask.session['logname'] = flask.request.form['username']
    return flask.redirect(flask.url_for('show_index'))


# create function


def create():
    """Create jawnt."""
    fullname = flask.request.form['fullname']
    username = flask.request.form['username']
    email = flask.request.form['email']
    password = flask.request.form['password']

    if (fullname == '' or
       username == '' or
       email == '' or
       password == ''):
        flask.abort(400)

    connection = insta485.model.get_db()

    # create query
    cur = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )

    result = cur.fetchall()
    # check for duplicate username
    if result:
        flask.abort(409)

    # uploads picture to db
    file = str(insta485.views.upload.file_upload())

    # salts password
    password = salt_password(password)

    # puts user into db
    connection.execute(
        "INSERT INTO users (username, fullname, email, filename, password) "
        "VALUES (?, ?, ?, ?, ?)",
        (username, fullname, email, file, password))

    # logs user in
    flask.session['logname'] = flask.request.form['username']

# delete function


def delete():
    """Delete jawnt."""
    connection = insta485.model.get_db()
    # query the database for the file name
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ?",
        (flask.session['logname'], )
    )
    result = cur.fetchone()
    file_path = os.path.join(
        insta485.app.config["UPLOAD_FOLDER"], result['filename'])

    print("FILE!!!!!!!!!!!!!!!!!")
    print(file_path)
    # if there is a associated file, remove it
    if os.path.exists(file_path):
        os.remove(file_path)

    # gets all posts that the user created
    post_cur = connection.execute(
        "SELECT filename "
        "FROM posts "
        "WHERE owner = ?",
        (flask.session['logname'], )
    )

    post_results = post_cur.fetchall()

    for post in post_results:
        file_path = os.path.join(
            insta485.app.config["UPLOAD_FOLDER"], post['filename'])

        # if there is a associated file, remove it
        if os.path.exists(file_path):
            os.remove(file_path)

    # removes users from the sql table
    connection.execute(
        "DELETE FROM users "
        "WHERE username = ?",
        (flask.session['logname'], )
    )

    flask.session.clear()

# edit function


def edit():
    """Edit that jawnt."""
    fullname = flask.request.form['fullname']
    email = flask.request.form['email']
    fileobj = flask.request.files["file"]

    # if username or email is empty, error
    if fullname == "" or email == "":
        flask.abort(400)

    connection = insta485.model.get_db()
    # update the password and email
    connection.execute(
        "UPDATE users "
        "SET fullname = ?, email = ? "
        "WHERE username = ?",
        (fullname, email, flask.session['logname'])
    )
    connection.commit()

    # if there is a picture, update that too
    if fileobj:
        # get the old file name
        old_fname = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?",
            (flask.session['logname'], )
        )
        result = old_fname.fetchone()
        file_path = insta485.app.config['UPLOAD_FOLDER']/result['filename']
        # if there is a associated file, remove it
        if os.path.exists(file_path):
            os.remove(os.path.join
                      (insta485.app.config["UPLOAD_FOLDER"], file_path))

        file = insta485.views.upload.file_upload()
        connection.execute(
            "UPDATE users "
            "SET filename = ? "
            "WHERE users.username = ?",
            (file, flask.session['logname'])
        )


# password function


def newpassword():
    """Password jawnt."""
    original = flask.request.form['password']
    new = flask.request.form['new_password1']
    new1 = flask.request.form['new_password2']
    user = flask.session['logname']

    if original == '' or new == '' or new1 == '':
        flask.abort(400)

    connection = insta485.model.get_db()
    # create query
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ?",
        (user, )
    )
    result = cur.fetchone()
    # up is user password
    uppity = result['password']
    # if the og does not match the actual password, abort
    if not password_check(uppity, original):
        flask.abort(403)
    # if new doesn't equal new1, abort
    elif new != new1:
        flask.abort(401)
    # everything went okay
    else:
        # salt password
        salted_new = salt_password(new)
        # update the db
        connection.execute(
            "UPDATE users "
            "SET password = ? "
            "WHERE username = ?",
            (salted_new, user, )
        )


# checks entered vs actual password
def password_check(user_password, entered_password):
    """Check that password jawnt."""
    up_split = user_password.split('$')
    algorithm = up_split[0]
    salt = up_split[1]
    margs = hashlib.new(algorithm)
    password_salted = salt + entered_password
    margs.update(password_salted.encode('utf-8'))
    password_hash = margs.hexdigest()
    return "$".join([algorithm, salt, password_hash]) == user_password

# password salter


def salt_password(password):
    """Salt that jawnt."""
    # salts password
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    return "$".join([algorithm, salt, password_hash])
