"""Helper funtions for REST API calls."""
import hashlib
import flask
import insta485


def valid_user():
    """Checks http request valid users."""
    if not flask.request.authorization:
        return False

    # There is a username and password
    else:
        username = flask.request.authorization['username']
        entered_password = flask.request.authorization['password']
        if (username == "" or entered_password == ""):
            return False
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT password "
            "FROM users "
            "WHERE username = ?",
            (username, )
        )
        result = cur.fetchone()
        if len(result) == 0:
            return False
        user_password = result['password']
        up_split = user_password.split('$')
        algorithm = up_split[0]
        salt = up_split[1]
        margs = hashlib.new(algorithm)
        password_salted = salt + entered_password
        margs.update(password_salted.encode('utf-8'))
        password_hash = margs.hexdigest()
        return "$".join([algorithm, salt, password_hash]) == user_password

def username_output():
    """Returns the correct logname."""
    logname = ""
    if flask.request.authorization:
        logname = flask.request.authorization['username']
    else:
        logname = flask.session['logname']
    return logname
