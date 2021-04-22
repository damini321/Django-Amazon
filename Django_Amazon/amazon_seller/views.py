from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from user.models import User
from .utils import Unique_Name, Unique_Password
from django.core.exceptions import ObjectDoesNotExist
from Django_Amazon.settings import EMAIL_HOST_USER
import datetime
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File


class Amazon_Seller_Signup_View(generics.CreateAPIView):
    queryset = Amazon_Seller.objects.all()
    serializer_class = Amazon_Seller_Signup_Serializer

    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            unique_id = Unique_Name()
            unique_password = Unique_Password()
            user_query = User.objects.create_user(username=unique_id,
                                                  first_name=self.request.data['first_name'],
                                                  email=self.request.data['email'],
                                                  password=unique_password,
                                                  last_name=self.request.data["last_name"],
                                                  is_amazon_seller=True)
            seller_query = serializer.save(user=user_query, active=False, unique_id=unique_id,
                                           password=unique_password)
            try:
                qrcode_img = qrcode.make(self.request.data['first_name'] + "amazon_seller")
                canvas = Image.new('RGB', (290, 290), 'white')
                draw = ImageDraw.Draw(canvas)
                canvas.paste(qrcode_img)
                username = self.request.data['first_name']
                fname = f'amazon_code-{username}' + '.png'
                buffer = BytesIO()
                canvas.save(buffer, 'PNG')
                seller_query.qr_code.save(fname, File(buffer), save=True)
                canvas.close()
            except:
                pass
            Amazon_Seller_Notifications.seller_registered(self=self, amazon_seller=seller_query,
                                                          first_name=seller_query.first_name,
                                                          email=seller_query.email,
                                                          from_email=EMAIL_HOST_USER)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class Amazon_Seller_Notification_View(generics.ListAPIView):
    queryset = Amazon_Seller_Notifications.objects.all()
    serializer_class = Amazon_Seller_Notificartions_Serializer

    def list(self, request, *args, **kwargs):
        if self.request.user.is_amazon_admin:
            seller_query = Amazon_Seller.objects.get(user=self.request.user)
            if seller_query.active:
                query = Amazon_Seller_Notifications.objects.get(amazon_seller=seller_query)
                serializer = self.get_serializer(query, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"NO_ACCESS": "Access Denied"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=status.HTTP_401_UNAUTHORIZED)


class Manage_Amazon_Seller_List_View(generics.ListAPIView):
    queryset = Amazon_Seller.objects.all()
    serializer_class = Amazon_Seller_List_View_Serializer

    def list(self, request, *args, **kwargs):
        if self.request.user.is_amazon_admin:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=status.HTTP_401_UNAUTHORIZED)


class Manage_Amazon_Seller_Retrieve_View(generics.RetrieveAPIView):
    queryset = Amazon_Seller.objects.all()
    serializer_class = Amazon_Seller_Retrieve_View_Serializer

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            try:
                query = Amazon_Seller.objects.get(id=self.kwargs["id"])
                serializer = self.get_serializer(query)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"DOES_NOT_EXIST": "Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=status.HTTP_401_UNAUTHORIZED)
