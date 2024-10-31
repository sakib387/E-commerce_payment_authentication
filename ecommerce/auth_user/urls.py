from django.urls import path
from auth_user import views

urlpatterns = [
       path('/signIn', views.signIn,name="signIn"),
       path('/signOut', views.signOut,name="singOut"),
       path('/signUp', views.signUp,name="signUp")
]