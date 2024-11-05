from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

@receiver(post_save, sender=User)
def adicionar_grupo_e_permissoes(sender, instance, created, **kwargs):
    if created:
        grupo_administrador, _ = Group.objects.get_or_create(name='Administrador')

        if grupo_administrador not in instance.groups.all():
            instance.groups.add(grupo_administrador)

        instance.is_staff = True
        instance.save()
