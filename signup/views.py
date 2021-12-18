from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from signup.models import User
from signup.serializers import SignupSerializer


@csrf_exempt
def signup_list(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

