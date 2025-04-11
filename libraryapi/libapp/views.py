from lib2to3.fixes.fix_input import context

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status

from libapp.models import Book

from libapp.serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from libapp.serializers import UserSerializer


# Create your views here.

class BookView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class SearchBooks(APIView):
    def get(self,request):
        query=self.request.query_params.get('search')
        if query:
            b=Book.objects.filter(Q(title__icontains=query)|Q(author__icontains=query))
            if not b.exists():
                return Response({'msg':'no results found'},status=status.HTTP_200_OK)
            books=BookSerializer(b,many=True,context={'request':request})
            return Response(books.data,status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'no results found'}, status=status.HTTP_200_OK)

#filter by title

class Filterbytitle(APIView):
    def get(self,request):
        query=self.request.query_params.get('title')
        if query:
            b=Book.objects.filter(title__icontains=query)
            if not b.exists():
                return Response({'msg':'no results found'},status=status.HTTP_200_OK)
            books=BookSerializer(b,many=True)
            return Response(books.data,status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'no results found'}, status=status.HTTP_200_OK)

#filter by author

class Filterbyauthor(APIView):
    def get(self,request):
        query=self.request.query_params.get('author')
        if query:
            b=Book.objects.filter(author__icontains=query)
            if not b.exists():
                return Response({'msg':'no results found'},status=status.HTTP_200_OK)
            books=BookSerializer(b,many=True)
            return Response(books.data,status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'no results found'}, status=status.HTTP_200_OK)

#AUTHENTICATION
#Register
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        self.request.user.auth_token.delete()
        return Response({"msg":"Logout Successfully"},status=status.HTTP_200_OK)