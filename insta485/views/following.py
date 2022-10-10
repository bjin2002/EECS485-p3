"""Following."""
import flask
import insta485


@insta485.app.route('/following/', methods=['POST'])
def following_target():
    """Likes target."""
    target = flask.request.args.get('target')

    if not target:
        target = "/"

    if flask.request.form['operation'] == 'follow':
        follow()
    if flask.request.form['operation'] == 'unfollow':
        unfollow()
    return flask.redirect(target)


def follow():
    """Follow."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM following "
        "WHERE username1 = ?"
        "AND username2 = ?",
        (flask.session['logname'], flask.request.form['username'], )
    )

    result = cur.fetchone()
    # if the logged in user already follows the user, abort
    if result:
        flask.abort(409)

    # enter new following relationship
    connection.execute(
        "INSERT INTO following (username1, username2) VALUES (?, ?)",
        (flask.session['logname'], flask.request.form['username'], ))


def unfollow():
    """Unfollow."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM following "
        "WHERE username1 = ?"
        "AND username2 = ?",
        (flask.session['logname'], flask.request.form['username'], )
    )

    result = cur.fetchone()
    # if the logged in user already unfollows the user, abort
    if not result:
        flask.abort(409)

    # delete the following relationship
    connection.execute(
        "DELETE FROM following "
        "WHERE username1 = ?"
        "AND username2 = ?",
        (flask.session['logname'], flask.request.form['username'], )
    )
