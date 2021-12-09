from functools import wraps
from django.http import HttpResponse
from .helpers import verifytoken
from .models import User

def protected_route(function):
  @wraps(function)
  def wrap(slf,request, *args, **kwargs):
        #decorator function to intercept the request on protected routes
        data = verifytoken(request.headers.get('Authorization')[7:])
        if data is not None:
            try:
                user = User.objects.get(user = data['user'])
                if user is None:
                    return HttpResponse("Not authorized",status=401)
                else:
                    return function(slf,request, user)
            except Exception as e:
                print(e)
                return HttpResponse("Not authorized",status=401)
        else:
            return HttpResponse("Not authorized",status=401)
  return wrap