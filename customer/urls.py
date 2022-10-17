from django.urls import path
from .views import *
urlpatterns = [
    path('sign-up', registration),
    path('sign-in', auth),
    path('token', checkUserView.as_view()),

    path('proccess/sign-in', SignInView.as_view()),
    path('proccess/sign-up', SignUpView.as_view()),
    path('logout', LogOutView.as_view()),
    path('info', UserView.as_view())
]