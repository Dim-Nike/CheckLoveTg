import random

from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseNotFound
from .models import *

# from ...bot_shopp.handlers.users.backend import USER_LINK

user_id = 1


class ApplicationSerializator(serializers.ModelSerializer):
    class Meta:
        model = OrderUser
        fields = '__all__'


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


class GetPerson(APIView):
    def get(self, *args, **kwargs):
        Order = OrderUser.objects.all()
        print(12342423423)
        random_order = random.choice(Order)
        serialized_order_user = ApplicationSerializator(random_order, many=False)
        return Response(serialized_order_user.data)

    def post(self, req):
        new_post = OrderUser.objects.create(
            id_user=req.data['id_user'],
            id_tg=req.data['id_tg'],
            data_start=req.data['data_start'],
            data_end=req.data['data_end'],
        )

        return Response({'post': model_to_dict(new_post)})


class PostResult(APIView):
    def get(self, *args, **kwargs):
        pass

    def post(self, req):
        new_result = 1

        return Response({'post': new_result})

class GetOneUser(APIView):
    def get(self, req, pk, *args, **kwargs):
        all_app = ApplicationUser.objects.filter(pk__gt=pk - 1).first()
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
