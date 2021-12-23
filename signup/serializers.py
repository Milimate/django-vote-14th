from rest_framework import serializers
from signup.models import User

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