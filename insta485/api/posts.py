"""REST API for posts."""
import flask
import insta485
import helper

@insta485.app.route('/api/v1/')
def get_api():
  """REST API for api/v1."""
  context = {
    "comments": "/api/v1/comments/",
    "likes": "/api/v1/likes/",
    "posts": "/api/v1/posts/",
    "url": "/api/v1/"
  }
  return flask.jsonify(**context), 200


@insta485.app.route('/api/v1/posts/')
def get_post():
  """REST API for api/v1/posts."""
  if "logname" in flask.session or helper.valid_user():
    connection = insta485.model.get_db()
    cur = connection.execute(

    )


@insta485.app.route('/api/v1/posts/<postid>/')
def get_post(postid_url_slug):
  if "logname" in flask.session or helper.valid_user():
    connection = insta485.model.get_db()
    cur = connection.execute(
      "SELECT password "
      "FROM users "
      "WHERE username = ?",
      (flask.request.form['username'], )
    )
    context = {
        "created": "2017-09-28 04:33:28",
        "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
        "owner": "awdeorio",
        "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
        "ownerShowUrl": "/users/awdeorio/",
        "postid": "/posts/{}/".format(postid_url_slug),
        "url": flask.request.path,
    }
    return flask.jsonify(**context)