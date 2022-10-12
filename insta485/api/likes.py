"""REST API for posts."""
import flask
import insta485


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def create_like():
    """REST API for api/v1/likes/?postid=<postid>."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        context = {"message": "Forbidden", "status_code": 403}
        return flask.jsonify(**context), 403

    connection = insta485.model.get_db()
    logname = insta485.api.helper.username_output()
    postid = flask.request.args.get("postid", type=int)

    # SQL for like with specific postid
    cur_like = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likes.owner = ? AND likes.postid = ?",
        (logname, postid)
    )
    like = cur_like.fetchone()

    # If like exists, return 200
    if like is not None:
        context = {"likeid": like["likeid"],
                   "url": "/api/v1/likes/" + str(like["likeid"]) + "/"}
        return flask.jsonify(**context), 200

    # If like does not exist, create like
    connection.execute(
        "INSERT INTO likes (owner, postid) VALUES (?, ?)",
        (logname,
         postid)
    )

    # Likes query for the newest like
    cur_likes = connection.execute(
        "SELECT last_insert_rowid() AS likeid",
    )
    new_like = cur_likes.fetchone()

    url = flask.request.full_path
    if url[-1] == "?":
        url = url[:-1]

    context = {
        "likeid": new_like["likeid"],
        "url": "/api/v1/likes/" + str(new_like["likeid"]) + "/"
    }
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/likes/<likeid>/', methods=['DELETE'])
def delete_like(likeid):
    """REST API for api/v1/likes/<likeid>/."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        context = {"message": "Forbidden", "status_code": 403}
        return flask.jsonify(**context), 403

    connection = insta485.model.get_db()
    logname = insta485.api.helper.username_output()

    # SQL for like id
    cur_like = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likes.likeid = ?",
        (likeid, )
    )
    like = cur_like.fetchone()

    # If like does not exist, return 404
    if like is None:
        flask.abort(404)

    # If user does not own like, return 403
    if like["owner"] != logname:
        flask.abort(403)

    # If like exists, delete like
    connection.execute(
        "DELETE FROM likes WHERE likes.likeid = ?",
        (likeid, )
    )

    return "", 204
