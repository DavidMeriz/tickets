from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import os


def user_unicode(self):

    return f'{self.last_name}, {self.first_name}'

User.__unicode__ = user_unicode 

# Ticket model 
class Ticket(models.Model):
    title = models.CharField('Título', max_length=255)

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='owner',
        blank=True,
        null=True,
        verbose_name='Propietario'
    )

    description = models.TextField('Descripción', blank=True, null=True)

    STATUS_CHOICES = [
            
        ('IN PROGRESS', 'EN PROGRESO'),
        ('WAITING', 'EN ESPERA'),
        ('DONE', 'FINALIZADO'),
    ]

    status = models.CharField(
        'Estado',
        choices=STATUS_CHOICES,
        max_length=255,
        blank=True,
        null=True,
    )

    waiting_for = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='waiting_for',
        blank=True,
        null=True,
        verbose_name='Ayudante'
    )

    closed_date = models.DateTimeField(blank=True, null=True)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='assigned_to',
        blank=True,
        null=True,
        verbose_name='Asignado a'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# FollowUp model o Seguimiento de Ticket
class FollowUp(models.Model):
    """
    A FollowUp is a comment to a ticket.
    """
    ticket = models.ForeignKey(Ticket, verbose_name='Ticket', on_delete=models.CASCADE)
    date = models.DateTimeField('Fecha', default=timezone.now)
    title = models.CharField('Titulo', max_length=200)
    text = models.TextField('Texto', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='Usuario', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified']


# Helper for attachment file path o archivo adjunto
def attachment_path(instance, filename):

    relative_dir = f'tickets/{instance.ticket.id}'
    absolute_dir = os.path.join(settings.MEDIA_ROOT, relative_dir)

    # Ensure the directory exists
    os.makedirs(absolute_dir, 0o777, exist_ok=True)

    return os.path.join(relative_dir, filename)

 
# Attachment model o Adjunto de Ticket
class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, verbose_name='Ticket', on_delete=models.CASCADE)
    file = models.FileField('File', upload_to=attachment_path, max_length=1000)
    filename = models.CharField('Filename', max_length=1000)
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='Usuario', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Adjunto'
        verbose_name_plural = 'Adjuntos'