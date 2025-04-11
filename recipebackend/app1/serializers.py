from rest_framework import serializers
from django.contrib.auth.models import User
from app1.models import Recipe

from app1.models import Review


class RecipeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    image = serializers.ImageField(required=False)
    class Meta:
        model=Recipe
        fields=['id','r_name','r_ingredients','instruction','r_cusine','meal_type','image','image_url']

    def get_image_url(self,obj):
        request=self.context.get('request')
        photo_url=obj.image.url
        return request.build_absolute_uri(photo_url)

class UserSeializer(serializers.ModelSerializer):
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


class ReviewSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField('get_user')
    date=serializers.SerializerMethodField('get_date')
    class Meta:
        model=Review
        fields=['recipe','user','comment','rating','created','name','date']

    def get_user(self,obj):
        return obj.user.username

    def get_date(self,obj):
        return obj.created.date()
