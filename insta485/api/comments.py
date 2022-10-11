"""REST API for comments."""
import flask
import insta485


@insta485.app.route('/api/v1/comments/', methods=['POST'])
def create_comment():
    """REST API for api/v1/comments/?postid=<postid>."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        flask.abort(403)

    connection = insta485.model.get_db()
    logname = insta485.api.helper.username_output()
    postid = flask.request.args.get("postid", type=int)
    text = flask.request.json.get("text", None)

    connection.execute(
        "INSERT INTO comments (owner, postid, text) VALUES (?, ?, ?)",
        (logname,
         postid,
         text)
    )

    # Comments query for the newest comment
    cur_comments = connection.execute(
        "SELECT last_insert_rowid() AS commentid",
    )
    new_comment = cur_comments.fetchone()

    url = flask.request.full_path
    if url[-1] == "?":
        url = url[:-1]

    context = {
        "commentid": new_comment["commentid"],
        "lognameOwnsThis": True,
        "owner": logname,
        "ownerShowUrl": "/users/" + logname + "/",
        "text": "Comment sent from httpie",
        "url": "/api/v1/comments/" + str(new_comment["commentid"]) + "/"
    }
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/comments/<commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """REST API for api/v1/comments/<commentid>/."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        flask.abort(403)

    connection = insta485.model.get_db()
    logname = insta485.api.helper.username_output()

    # SQL for comment id
    cur_comment = connection.execute(
        "SELECT * "
        "FROM comments "
        "WHERE comments.commentid = ?",
        (commentid, )
    )
    comment = cur_comment.fetchone()

    # If comment does not exist, return 404
    if comment is None:
        context = {"message": "Not Found", "status_code": 404}
        return flask.jsonify(**context), 404

    # If users doesn't own comment, return 403
    if comment["owner"] != logname:
        context = {"message": "Forbidden", "status_code": 403}
        return flask.jsonify(**context), 403

    # SQL query to delete the comment
    connection.execute(
        "DELETE FROM comments WHERE commentid = ?",
        (commentid, )
    )

    # flask return 204 if successful
    return "", 204
