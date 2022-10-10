"""Posts."""
import os
import flask
import arrow
import insta485


@insta485.app.route('/posts/<postid>/', methods=['GET'])
def show_post(postid):
    """Display / route."""
    # Connect to database
    connection = insta485.model.get_db()

    # Check if user is logged in
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session['logname']

    # posts query
    cur_posts = connection.execute(
        "SELECT * "
        "FROM posts "
        "WHERE posts.postid = ?",
        (postid, )
    )
    post = cur_posts.fetchone()
    if not post:
        flask.abort(403, "post query has failed in 'show_post'")

    post["post_liked_by_logname"] = 0

    # for the post, query for all of the likes with that postId
    cur_likes = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likes.postid = ?",
        (post["postid"], )
    )
    likes_for_post = cur_likes.fetchall()

    # set post likes equal to size of query (num likes)
    post["post_likes"] = len(likes_for_post)

    # determine whether the post was liked by the logged in user (logname)
    for like in likes_for_post:
        if like["owner"] == logname:
            post["post_liked_by_logname"] = 1
            break

    # add the profile pic name for the post
    cur_pro_pic = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE users.username = ?",
        (post["owner"], )
    )
    pro_pic = cur_pro_pic.fetchone()

    post["pro_pic"] = pro_pic["filename"]

    # humanize the time the post was created
    post["created"] = arrow.get(post["created"]).humanize()

    # comments query
    cur_comments = connection.execute(
        "SELECT * "
        "FROM comments "
        "WHERE comments.postid = ?"
        "ORDER BY comments.commentid ASC",
        (post["postid"], )
    )
    comments = cur_comments.fetchall()

    # Add database info to context
    context = {"post": post, "comments": comments,
               "logname": flask.session['logname']}
    return flask.render_template("post.html", **context)


@insta485.app.route('/posts/', methods=['POST'])
def posts_target():
    """Post target."""
    target = flask.request.args.get('target')

    logname = flask.session['logname']
    if not target:
        target = f"/users/{logname}/"

    if flask.request.form['operation'] == 'create':
        create_posts()
    if flask.request.form['operation'] == 'delete':
        delete_posts()
    print(target)
    return flask.redirect(target)


def create_posts():
    """Post."""
    connection = insta485.model.get_db()

    # uploads picture to db
    file = insta485.views.upload.file_upload()

    # create query
    connection.execute(
        "INSERT INTO posts (owner, filename) VALUES (?, ?)",
        (flask.session['logname'], str(file))
    )


def delete_posts():
    """Delete."""
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT * FROM posts "
        "WHERE postid = ?"
        "AND owner = ?",
        (flask.request.form['postid'], flask.session['logname'], )
    )

    result = cur.fetchone()
    # if the post is already unliked by the logname, abort
    if not result:
        flask.abort(403)

    # query the database for the post's file name
    cur = connection.execute(
        "SELECT filename "
        "FROM posts "
        "WHERE owner = ?"
        "AND postid = ?",
        (flask.session['logname'], flask.request.form['postid'], )
    )
    result = cur.fetchone()

    file_path = os.path.join(
        insta485.app.config["UPLOAD_FOLDER"], result['filename'])

    # if there is a associated file, remove it
    if os.path.exists(file_path):
        os.remove(file_path)

    # delete query
    connection.execute(
        "DELETE FROM posts "
        "WHERE postid = ?"
        "AND owner = ?",
        (flask.request.form['postid'], flask.session['logname'], )
    )
