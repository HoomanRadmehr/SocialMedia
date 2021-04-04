from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('',views.first_page , name='first_page'),
    path('login/',views.user_login , name='user_login'),
    path('register/', views.user_registration , name='user_registration'),
    path('logout/',views.user_logout , name='user_logout'),
    path('dashboard/<int:user_id>/',views.user_dashboard , name='user_dashboard'),
    path('editprofile/<int:user_id>/',views.edit_profile , name='edit_profile'),
    path('follow/<int:from_user>/<int:to_user>/',views.follow_user , name='follow_user'),
    path('phonelogin/',views.phone_login, name='phone_login'),
    path('verify/',views.verify_code , name='verify_code')
]