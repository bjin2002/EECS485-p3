"""REST API for posts."""
import flask
import insta485


@insta485.app.route('/api/v1/')
def get_api():
    """REST API for api/v1."""
    # /api/v1/ DOES NOT return a 403 if the user is not authenticated because
    # it is publicly available
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context), 200


@insta485.app.route('/api/v1/posts/', methods=['GET'])
def get_post_api():
    """REST API for api/v1/posts/."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        context = {"message": "Forbidden", "status_code": 403}
        return flask.jsonify(**context), 403

    posts_size = flask.request.args.get(
        "size", default=10, type=int)
    posts_page = flask.request.args.get(
        "page", default=0, type=int)
    posts_postid_lte = flask.request.args.get(
        "postid_lte", default=float("inf"), type=int)

    # if posts_size or posts_page is negative return 400 Bad Request
    if posts_size < 0 or posts_page < 0:
        context = {"message": "Bad Request", "status_code": 400}
        return flask.jsonify(**context), 400

    connection = insta485.model.get_db()

    # CODE FROM P2 TO GET PRUNED POSTS ##############################
    # posts query
    cur = connection.execute(
        "SELECT * "
        "FROM posts "
        "WHERE posts.postid <= ? "
        "ORDER BY posts.postid DESC",
        (posts_postid_lte, )
    )
    posts = cur.fetchall()

    if len(posts) == -1:
        print("stinky pyl")

    cur = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username1 = ?",
        (insta485.api.helper.username_output(), )
    )

    foll = cur.fetchall()

    user_foll_set = set()
    # Create set of all the users that the logged in user is following
    for row in foll:
        user_foll_set.add(row["username2"])
    pruned_posts = []
    # We now have a list of all the posts that are by the logged in user OR
    # by a user that the logged in user is following
    for row in posts:
        if (row["owner"] in user_foll_set
           or row["owner"] == insta485.api.helper.username_output()):
            new_dict = {}
            new_dict["postid"] = row["postid"]
            pruned_posts.append(new_dict)
    posts_postid_lte = pruned_posts[0]["postid"]

    # Now we must prune the posts to only include the posts that are less than
    # or equal to the postid_lte
    pruned_posts_limited = []

    if posts_size * (posts_page) == len(pruned_posts):
        pruned_posts_limited = []
    else:
        for i in range(posts_size * (posts_page),
                       min(posts_size * (posts_page) + posts_size,
                           len(pruned_posts))):
            pruned_posts[i]["url"] = "/api/v1/posts/" + \
                str(pruned_posts[i]["postid"]) + "/"
            pruned_posts_limited.append(pruned_posts[i])

    # If the length of the result is greater than or
    # equal to posts_size, then we have to set 'next'
    next_url = ""
    if len(pruned_posts_limited) >= posts_size:
        next_url = "/api/v1/posts/?size=" + \
            str(posts_size) + "&page=" + str(posts_page + 1) + \
            "&postid_lte=" + str(posts_postid_lte)

    # if the last character is a question mark, remove it from url string
    if flask.request.full_path[-1] == "?":
        flask.request.full_path = flask.request.full_path[:-1]

    context = {"next": next_url,
               "results": pruned_posts_limited, "url": flask.request.full_path}
    return flask.jsonify(**context), 200


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """REST API for api/v1/posts/<postid>/."""
    # Every REST API route should return 403 if a user is not authenticated.
    if "logname" not in flask.session and not insta485.api.helper.valid_user():
        context = {"message": "Forbidden", "status_code": 403}
        return flask.jsonify(**context), 403

    logname = insta485.api.helper.username_output()
    connection = insta485.model.get_db()

    # Post query
    cur = connection.execute(
        "SELECT * "
        "FROM posts "
        "WHERE posts.postid = ?",
        (postid_url_slug, )
    )
    all_posts = cur.fetchall()
    # Post IDs that are out of range should return a 404 error.
    if len(all_posts) == 0:
        context = {"message": "Not Found", "status_code": 404}
        return flask.jsonify(**context), 404
    post = all_posts[0]

    # Comments query for the specific postid
    cur = connection.execute(
        "SELECT * "
        "FROM comments "
        "WHERE comments.postid = ?"
        "ORDER BY comments.commentid ASC",
        (postid_url_slug, )
    )
    comments = cur.fetchall()

    # delete/add certain fields to prepare dictionary for json format
    for comment in comments:
        comment["lognameOwnsThis"] = (comment["owner"] == logname)
        comment["ownerShowUrl"] = "/users/" + comment["owner"] + "/"
        comment["url"] = "/api/v1/comments/" + str(comment["commentid"]) + "/"
        del comment["postid"]
        del comment["created"]

    # Query for total number of likes on the specific post id
    likes = {}
    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likes.postid = ?",
        (postid_url_slug, )
    )
    total_likes_for_post = cur.fetchall()
    likes["numLikes"] = len(total_likes_for_post)

    # Query to determine if logname liked the post
    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likes.owner = ? "
        "AND likes.postid = ?",
        (logname, postid_url_slug)
    )
    logname_likes_results = cur.fetchall()
    likes["lognameLikesThis"] = (len(logname_likes_results) > 0)
    if likes["lognameLikesThis"]:
        likes["url"] = "/api/v1/likes/" + \
            str(logname_likes_results[0]["likeid"]) + "/"
    else:
        likes["url"] = None

    # Query to find the owner of the post
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE users.username = ?",
        (post["owner"], )
    )
    owner_of_post_filename = cur.fetchone()

    # if the last character is a question mark, remove it from url string
    url = flask.request.full_path
    if url[-1] == "?":
        url = url[:-1]

    context = {"comments": comments,
               "comments_url":
               "/api/v1/comments/?postid=" + str(postid_url_slug),
               "created": post["created"],
               "imgUrl": "/uploads/" + post["filename"],
               "likes": likes,
               "owner": post["owner"],
               "ownerImgUrl": "/uploads/" + owner_of_post_filename["filename"],
               "ownerShowUrl": "/users/" + post["owner"] + "/",
               "postShowUrl": "/posts/" + str(postid_url_slug) + "/",
               "postid": postid_url_slug,
               "url": url}
    return flask.jsonify(**context), 200
