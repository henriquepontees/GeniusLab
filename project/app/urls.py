from django.urls import path
from .views import LivrosDisponiveisListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("livros-disponiveis/", LivrosDisponiveisListView.as_view(), name="livros_disponiveis"),
    path('', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
