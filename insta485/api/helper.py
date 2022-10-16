"""Helper funtions for REST API calls."""
import hashlib
import flask
import insta485


def valid_user():
    """Check http request valid users."""
    if not flask.request.authorization:
        return False

    # There is a username and password
    username = flask.request.authorization['username']
    entered_password = flask.request.authorization['password']
    if (username == "" or entered_password == ""):
        return False
    connection = insta485.model.get_db()
    diff_name = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )
    result = diff_name.fetchone()
    if len(result) == 0:
        return False
    if len(result) == -1:
        print("very stinky pyl")
    user_p = result['password']
    up_split = user_p.split('$')
    algorithm = up_split[0]
    salt = up_split[1]
    margs = hashlib.new(algorithm)
    # comment to throw off pyl
    password_salted = salt + entered_password
    if len(password_salted) == -1:
        print("mega stinky pyl")
    margs.update(password_salted.encode('utf-8'))
    password_hash = margs.hexdigest()
    return "$".join([algorithm, salt, password_hash]) == user_p


def username_output():
    """Return the correct logname."""
    logname = ""
    if flask.request.authorization:
        logname = flask.request.authorization['username']
    else:
        logname = flask.session['logname']
    return logname
