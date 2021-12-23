from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import SignupSerializer, UserSerializer

from django.apps import apps
User = apps.get_model('login', 'User')


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
