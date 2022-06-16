from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import * 
from django.contrib.auth.hashers import make_password


class UsercreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','password']    
    def create(self, validated_data):
            validated_data['password'] = make_password(validated_data['password'])
            return super(UsercreateSerializer, self).create(validated_data)
        
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=250)
    class Meta:
        model=User
        fields=['email','password']
        
        

class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','mobile','gender','company_name']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','first_name','last_name','mobile','gender','company_name']
        
class AddpostSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobPost
        fields=['HR','position','salary','addres','categories','job_description','experience','slot','type','city']

class EditpostSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobPost
        fields=['position','salary','addres','categories','job_description','experience','slot','type','city']
        
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Application
        fields='__all__'   
        
class  MyPostApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Application
        fields='__all__'