from django.urls import path
from auth_user import views

urlpatterns = [
    path('/signIn', views.signIn, name="signIn"),
    path('/signOut', views.signOut, name="signOut"),
    path('/signUp', views.signUp, name="signUp"),
    path('/activate/<uidb64>/<token>/', views.activate, name='activate'),
]
