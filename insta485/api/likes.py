"""REST API for posts."""
import flask
import insta485


@insta485.app.route('/api/v1/likes/?postid=<postid>')
def create_like():
    """REST API for api/v1/likes/?postid=<postid>."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        flask.abort(403)

    connection = insta485.model.get_db()

    pass


@insta485.app.route('/api/v1/likes/?<likeid>/')
def delete_like():
    """REST API for api/v1/likes/?<likeid>/."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        flask.abort(403)

    connection = insta485.model.get_db()

    pass
