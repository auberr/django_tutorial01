from django.urls import path
from articles.views import UploadFeed, Main, Profile


urlpatterns = [
    path('upload', UploadFeed.as_view()),
    path('main/', Main.as_view()),
    path('profile/', Profile.as_view()),
]