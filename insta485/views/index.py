"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485


@insta485.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""
    # Connect to database
    connection = insta485.model.get_db()

    # Check if user is logged in
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

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
            pruned_posts.append(row)

    for row in pruned_posts:
        row["post_liked_by_logname"] = 0

        # for the current row in posts, query for all likes with that postId
        cur = connection.execute(
            "SELECT * "
            "FROM likes "
            "WHERE likes.postid = ?",
            (row["postid"], )
        )
        likes_for_post = cur.fetchall()

        # set post likes equal to size of query (num likes)
        row["post_likes"] = len(likes_for_post)

        # determine whether the post was liked by the logged in user (logname)
        for like in likes_for_post:
            if like["owner"] == logname:
                row["post_liked_by_logname"] = 1
                break

        # add the profile pic name for the post
        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE users.username = ?",
            (row["owner"], )
        )

        pro_pic = cur.fetchone()

        row["pro_pic"] = pro_pic["filename"]

        # humanize the time the post was created
        row["created"] = arrow.get(row["created"]).humanize()

    # comments query
    cur = connection.execute(
        "SELECT * "
        "FROM comments "
        "ORDER BY comments.commentid ASC"
    )
    comments = cur.fetchall()

    # Add database info to context
    context = {"users": users, "posts": pruned_posts, "comments": comments,
               "logname": flask.session['logname']}
    return flask.render_template("index.html", **context)
