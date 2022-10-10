"""
Insta485 explore view.

URLs include:
/explore/
"""
import flask
import insta485


@insta485.app.route('/explore/', methods=['GET'])
def show_explore():
    """Show explore template."""
    if flask.session['logname']:
        connection = insta485.model.get_db()
        logname = flask.session['logname']

        all_users = connection.execute(
            "SELECT * "
            "FROM users "
            "WHERE username != ?",
            (logname, )
        )
        users = all_users.fetchall()

        all_following_explore = connection.execute(
            "SELECT username2 "
            "FROM following "
            "WHERE username1 = ?",
            (logname, )
        )
        following = all_following_explore.fetchall()

        logged_user_following_list = set()
        # Create set of all the users that the logged in user is following
        for row in following:
            logged_user_following_list.add(row["username2"])

        exploreusers = []
        for row in users:
            if row["username"] not in logged_user_following_list:
                exploreusers.append(row)

        # Add database info to context
        context = {"users": exploreusers, "logname": flask.session['logname']}
        return flask.render_template("explore.html", **context)

    return flask.redirect(flask.url_for('show_login'))
