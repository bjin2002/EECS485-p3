"""Likes."""
import flask
import insta485


@insta485.app.route('/likes/', methods=['POST'])
def likes_target():
    """Likes target."""
    target = flask.request.args.get('target')

    if not target:
        target = "/"

    if flask.request.form['operation'] == 'like':
        like()
    if flask.request.form['operation'] == 'unlike':
        unlike()
    return flask.redirect(target)


def unlike():
    """Unlikes."""
    connection = insta485.model.get_db()

    # Query for likes
    cur_likes = connection.execute(
        "SELECT * FROM likes "
        "WHERE postid = ?"
        "AND owner = ?",
        (flask.request.form['postid'], flask.session['logname'], )
    )

    result = cur_likes.fetchone()
    # if the post is already unliked by the logname, abort
    if not result:
        flask.abort(409)

    # delete query
    connection.execute(
        "DELETE FROM likes "
        "WHERE postid = ?"
        "AND owner = ?",
        (flask.request.form['postid'], flask.session['logname'], )
    )


def like():
    """Likes."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM likes "
        "WHERE postid = ?"
        "AND owner = ?",
        (flask.request.form['postid'], flask.session['logname'], )
    )

    result = cur.fetchone()
    # if the post is already liked by the logname, abort
    if result:
        flask.abort(409)

    # create query
    connection.execute(
        "INSERT INTO likes (owner, postid) VALUES (?, ?)",
        (flask.session['logname'], flask.request.form['postid'], ))
