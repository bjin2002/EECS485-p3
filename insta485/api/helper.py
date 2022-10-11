"""Helper funtions for REST API calls."""
import hashlib
import flask
import insta485


def valid_user():
    """Checks http request valid users."""
    if "username" not in flask.request.authorization or "password" not in flask.request.authorization:
        return False

    # There is a username and password
    else:
        username = flask.request.authorization['username']
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
        entered_password = flask.request.authorization['password']
        up_split = user_password.split('$')
        algorithm = up_split[0]
        salt = up_split[1]
        margs = hashlib.new(algorithm)
        password_salted = salt + entered_password
        margs.update(password_salted.encode('utf-8'))
        password_hash = margs.hexdigest()
        return "$".join([algorithm, salt, password_hash]) == user_password
