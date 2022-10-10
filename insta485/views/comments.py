"""Comment bullshit."""
import flask
import insta485


@insta485.app.route('/comments/', methods=['POST'])
def comments_target():
    """Comments target."""
    target = flask.request.args.get('target')

    if not target:
        target = "/"

    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_index'))

    if flask.request.form['operation'] == 'create':
        create_comments()
    if flask.request.form['operation'] == 'delete':
        delete_comments()

    return flask.redirect(target)


def create_comments():
    """Create comments."""
    connection = insta485.model.get_db()

    if flask.request.form['text'] == "":
        flask.abort(400)

    # create query
    connection.execute(
        "INSERT INTO comments (owner, postid, text) VALUES (?, ?, ?)",
        (flask.session['logname'],
         flask.request.form['postid'],
         flask.request.form['text']))


def delete_comments():
    """Delete comments."""
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT * FROM comments "
        "WHERE commentid = ?"
        "AND owner = ?",
        (flask.request.form['commentid'], flask.session['logname'], )
    )

    result = cur.fetchone()
    # if the comment is not owned by the logname, then abort
    if not result:
        flask.abort(403)

    # delete query
    connection.execute(
        "DELETE FROM comments "
        "WHERE commentid = ?"
        "AND owner = ?",
        (flask.request.form['commentid'], flask.session['logname'], )
    )
