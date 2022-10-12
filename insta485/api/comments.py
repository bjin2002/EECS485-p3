"""REST API for comments."""
import flask
import insta485


@insta485.app.route('/api/v1/comments/?postid=<postid>', methods = ['POST'])
def create_comment():
    """REST API for api/v1/comments/?postid=<postid>."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        flask.abort(403)

    connection = insta485.model.get_db()


    connection.execute(
        "INSERT INTO comments (owner, postid, text) VALUES (?, ?, ?)",
        (flask.session['logname'],
         flask.request.form['postid'],
         flask.request.form['text']))

         
    

    pass


@insta485.app.route('/api/v1/comments/<commentid>/')
def delete_comment():
    """REST API for api/v1/comments/<commentid>/."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        flask.abort(403)

    connection = insta485.model.get_db()

    pass
