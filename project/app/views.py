# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Livro, Emprestimo

@login_required
def lista_livros(request):
    livros_disponiveis = Livro.objects.filter(ativo=True, quantidade_disponivel__gt=0)
    return render(request, 'app/lista_livros.html', {'livros': livros_disponiveis})

def solicitar_emprestimo(request, livro_id):
    livro = Livro.objects.get(id=livro_id)
    if livro.pode_ser_emprestado():
        data_emprestimo = timezone.now().date()
        data_devolucao_prevista = data_emprestimo + timedelta(days=14)

        emprestimo = Emprestimo.objects.create(
            usuario=request.user,
            livro=livro,
            status='PENDENTE',
            data_emprestimo=data_emprestimo,
            data_devolucao_prevista=data_devolucao_prevista
        )
        livro.quantidade_disponivel -= 1
        livro.save()
        messages.success(request, f"Empréstimo do livro '{livro.titulo}' solicitado com sucesso! Devolução prevista para {data_devolucao_prevista}.")
    else:
        messages.error(request, "Não foi possível solicitar o empréstimo, o livro não está disponível.")
    return redirect('lista_livros')