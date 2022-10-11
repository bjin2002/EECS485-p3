"""REST API for posts."""
import flask
import insta485


@insta485.app.route('/api/v1/')
def get_api():
    """REST API for api/v1."""
    # Every REST API route should return 403 if a user is not authenticated.
    # The only exception is /api/v1/, which is publicly available.
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context), 200


# @insta485.app.route('/api/v1/posts/?size=N&page=N&postid_lte=N', methods=['GET'])
@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_post_api():
    """REST API for api/v1/?size=N&page=N&postid_lte=N"""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session or not insta485.api.helper.valid_user():
        flask.abort(403)

    logname = flask.session['logname']
    DEFAULT_POSTS_SIZE = 10

    posts_size = flask.request.args.get(
        "size", default=DEFAULT_POSTS_SIZE, type=int)
    posts_page = flask.request.args.get('page', type=int)
    posts_postid_lte = flask.request.args.get(
        'postid_lte', default=float("inf"), type=int)

    connection = insta485.model.get_db()

    # CODE FROM P2
    # users query
    logname = flask.session['logname']
    cur = connection.execute(
        "SELECT username, fullname "
        "FROM users "
        "WHERE username != ?",
        (logname, )
    )
    users = cur.fetchall()

    # posts query
    cur = connection.execute(
        "SELECT * "
        "FROM posts "
        "ORDER BY posts.postid DESC"
    )
    posts = cur.fetchall()

    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ?",
        (logname, )
    )
    following = cur.fetchall()

    logged_user_following_list = set()
    # Create set of all the users that the logged in user is following
    for row in following:
        logged_user_following_list.add(row["username2"])

    pruned_posts = []
    for row in posts:
        if (row["owner"] in logged_user_following_list
           or row["owner"] == flask.session['logname']):
            newDict = {}
            newDict["postid"] = row["postid"]
            pruned_posts.append(newDict)

    pruned_posts_limited = []
    i = 0
    start_index = posts_size * (posts_page - 1)
    for row in pruned_posts:
        row["url"] = "/api/v1/posts/" + str(row["postid"]) + "/"

        if (start_index <= i and i < start_index + posts_size):
            pruned_posts_limited.append(row)

            # if postid is greater than postid_lte, break
            if (row["postid"] >= posts_postid_lte):
                break

        i += 1

    # # posts query for posts by logged in user or users they follow
    # cur_posts = connection.execute(
    #     "SELECT postid "
    #     "FROM posts "
    #     "ORDER BY posts.postid DESC "
    #     "OFFEST ?",
    #     (posts_size * (posts_page - 1),)
    # )
    # cur_posts_result = cur_posts.fetchall()

    # If the length of the result is greater than or equal to posts_size, then we have to set 'next'
    next_url = ""
    if len(pruned_posts) == posts_size:
        next_url = f"/api/v1/posts/?size={posts_size}&page={posts_page + 1}&postid_lte={posts_postid_lte}"
    elif len(pruned_posts) > posts_size:
        next_url = f"/api/v1/posts/?size={posts_size}&page={posts_page + 1}&postid_lte={posts_postid_lte}"

    context = {"next": next_url,
               "results": pruned_posts_limited, "url": flask.request.url}
    return flask.jsonify(**context), 200


# @insta485.app.route('/api/v1/posts/?size=N')
# def get_newest_posts():
#     """REST API for api/v1/posts/?size=N'"""
#     # Every REST API route should return 403 if a user is not authenticated.
#     if "logname" not in flask.session or not insta485.api.helper.valid_user():
#         flask.abort(403)

#     connection = insta485.model.get_db()

#     pass


# @insta485.app.route('/api/v1/posts/?page=N')
# def get_nth_page():
#     """REST API for api/v1/posts/?page=N'"""
#     # Every REST API route should return 403 if a user is not authenticated.
#     if "logname" not in flask.session or not insta485.api.helper.valid_user():
#         flask.abort(403)

#     connection = insta485.model.get_db()

#     pass


# @insta485.app.route('/api/v1/posts/?postid_lte=N')
# def get_post_ids():
#     """REST API for api/v1/posts/?postid_lte=N"""
#     # Every REST API route should return 403 if a user is not authenticated.
#     if "logname" not in flask.session or not insta485.api.helper.valid_user():
#         flask.abort(403)

#     connection = insta485.model.get_db()

#     pass


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post():
    """REST API for api/v1/posts/<postid>/"""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session or not insta485.api.helper.valid_user():
        flask.abort(403)

    connection = insta485.model.get_db()

    pass


# @insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
# def get_post(postid_url_slug):
#   if "logname" in flask.session or insta485.api.helper.valid_user():
#     username = ""
#     dict = {}
#     connection = insta485.model.get_db()
#     cur = connection.execute(
#       "SELECT * "
#       "FROM comments "
#       "WHERE postid = ?",
#       (postid_url_slug, )
#     )
#     # TODO: general idea, flesh out later
#     result = cur.fetchall()
#     for comment in result:
#       if comment.owner == username:
#         context = {
#         "created": "2017-09-28 04:33:28",
#         "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
#         "owner": "awdeorio",
#         "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
#         "ownerShowUrl": "/users/awdeorio/",
#         "postid": "/posts/{}/".format(postid_url_slug),
#         "url": flask.request.path,
#     }
#     return flask.jsonify(**context)
#   else:
#     flask.abort(403)
