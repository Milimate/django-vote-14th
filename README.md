# 🪐MyPlanIt🪐



## [🌒API 명세서](https://www.notion.so/CEOS-15-App-950479e6f0b84cefad5735d7c2d8e250)



## 🌓ERD
![erd](https://user-images.githubusercontent.com/80563849/147400579-9ca281df-ccb3-45a4-a3d1-adde2169ae80.png)


## 수진 - 로그인, 투표 기능 담당

## <로그인>
-> JWT를 이용한 로그인 기능 구현

( notion에서 django의 simpleJWT를 쓰라고 했는데, django의 PyJWT를 써서 구현했습니다.   
  이후 리팩토링때, simpleJWT를 이용하여 구현하겠습니다.)   

```python
# 로그인 GET, POST
class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('존재하지 않는 username입니다.')

        if check_password(password, user.password):
            raise AuthenticationFailed('비밀번호가 틀렸습니다.')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, env('DJANGO_SECRET_KEY'), algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError or jwt.Invalidtokenerror:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user).data
        return Response(serializer)

    
# 로그아웃
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return 
```

jwt의 payload에는 **id, exp, iat** 정도만을 담았고,   
* exp: 토큰의 만료시간 (1시간으로 잡음)
* iat: 토큰이 발급된 시간

이 payload를 HS256 해쉬 알고리즘을 이용하여 인코드하였고,
쿠키를 생성하도록 하고, 쿠키에 토큰을 넣어 클라이언트에 전달하도록 하였습니다.   
쿠키를 정보 전송수단으로 이용하는 것입니다.


간단히 토큰 하나만을 발급하여 설정하였는데,    
이후 추가 리팩토링때는 access token과 refresh token 두 개를 만들어서 로그인기능을 좀 더 다듬겠습니다.


## <투표>
- 로그인 한 유저는 투표 조회 가능 + 투표 가능   
- 로그인 하지 않은 유저는 투표 조회만 가능(투표는 불가능)

```python
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
        except jwt.ExpiredSignatureError or jwt.Invalidtokenerror:
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
```


## 수경 - 회원가입 기능 담당

## <회원가입>



```python
# 회원가입 POST view

class SignupView(ListCreateAPIView):
    create_queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        newUser = serializer.save()

        return Response(
            {
                "user": UserSerializer(newUser, context=self.get_serializer_context()).data,
            }
        )
```



```python
# serializer

from rest_framework import serializers
from django.apps import apps
User = apps.get_model('login', 'User')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {"password": {"write_only": True}}

        def create(self, validated_data):
            vote_user = User.objects.create_user(
                validated_data["username"], validated_data["email"], validated_data["password"]
            )

            return vote_user
```
