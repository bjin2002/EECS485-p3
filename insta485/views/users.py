"""Users."""
import flask
import insta485


@insta485.app.route('/users/<username>/', methods=['GET'])
def show_user(username):
    """Show user."""
    # Connect to database
    connection = insta485.model.get_db()

    # Check if user is logged in
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session['logname']

    # users query
    cur_users = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ?",
        (username, )
    )
    user = cur_users.fetchone()

    # following query
    cur_following = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username1 = ?",
        (username, )
    )
    following = cur_following.fetchall()

    # followers query
    cur_followers = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username2 = ?",
        (username, )
    )
    followers = cur_followers.fetchall()

    # posts query
    cur_posts = connection.execute(
        "SELECT * "
        "FROM posts "
        "WHERE owner = ?",
        (username, )
    )
    posts = cur_posts.fetchall()

    # Does logname follow username?
    user["logname_follows_username"] = 0
    cur = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username1 = ?"
        "AND username2 = ?",
        (logname, username, )
    )
    logname_check = cur.fetchall()
    if len(logname_check) >= 1:
        user["logname_follows_username"] = 1

    user["num_posts"] = len(posts)

    # Add database info to context
    context = {"logname": logname,
               "user": user,
               "posts": posts,
               "total_posts": len(posts),
               "followers": len(followers),
               "following": len(following)}
    return flask.render_template("user.html", **context)


@insta485.app.route('/users/<username>/followers/', methods=['GET'])
def show_user_followers(username):
    """Show user followers."""
    # Connect to database
    connection = insta485.model.get_db()

    # Check if user is logged in
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session['logname']

    # followers query
    cur_followers = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username2 = ?",
        (username, )
    )
    followers = cur_followers.fetchall()

    set_of_followers = set()
    for follower in followers:
        set_of_followers.add(follower["username1"])

    # users query
    cur_users = connection.execute(
        "SELECT * "
        "FROM users "
    )
    users = cur_users.fetchall()

    pruned_users = []
    for user in users:
        user["logname_follows_username"] = 1
        # CHECK IF LOGNAME FOLLOWS USERNAME BACK
        # followers query
        cur_follow_back_check = connection.execute(
            "SELECT * "
            "FROM following "
            "WHERE username1 = ? "
            "AND username2 = ?",
            (logname, user["username"])
        )
        follow_back_check = cur_follow_back_check.fetchall()

        if not follow_back_check:
            user["logname_follows_username"] = 0

        if user["username"] in set_of_followers:
            pruned_users.append(user)

    print(pruned_users)
    # Add database info to context
    context = {"logname": logname,
               "page_username": username,
               "users": pruned_users,
               "followers": followers}
    return flask.render_template("followers.html", **context)


@insta485.app.route('/users/<username>/following/', methods=['GET'])
def show_user_following(username):
    """Show user following."""
    # Connect to database
    connection = insta485.model.get_db()

    # Check if user is logged in
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session['logname']

    # following query
    cur_following = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username1 = ?",
        (username, )
    )
    following = cur_following.fetchall()

    set_of_following = set()
    for jit in following:
        set_of_following.add(jit["username2"])

    # users query
    cur_users = connection.execute(
        "SELECT * "
        "FROM users "
    )
    users = cur_users.fetchall()

    pruned_users = []
    for user in users:
        user["logname_follows_username"] = 1
        # CHECK IF LOGNAME FOLLOWS USERNAME BACK
        # followers query
        cur_follow_back_check = connection.execute(
            "SELECT * "
            "FROM following "
            "WHERE username1 = ? "
            "AND username2 = ?",
            (logname, user["username"])
        )
        follow_back_check = cur_follow_back_check.fetchall()

        if not follow_back_check:
            user["logname_follows_username"] = 0

        if user["username"] in set_of_following:
            pruned_users.append(user)

    # Add database info to context
    context = {"logname": logname,
               "page_username": username,
               "users": pruned_users,
               "following": following}
    return flask.render_template("following.html", **context)
