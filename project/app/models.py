from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError

class Livro(models.Model):
    GENEROS = [
        ('Ficção', 'Ficção'),
        ('Não-Ficção', 'Não-Ficção'),
        ('Romance', 'Romance'),
        ('Ciência', 'Ciência'),
    ]

    titulo = models.CharField("Título do Livro", max_length=255)
    autor = models.CharField("Autor", max_length=255)
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    editora = models.CharField("Editora", max_length=255)
    ano_publicacao = models.PositiveIntegerField("Ano de Publicação")
    genero = models.CharField("Gênero", max_length=20, choices=GENEROS)
    quantidade_total = models.PositiveIntegerField("Quantidade Total")
    quantidade_disponivel = models.PositiveIntegerField("Quantidade Disponível")
    descricao = models.TextField("Descrição", blank=True, null=True)
    ativo = models.BooleanField("Ativo", default=True)

    def pode_ser_emprestado(self):
        return self.quantidade_disponivel > 0 and self.ativo

    def save(self, *args, **kwargs):
        if self.quantidade_disponivel > self.quantidade_total:
            self.quantidade_disponivel = self.quantidade_total
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
        ('CONCLUIDO', 'Concluído'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, verbose_name="Livro")
    data_emprestimo = models.DateField(null=True, blank=True, verbose_name="Data do Empréstimo")
    data_devolucao_prevista = models.DateField(null=True, blank=True, verbose_name="Data de Devolução Prevista")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE', verbose_name="Status do Empréstimo")

    def save(self, *args, **kwargs):
        # Verifica se o empréstimo é novo e está pendente
        if self.pk is None and self.status == 'PENDENTE':
            if not self.livro.pode_ser_emprestado():
                raise ValidationError("O livro não está disponível para empréstimo.")
        super().save(*args, **kwargs)

    def aprovar_emprestimo(self):
        # Aprova o empréstimo usando a data de devolução prevista informada
        if self.status == 'PENDENTE':
            self.status = 'APROVADO'
            self.data_emprestimo = date.today()
            if not self.data_devolucao_prevista:
                raise ValidationError("A data de devolução prevista é obrigatória para aprovar o empréstimo.")
            self.livro.quantidade_disponivel -= 1
            self.livro.save()
            self.save()

    def rejeitar_emprestimo(self):
        if self.status == 'PENDENTE':
            self.status = 'REJEITADO'
            self.save()

    def concluir_emprestimo(self):
        if self.status == 'APROVADO':
            self.status = 'CONCLUIDO'
            self.livro.quantidade_disponivel += 1
            self.livro.save()
            self.save()

    class Meta:
        verbose_name_plural = "Adicionar Empréstimo"

    def __str__(self):
        return f"Empréstimo de {self.livro} para {self.usuario}"


class Devolucao(models.Model):
    emprestimo = models.OneToOneField(
        Emprestimo,
        on_delete=models.CASCADE,
        verbose_name="Empréstimo",
        limit_choices_to={'status': 'EM_ABERTO'}
    )
    data_devolucao = models.DateField(default=date.today, verbose_name="Data de Devolução")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        verbose_name_plural = "Devolver Empréstimo"

    def __str__(self):
        return f"Devolução do empréstimo ID {self.emprestimo.id} para o livro '{self.emprestimo.livro}'"

    def save(self, *args, **kwargs):
        # Registra a devolução, conclui o empréstimo e atualiza a disponibilidade do livro
        if self.emprestimo.status == 'EM_ABERTO':
            self.emprestimo.concluir_emprestimo()
        super().save(*args, **kwargs)
