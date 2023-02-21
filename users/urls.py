from django.urls import path

from . import views

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('login', views.LoginProfileView.as_view(), name='login'),
    path('logout', views.LogoutProfileView.as_view(), name='logout'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('cart', views.BasketView.as_view(), name='cart'),
    path('verify/<str:email>/<uuid:code>', views.VerifyView.as_view(), name='verify'),
]
