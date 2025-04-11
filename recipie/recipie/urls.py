"""
URL configuration for recipie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from recipeapp import views
from rest_framework.authtoken import views as view1
router=SimpleRouter()
router.register('user',views.UserView)
router.register('recipe',views.RecipeView)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('login/',view1.obtain_auth_token),
    path('logout/',views.LogoutUser.as_view()),
    path('search/',views.SearchRecipe.as_view()),
    path('title/',views.Filterbytitle.as_view()),
    path('mealtype/',views.Filterbymealtype.as_view()),
    path('cuisine/',views.Filterbycuisine.as_view()),
    path('review/',views.CreateReview.as_view()),
    path('read/<int:pk>',views.ReadReview.as_view()),
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)