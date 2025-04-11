from app1.models import Book
from rest_framework import serializers
from django.contrib.auth.models import User

class BookSerializer(serializers.ModelSerializer):

    image_url=serializers.SerializerMethodField('get_image_url')


    image=serializers.ImageField(required=False)
    class Meta:
        model=Book
        fields='__all__'  #id,age,place,name

    def get_image_url(self,obj):
        request=self.context.get('request')
        photo_url=obj.image.url
        return request.build_absolute_uri(photo_url)

class UserSeializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']
    def create(self, validated_data): #To validate data and covert password to encrypted values
        u=User.objects.create_user(username=validated_data['username'],
                                   password=validated_data['password'],
                                   email=validated_data['email'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'])
        return u