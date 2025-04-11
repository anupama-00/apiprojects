from django.contrib.auth.models import User
from django.template.context_processors import request
from rest_framework import serializers

from libapp.models import Book


class BookSerializer(serializers.ModelSerializer):
    image_url=serializers.SerializerMethodField('get_image_url')
    image=serializers.ImageField(required=False)
    class Meta:
        model=Book
        fields='__all__'

    def get_image_url(self,obj):
        request =self.context.get('request')
        photo_url=obj.image.url
        return request.build_absolute_uri(photo_url)

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']

    def create(self, validated_data):
        u=User.objects.create_user(username=validated_data['username'],password=validated_data['password'],
                                   email=validated_data['email'],first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'])
        return u
