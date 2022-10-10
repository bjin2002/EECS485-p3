"""Views, one for each Insta485 page."""
from insta485.views.accounts import show_login
from insta485.views.accounts import logout
from insta485.views.accounts import show_create
from insta485.views.accounts import show_delete
from insta485.views.accounts import show_edit
from insta485.views.accounts import show_password
from insta485.views.accounts import account_target
from insta485.views.comments import comments_target
from insta485.views.explore import show_explore
from insta485.views.following import following_target
from insta485.views.index import show_index
from insta485.views.likes import likes_target
from insta485.views.posts import show_post
from insta485.views.posts import posts_target
from insta485.views.upload import file_upload
from insta485.views.upload import image_render
from insta485.views.users import show_user
