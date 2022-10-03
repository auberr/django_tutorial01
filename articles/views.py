from urllib import request
from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed, Reply, Like, Bookmark
import os
from config.settings import MEDIA_ROOT
from user.models import User


# Create your views here.
class Main(APIView):
    def get(self, request):
        email = request.session.get('email')
        print(email)

        if email is None:
            return render(request, 'login.html')    

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, 'login.html')    

        feed_object_list = Feed.objects.all().order_by('-id')
        feed_list = []

        for feed in feed_object_list:
            user = User.objects.get(email=feed.email)
            print(email)
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(feed_id=reply.feed_id,
                                        reply_content=reply.reply_content,
                                        nickname=user.nickname))
            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked=Like.objects.filter(feed_id=feed.id, email=email, is_like=True).exists()
            feed_list.append(dict(id=feed.id,
                                image=feed.image,
                                content=feed.content,
                                like_count=like_count,
                                profile_image=user.profile_img,
                                nickname=user.nickname,
                                reply_list=reply_list,
                                is_liked=is_liked
                                ))
            print(email)

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
        email = request.session.get('email')
        

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


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)

        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id, reply_content=reply_content, email=email)

        return Response(status=200)


class ToggleLike(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        favorite_text = request.data.get('favorite_text', True)

        if favorite_text == 'favorite_border':
            is_like = True
        else:
            is_like = False

        email = request.session.get('email', None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id, is_like=is_like, email=email)

        return Response(status=200)
