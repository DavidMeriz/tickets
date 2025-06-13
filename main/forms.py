# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from .models import Ticket, FollowUp, Attachment


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description')
        labels = {
            'title': 'Título',
            'description': 'Descripción',
        }


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'owner', 'description', 'status', 'waiting_for', 'assigned_to')
        labels = {
            'title': 'Título',
            'owner': 'Propietario',
            'description': 'Descripción',
            'status': 'Estado',
            'waiting_for': 'Ayudante',
            'assigned_to': 'Asignado a',
        }


class FollowupForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ('ticket', 'title', 'text', 'user')
        labels = {
            'ticket': 'Ticket',
            'title': 'Título',
            'text': 'Texto',
            'user': 'Usuario',
        }


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('file',)
        labels = {
            'file': 'Archivo',
        }
