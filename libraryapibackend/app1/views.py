from django.shortcuts import render
from app1.models import Book
# Create your views here.
from app1.serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from app1.serializers import UserSeializer
from django.contrib.auth.models import User

class BookView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] #this view can only access by authenticated users
    queryset = Book.objects.all()
    serializer_class = BookSerializer
from django.db.models import Q
from rest_framework import status
class Booksearch(APIView):
    def get(self,request):
        query=self.request.query_params.get('search') #read keyword from search request params
        if query:
            b=Book.objects.filter(Q(title__icontains=query)|Q(author__icontains=query))
            if not b.exists(): # if queyset not exists
                return Response({'msg':'no results'},status=status.HTTP_200_OK)
            books=BookSerializer(b,many=True,context={'request':request})
            return Response(books.data,status=status.HTTP_200_OK)
        else: # if keyword is empty
            return Response({'msg': 'no results'}, status=status.HTTP_200_OK)


#Filter by title
class Filterbytitle(APIView):
    def get(self,request):
        query=self.request.query_params.get('search') #read keyword from search request params
        if query:
            b=Book.objects.filter(title__icontains=query)
            if not b.exists(): # if queyset not exists
                return Response({'msg':'no results'},status=status.HTTP_200_OK)
            books=BookSerializer(b,many=True)
            return Response(books.data,status=status.HTTP_200_OK)
        else: # if keyword is empty
            return Response({'msg': 'no results'}, status=status.HTTP_200_OK)


#Filter by author
class Filterbyauthor(APIView):
    def get(self,request):
        query=self.request.query_params.get('search') #read keyword from search request params
        if query:
            b=Book.objects.filter(author__icontains=query)
            if not b.exists(): # if queyset not exists
                return Response({'msg':'no results'},status=status.HTTP_200_OK)
            books=BookSerializer(b,many=True)
            return Response(books.data,status=status.HTTP_200_OK)
        else: # if keyword is empty
            return Response({'msg': 'no results'}, status=status.HTTP_200_OK)

class Userview(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSeializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        self.request.user.auth_token.delete()  #to delete the token of current user who is logged in and token is deleted from backend table
        return Response({'msg':'Logout Successfully'},status=status.HTTP_200_OK)


