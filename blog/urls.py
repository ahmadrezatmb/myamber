from django.urls import path
from .views import about, deletepost, home , loginuser, logoutuser, postpage, resetpasswords ,signup , newpost ,profile ,editprofile ,editpost
urlpatterns = [
    path('', home , name="blog-home"),
    path('about/' , about , name="blog-about"),
    path('login/' , loginuser , name="login"),
    path('signup/' , signup , name="signup"),
    path('about/' , about , name="about"),
    path('newpost/' , newpost , name="newpost"),
    path('profile/<str:username>/' , profile , name="profile"),
    path('editprofile/<str:username>/' , editprofile , name="editprofile"),
    path('post/<int:id>/' , postpage , name="postpage"),
    path('deletepost/<int:id>/' , deletepost , name="deletepost"),
    path('logout/' , logoutuser , name="logout"),
    path('editpost/<int:id>/' ,editpost , name="editpost"),
    path('resetpassword/' , resetpasswords , name="resetpassword")
]
