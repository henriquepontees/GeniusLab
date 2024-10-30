# biblioteca/views.py
from django.views.generic import ListView
from .models import *

class LivrosDisponiveisListView(ListView):
    model = Livro
    template_name = "app/livros_disponiveis_list.html"
    context_object_name = "livros"
    
    def get_queryset(self):
        # Filtra apenas os livros que estão disponíveis
        return Livro.objects.filter(quantidade_disponivel__gt=0)
