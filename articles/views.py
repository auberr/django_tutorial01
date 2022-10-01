from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed

# Create your views here.
class Main(APIView):
    def get(self, reuqest):
        feed_list = Feed.objects.all()
        
        for feed in feed_list:
            print(feed.content)

        return render(reuqest, "main.html", context=dict(feed_list=feed_list))

    def post(self, request):
        print("포스트로 호출")
        return render(request, "main.html")

    