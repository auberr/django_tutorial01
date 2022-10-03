from django.urls import path
from user.views import Join, Login,LogOut, UploadProfile


urlpatterns = [
    path('join/', Join.as_view(), name='join'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('profile/upload', UploadProfile.as_view()),
]
