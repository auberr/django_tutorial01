from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', Main.as_view()),
]
