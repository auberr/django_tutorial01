from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from django.contrib.auth.hashers import make_password
import os
from uuid import uuid4
from config.settings import MEDIA_ROOT

# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, "join.html")

    def post(self, request):
        # Todo 회원가입
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email, nickname=nickname, name=name, password=make_password(password), profile_img="default_profile.jpg")

        return Response(status=200)

class Login(APIView):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        # 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            # 로그인을 했다. 세션 or 쿠키
            request.session['email'] = email
            # response = render(request, 'main.html')
            # response.set_cookie('email', email)
            # return response
            return render(request, 'main.html')

        else:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))


class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "login.html")


class UploadProfile(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']
        email = request.data.get('email')

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image= uuid_name
        
        user = User.objects.filter(email=email).first()

        user.profile_img = profile_image
        user.save()

        return Response(status=200)