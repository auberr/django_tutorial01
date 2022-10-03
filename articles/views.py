from urllib import request
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed # Reply, Like, Bookmark
import os
from config.settings import MEDIA_ROOT
from user.models import User


# Create your views here.
class Main(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, 'login.html')    

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'login.html')    

        feed_object_list = Feed.objects.all().order_by('-id')
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            # reply_object_list = Reply.objects.filter(feed_id=feed.id)
            # reply_list = []
            # for reply in reply_object_list:
            #     user = User.objects.filter(email=reply.email).first()
            #     reply_list.append(dict(feed_id=reply.feed_id,
            #                             reply_content=reply.reply_content,
            #                             nickname=user.nickname))

            feed_list.append(dict(image=feed.image,
                                content=feed.content,
                                # like_count=feed.like_count,
                                profile_image=user.profile_img,
                                nickname=user.nickname,
                                # reply_list=reply_list
                                ))

        # for feed in feed_list:
        #     print(feed.content)

        return render(request, "main.html", context=dict(feed_list=feed_list, user=user))

    def post(self, request):
        print("포스트로 호출")
        return render(request, "main.html")


class UploadFeed(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image= uuid_name
        content = request.data.get('content')
        email = request.session.get('email', None)
        

        Feed.objects.create(image=image, content=content, email=email, like_count=0)

        return Response(status=200)

class Profile(APIView):
    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, 'login.html')    

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'login.html')    

        return render(request, 'profile.html', context=dict(user=user))


# class UploadReply(APIView):
#     def post(self, request):
#         feed_id = request.session.get('feed_id', None)
#         reply_content = request.session.get('feed_id', None)

#         email = request.session.get('email', None)

#         Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

#         return Response(status=200)
