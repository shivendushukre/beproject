from django.urls import path
from .views import *

urlpatterns = [
    path('upload/',PaperUploadView,name='home'),
    path('',login,name='login'),
    # path('summary/', summary, name='summary')
    path('signup/',singup, name='signup')
]