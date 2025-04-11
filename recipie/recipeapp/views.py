
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets, status

from recipeapp.serializer import UserSerializer

from recipeapp.models import Recipe

from recipeapp.serializer import RecipeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipeapp.models import Review
from recipeapp.serializer import ReviewSerializer


# Create your views here.


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RecipeView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer



class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        self.request.user.auth_token.delete()
        return Response({'msg':'Logged out successfully'},status=status.HTTP_200_OK)


class SearchRecipe(APIView):
    def get(self,request):
        query=self.request.query_params.get('search')
        print(query)
        if query:
            r=Recipe.objects.filter(Q(recipe_name__icontains=query)|Q(recipe_ingredient__icontains=query)|Q(instructions__icontains=query)|Q(recipe_cuisine__icontains=query)|Q(meal_type__icontains=query))
            print(r)
            if not r.exists():
                return Response({'msg':'no results found'},status=status.HTTP_200_OK)
            recipe=RecipeSerializer(r,many=True,context={'request':request})
            return Response(recipe.data,status=status.HTTP_200_OK)
        else:
            return Response({'msg':'no results found'},status=status.HTTP_200_OK)

class Filterbytitle(APIView):
    def get(self,request):
        query=self.request.query_params.get('search')
        if query:
            r=Recipe.objects.filter(recipe_name__icontains=query)
            if not r.exists():
                return Response({'msg':'no results found'},status=status.HTTP_200_OK)
            recipe=RecipeSerializer(r,many=True)
            return Response(recipe.data,status=status.HTTP_200_OK)
        else:
            return Response({'msg':'no results found'},status=status.HTTP_200_OK)

class Filterbymealtype(APIView):
    def get(self,request):
        query=self.request.query_params.get('search')
        if query:
            r=Recipe.objects.filter(meal_type__icontains=query)
            if not r.exists():
                return Response({'msg':'no results found'},status=status.HTTP_200_OK)
            recipe=RecipeSerializer(r,many=True)
            return Response(recipe.data,status=status.HTTP_200_OK)
        else:
            return Response({'msg':'no results found'},status=status.HTTP_200_OK)

class Filterbycuisine(APIView):
    def get(self,request):
        query=self.request.query_params.get('search')
        if query:
            r=Recipe.objects.filter(recipe_ingredient__icontains=query)
            if not r.exists():
                return Response({'msg':'no results found'},status=status.HTTP_200_OK)
            recipe=RecipeSerializer(r,many=True)
            return Response(recipe.data,status=status.HTTP_200_OK)
        else:
            return Response({'msg':'no results found'},status=status.HTTP_200_OK)

class CreateReview(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        id=request.data['id']
        comment=request.data['comments']
        r=request.data['rating']
        u=self.request.user
        recipe=Recipe.objects.get(id=id)
        rev=Review.objects.create(user=u,recipe=recipe,comments=comment,rating=r)
        rev.save()
        review=ReviewSerializer(rev)
        return Response(review.data,status=status.HTTP_201_CREATED)

class ReadReview(APIView):
    def get_object(self,pk):
        try:
            return Recipe.objects.get(id=pk)
        except:
            raise Http404
    def get(self,request,pk):
        r=self.get_object(pk)
        rev=Review.objects.filter(recipe=r)
        review=ReviewSerializer(rev,many=True)
        return Response(review.data,status=status.HTTP_200_OK)





