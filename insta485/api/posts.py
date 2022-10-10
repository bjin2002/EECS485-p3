"""REST API for posts."""
import flask
import insta485

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
def get_post_api():
  """REST API for api/v1/posts."""
  if "logname" in flask.session or insta485.api.helper.valid_user():
    connection = insta485.model.get_db()
    cur = connection.execute(

    )
  else:
    flask.abort(403)

@insta485.app.route('/api/v1/posts/?size=N')
def get_newest_posts():
  """REST API for api/v1/posts/?size=N'"""
  pass

@insta485.app.route('/api/v1/posts/?page=N')
def get_nth_page():
  """REST API for api/v1/posts/?page=N'"""
  pass

@insta485.app.route('/api/v1/posts/?postid_lte=N')
def get_post_ids():
  """REST API for api/v1/posts/?postid_lte=N"""
  pass

@insta485.app.route('/api/v1/posts/<postid>/')
def get_post():
  """REST API for api/v1/posts/<postid>/"""
  pass


@insta485.app.route('/api/v1/likes/?postid=<postid>')
def create_like():
  """REST API for api/v1/likes/?postid=<postid>"""
  pass


@insta485.app.route('/api/v1/likes/?<likeid>/')
def delete_like():
  """REST API for api/v1/likes/?<likeid>/"""
  pass

@insta485.app.route('/api/v1/comments/?postid=<postid>')
def create_comment():
  """REST API for api/v1/comments/?postid=<postid>"""
  pass

@insta485.app.route('/api/v1/comments/<commentid>/')
def delete_comment():
  """REST API for api/v1/comments/<commentid>/"""
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