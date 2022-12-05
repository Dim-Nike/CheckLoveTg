import random

from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseNotFound
from .models import *


class ApplicationSerializator(serializers.ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = ['id_user', 'link_user', 'name']


class AppResultSerializator(serializers.ModelSerializer):
    class Meta:
        model = AppResult
        fields = ['lover', 'friend_best', 'number_app']


class GetUser(APIView):
    def get(self, *args, **kwargs):
        all_applications = ApplicationUser.objects.all()
        random_app = random.choice(all_applications)
        serialized_random_app = ApplicationSerializator(random_app, many=False)
        return Response(serialized_random_app.data)


class GetOneUser(APIView):
    def get(self, req, pk, *args, **kwargs):
        all_app = ApplicationUser.objects.filter(pk__gt=pk-1).first()
        if not all_app:
            return HttpResponseNotFound()
        serial_app = ApplicationSerializator(all_app, many=False)
        return Response(serial_app.data)


class GetResult(APIView):
    def get(self, req, pk, *args, **kwargs):
        all_app = ApplicationUser.objects.filter(pk__gt=pk).first()
        print(all_app.result.lover)
        if not all_app:
            return HttpResponseNotFound()
        serial_resultApp = AppResultSerializator(all_app.result, many=False)
        return Response(serial_resultApp.data)