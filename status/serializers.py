from rest_framework import serializers
from django.contrib.auth.models import User
from status.models import Status
from datetime import datetime


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password','email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField(many=True, read_only=True)
    no_of_status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'status', 'no_of_status']
    
    def get_no_of_status(self, object):
        return object.status.count()


class StatusSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Status
        fields = ['id', 'title', 'body', 'owner']