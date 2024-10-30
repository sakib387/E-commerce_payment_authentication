from django.contrib import admin  # Import admin module
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("ecommerceapp.urls")),
]
