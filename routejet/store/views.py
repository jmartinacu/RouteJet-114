
from http.client import HTTPResponse
from django.views import View
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views




def product_list(request): 
    return HTTPResponse('Hello World')



