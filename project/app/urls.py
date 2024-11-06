from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('livros/', lista_livros, name='lista_livros'),
    path('solicitar-emprestimo/<int:livro_id>/', solicitar_emprestimo, name='solicitar_emprestimo'),
    path('', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('relatorio/', relatorio_emprestimos, name='relatorio_emprestimos'),
]
