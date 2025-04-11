from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from rest_framework import viewsets
from app1.models import Recipe
from app1.serializers import RecipeSerializer

from django.contrib.auth.models import User
from app1.serializers import UserSeializer
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app1.serializers import ReviewSerializer


# Create your views here.

class RecipeView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset=Recipe.objects.all()
    serializer_class=RecipeSerializer

class Userview(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSeializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        self.request.user.auth_token.delete() 
        return Response({'msg':'Logout Successfully'},status=status.HTTP_200_OK)

from django.db.models import Q
class Recipesearch(APIView):
    def get(self,request):
        query=self.request.query_params.get('search') #read keyword from search request params
        if query:
            b=Recipe.objects.filter(Q(r_name__icontains=query)|Q(r_cusine__icontains=query))
            if not b.exists(): # if queyset not exists
                return Response({'msg':'no results'},status=status.HTTP_200_OK)
            recipe=RecipeSerializer(b,many=True,context={'request':request})
            return Response(recipe.data,status=status.HTTP_200_OK)
        else: # if keyword is empty
            return Response({'msg': 'no results'}, status=status.HTTP_200_OK)

class Filterbycusine(APIView):
    def get(self,request):
        query=self.request.query_params.get('search') #read keyword from search request params
        if query:
            b=Recipe.objects.filter(r_cusine__icontains=query)
            if not b.exists(): # if queyset not exists
                return Response({'msg':'no results'},status=status.HTTP_200_OK)
            recipe=RecipeSerializer(b,many=True)
            return Response(recipe.data,status=status.HTTP_200_OK)
        else: # if keyword is empty
            return Response({'msg': 'no results'}, status=status.HTTP_200_OK)

class Filterbymealtype(APIView):
    def get(self,request):
        query=self.request.query_params.get('search') #read keyword from search request params
        if query:
            b=Recipe.objects.filter(meal_type__icontains=query)
            if not b.exists(): # if queyset not exists
                return Response({'msg':'no results'},status=status.HTTP_200_OK)
            recipe=RecipeSerializer(b,many=True)
            return Response(recipe.data,status=status.HTTP_200_OK)
        else: # if keyword is empty
            return Response({'msg': 'no results'}, status=status.HTTP_200_OK)
class Filterbying(APIView):
    def get(self,request):
        query=self.request.query_params.get('search') #read keyword from search request params
        if query:
            b=Recipe.objects.filter(r_ingredients__icontains=query)
            if not b.exists(): # if queyset not exists
                return Response({'msg':'no results'},status=status.HTTP_200_OK)
            recipe=RecipeSerializer(b,many=True)
            return Response(recipe.data,status=status.HTTP_200_OK)
        else: # if keyword is empty
            return Response({'msg': 'no results'}, status=status.HTTP_200_OK)

from app1.models import Review
class CreateReview(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        id=request.data.get('id')
        user=self.request.user
        comment=request.data['comment']
        rating=request.data['rating']


        r=Recipe.objects.get(id=id)
        rev=Review.objects.create(recipe=r,user=user,comment=comment,rating=rating)
        rev.save()
        recipe=ReviewSerializer(rev)
        return Response(recipe.data,status=status.HTTP_201_CREATED)


from django.http import Http404

class RecipeReview(APIView):
    def get_object(self,pk):
        try:
            return Recipe.objects.get(pk=pk)
        except:
            raise Http404
    def get(self,request,pk):
        r=self.get_object(pk)
        rev=Review.objects.filter(recipe=r)
        review=ReviewSerializer(rev,many=True)
        return Response(review.data,status=status.HTTP_200_OK)