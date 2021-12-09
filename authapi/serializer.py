from rest_framework import serializers

from .models import User,UserLoginHistory


class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = (
      'id',
      'user',
      'password',
      'service'
    )

class UserHistorySerializer(serializers.ModelSerializer):

  class Meta:
    model = UserLoginHistory
    fields = (
      'id',
      'user',
      'last_login'
    )