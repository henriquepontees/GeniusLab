# admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Tipo de usuário")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'group')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.add(self.cleaned_data["group"])  # Adiciona o usuário ao grupo selecionado
        return user

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'group'),
        }),
    )

# Remover a inscrição original do UserAdmin e registrar a personalizada
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'editora', 'ano_publicacao', 'quantidade_total', 'quantidade_disponivel')

admin.site.register(Livro, LivroAdmin)
admin.site.register(Emprestimo)
admin.site.register(Devolucao)
