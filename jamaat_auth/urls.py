from django.urls import path
from . import views


urlpatterns = [
    path('generate_jamaat_user', views.CustomJamaatUserAPIVIew.as_view(), name='generate-jamaat-user'),
    path('login', views.CustomJamaatUserLoginAPIView.as_view(), name='login-jamaat-user'),


    path('jamaat_login', views.ATJamaatAdminLogin.as_view(), name='template-jamaat-login')

]