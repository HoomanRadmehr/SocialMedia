from django.urls import path
from . import views

app_name = 'post'
urlpatterns =[
    path('allposts', views.all_posts , name='all_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/' , views.post_detail , name = "post_detail" ),
    path('addpost/<int:user_id>/',views.add_post,name = 'add_post'),
    path('editpost/<int:post_id>/<int:user_id>/',views.edit_post,name='edit_post'),
    path('deletepost/<int:post_id>/<int:user_id>/',views.delete_post , name='delete_post'),
    path('addcomment/<int:post_id>/<int:user_id>/' , views.add_comment , name= 'add_comment'),
    path('addreply/<int:post_id>/<int:comment_id>/<int:user_id>/' , views.add_reply , name='add_reply'),
    path('like/<int:post_id>/<int:user_id>/',views.like_post, name='like_post'),
]