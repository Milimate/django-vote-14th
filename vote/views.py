from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Candidate
from django.db import models
from .serializers import CandidateSerializer
import jwt
import os, environ
from django.apps import apps
User = apps.get_model('login', 'User')

# .env 파일 가져오기
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
env = environ.Env(
    DEBUG=(bool, False)
)

# Create your views here.


# 투표화면 GET, POST
class VoteView(APIView):
    def get(self, request):
        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('로그인을 해야 투표를 할 수 있습니다.') # 예외처리1:  로그인 안 한 유저인 경우

        try:
            payload = jwt.decode(token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated') # 예외처리2: 유효성 검사 오류

        user = User.objects.get(id=payload['id'])

        if not user:
            raise AuthenticationFailed('Unauthenticated') # 예외처리3: 유저가 db에 없는 경우

        candidate = Candidate.objects.get(id=request.data) # request로 후보자 id를 전달받아서 이를 처리
        candidate.vote_count += 1
        candidate.save()

        candidates = Candidate.objects.all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)
