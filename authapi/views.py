
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from .helpers import get_hashed_password, check_password, generatetoken, verifytoken
from .serializer import UserSerializer, UserHistorySerializer
from .tokenVerifier import protected_route
#from .config import CLIENT_SECRET, GOOGLE_CLIENT_ID
import requests

import csv

from .models import User, UserLoginHistory


class Signup(
  APIView, # Basic View class provided by the Django Rest Framework
  UpdateModelMixin, # Mixin that allows the basic APIView to handle PUT HTTP requests
  DestroyModelMixin, # Mixin that allows the basic APIView to handle DELETE HTTP requests
):

  def post(self, request):

    keys = request.data.keys()
    if 'service' not in keys:
        return HttpResponse('More parameters required', status=400)
    if(request.data['service'] == 'app'):
        if 'user' not in keys or 'password' not in keys:
            return HttpResponse('More parameters required', status=400)
        try:
            user = User.objects.get(user = request.data['user'])
        except Exception as e:
            user = None
        if user is None:
            hashedpass = get_hashed_password(request.data['password'])
            user = User(user = request.data['user'], password = hashedpass, service='app')
            user.save()
            data = {"token":generatetoken({"user":request.data['user']})}
            return Response(data)
        else:
            return HttpResponse('User already exist',status=400)
    else:
        return HttpResponse('More parameters required', status=400)

    # Pass JSON data from user POST request to serializer for validation
    # create_serializer = TodoSerializer(data=request.data)

    # # Check if user POST data passes validation checks from serializer
    # if create_serializer.is_valid():

    #   # If user data is valid, create a new todo item record in the database
    #   todo_item_object = create_serializer.save()

    #   # Serialize the new todo item from a Python object to JSON format
    #   read_serializer = TodoSerializer(todo_item_object)

    #   # Return a HTTP response with the newly created todo item data
    #   return Response(read_serializer.data, status=201)

    # # If the users POST data is not valid, return a 400 response with an error message
    # return Response(create_serializer.errors, status=400)

class Signin(
  APIView, # Basic View class provided by the Django Rest Framework
  UpdateModelMixin, # Mixin that allows the basic APIView to handle PUT HTTP requests
  DestroyModelMixin, # Mixin that allows the basic APIView to handle DELETE HTTP requests
):

  def post(self, request):
    # Pass JSON data from user POST request to serializer for validation
    
    keys = request.data.keys()
    if 'service' not in keys:
        return HttpResponse('More parameters required', status=400)
    if(request.data['service'] == 'app'):
        if 'user' not in keys or 'password' not in keys:
            return HttpResponse('More parameters required', status=400)
        try:
            user = User.objects.get(user = request.data['user'])
        except Exception as e:
            user = None

        if user is not None:
            if check_password(request.data['password'],UserSerializer(user)['password'].value):
                history = UserLoginHistory(user=request.data['user'])
                history.save()
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                print(ip)
                r = requests.post('https://encrusxqoan0b.x.pipedream.net/', data={'user': request.data['user'],'ip':ip})
                data = {"token":generatetoken({"user":request.data['user']})}
                return Response(data)
            else:
                return HttpResponse('Wrong password',status=401)
        else:
            return HttpResponse('Account does not exist',status=400)
    else:
        #did not work try later
        # if 'code' not in keys:
        #     return HttpResponse('More parameters required', status=400)
        # else:
        #     try:
        #         url = "https://oauth2.googleapis.com/token?code="+request.data['code']+"&client_id="+GOOGLE_CLIENT_ID+"&client_secret="+CLIENT_SECRET+"&access_type=offline&scope=&grant_type=authorization_code&redirect_uri=http://localhost:8000"
        #         resp = requests.post(url)
        #         print(url)
        #         print("respone is")
        #         print(resp.content)
        #         return Response('OK')
        #     except Exception as e:
        #         print(e)
        #         return HttpResponse('Unauthorize', status=401)
        #
        return Response("Aunathorize",status=401)


class GenerateCsv(
  APIView, # Basic View class provided by the Django Rest Framework
  UpdateModelMixin, # Mixin that allows the basic APIView to handle PUT HTTP requests
  DestroyModelMixin, # Mixin that allows the basic APIView to handle DELETE HTTP requests
):

  @protected_route
  def get(self, request, user):
    # API to get csv of report of loggedin user
    userserializer = UserSerializer(user)
    qs = UserLoginHistory.objects.filter(user = userserializer.data['user'])
    result = list(qs.values("user", "last_login")[:2])
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )
    print(result)
    writer = csv.writer(response)
    writer.writerow(('user','last_login'))
    for row in result:
        writer.writerow((row['user'],row['last_login']))
    return response

class Dummy(
  APIView, # Basic View class provided by the Django Rest Framework
  UpdateModelMixin, # Mixin that allows the basic APIView to handle PUT HTTP requests
  DestroyModelMixin, # Mixin that allows the basic APIView to handle DELETE HTTP requests
):

  @protected_route
  def get(self, request, user):
    #Dummy api to check token functionality
    return Response("Dummy Data From Server On Successfull authentication")

