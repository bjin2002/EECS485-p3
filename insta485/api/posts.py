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
    """REST API for api/v1/?size=N&page=N&postid_lte=N."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        flask.abort(403)

    logname = flask.session['logname']
    DEFAULT_POSTS_SIZE = 10

    posts_size = flask.request.args.get(
        "size", default=DEFAULT_POSTS_SIZE, type=int)
    posts_page = flask.request.args.get('page', type=int)
    posts_postid_lte = flask.request.args.get(
        'postid_lte', default=float("inf"), type=int)

    connection = insta485.model.get_db()

    # CODE FROM P2 TO GET PRUNED POSTS ######################
    # users query
    logname = flask.session['logname']
    cur = connection.execute(
        "SELECT username, fullname "
        "FROM users "
        "WHERE username != ?",
        (logname, )
    )
    users = cur.fetchall()

    print(users)
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
    # We now have a list of all the posts that are by the logged in user OR
    # by a user that the logged in user is following
    for row in posts:
        if (row["owner"] in logged_user_following_list
           or row["owner"] == flask.session['logname']):
            newDict = {}
            newDict["postid"] = row["postid"]
            pruned_posts.append(newDict)

    # Now we must prune the posts to only include the posts that are less than
    # or equal to the postid_lte
    pruned_posts_limited = []
    i = 0
    # WRONG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # /api/v1/posts/?size=10&page=1&postid_lte=11.
    # A GET request to the next url will return 1 post in this case.
    start_index = posts_size * (posts_page - 1)
    for row in pruned_posts:
        row["url"] = "/api/v1/posts/" + str(row["postid"]) + "/"

        if (start_index <= i and i < start_index + posts_size):
            pruned_posts_limited.append(row)

            # if postid is greater than postid_lte, break
            if (row["postid"] >= posts_postid_lte):
                break

        i += 1

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
#     """REST API for api/v1/posts/?size=N'."""
#     # Every REST API route should return 403 if a user is not authenticated.
#     if "logname" not in flask.session and not insta485.api.helper.valid_user():
#         flask.abort(403)

#     connection = insta485.model.get_db()

#     pass


# @insta485.app.route('/api/v1/posts/?page=N')
# def get_nth_page():
#     """REST API for api/v1/posts/?page=N."""
#     # Every REST API route should return 403 if a user is not authenticated.
#     if "logname" not in flask.session and not insta485.api.helper.valid_user():
#         flask.abort(403)

#     connection = insta485.model.get_db()

#     pass


# @insta485.app.route('/api/v1/posts/?postid_lte=N')
# def get_post_ids():
#     """REST API for api/v1/posts/?postid_lte=N."""
#     # Every REST API route should return 403 if a user is not authenticated.
#     if "logname" not in flask.session and not insta485.api.helper.valid_user():
#         flask.abort(403)

#     connection = insta485.model.get_db()

#     pass


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post():
    """REST API for api/v1/posts/<postid>/."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        flask.abort(403)

    logname = flask.session['logname']
    connection = insta485.model.get_db()

    flask.request.args.get(
        'postid_lte', default=float("inf"), type=int)

    # Get postid from url
    post_id_url_slug = flask.request.args.get('postid_url_slug', type=int)

    # Post query
    cur_post = connection.execute(
        "SELECT * "
        "FROM posts "
        "WHERE posts.postid = ?",
        (post_id_url_slug, )
    )
    post = cur_post.fetchall()

    # Post IDs that are out of range should return a 404 error.
    if len(post) == 0:
        flask.abort(404)

    # Comments query
    cur_comments = connection.execute(
        "SELECT * "
        "FROM comments "
        "WHERE comments.postid = ?"
        "ORDER BY comments.commentid ASC",
        (post_id_url_slug, )
    )
    comments = cur_comments.fetchall()

    # delete/add certain fields to prepare dictionary for json format
    for comment in comments:
        comment["lognameOwnsThis"] = (comment["owner"] == logname)
        comment["ownerShowUrl"] = "/users/" + comment["owner"] + "/"
        comment["url"] = "/api/v1/comments/" + str(comment["postid"]) + "/"
        del comment["postid"]
        del comment["created"]

    # likes query and dict creation
    likes = {}
    cur_likes = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likes.postid = ?",
        (post_id_url_slug, )
    )
    total_likes_for_post = cur_likes.fetchall()
    likes["numLikes"] = len(total_likes_for_post)

    cur_likes = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likes.owner = ?",
        (logname, )
    )
    likes_results = cur_likes.fetchall()
    likes["lognameLikesThis"] = (len(likes_results) > 0)
    # FIX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    likes["url"] = "/api/v1/likes/" + str(post_id_url_slug) + "/"

    # context = {"comments": comments,
    #            "comments_url": "/api/v1/comments/?postid=" + str(post_id_url_slug),
    #            "created": post["created"],
    #            "imgUrl": post, #FIX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #            "likes": likes,
    #            "owner": post["owner"],
    #            "ownerImgUrl": ,
    #            "ownerShowUrl":,
    #            "postShowUrl":,
    #            "postid":,
    #            "url":}
    context = {}
    return flask.jsonify(**context), 200

    pass


# @insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
# def get_post(postid_url_slug):
#   """REST API for /api/v1/posts/<int:postid_url_slug>/."""
#   if "logname" in flask.session and insta485.api.helper.valid_user():
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
