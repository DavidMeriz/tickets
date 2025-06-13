# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import Ticket, Attachment, FollowUp
from .forms import UserSettingsForm, TicketCreateForm, TicketEditForm, FollowupForm, AttachmentForm

# Logging
import logging
logger = logging.getLogger(__name__)


def inbox_view(request):
    users = User.objects.all()
    tickets_unassigned = Ticket.objects.exclude(assigned_to__in=users)
    tickets_assigned = Ticket.objects.filter(assigned_to__in=users)

    context = {
        "tickets_assigned": tickets_assigned,
        "tickets_unassigned": tickets_unassigned,
    }
    return render(request, 'main/inbox.html', context)


def my_tickets_view(request):
    tickets = Ticket.objects.filter(assigned_to=request.user).exclude(status="DONE")
    tickets_waiting = Ticket.objects.filter(waiting_for=request.user, status="WAITING")

    context = {
        "tickets": tickets,
        "tickets_waiting": tickets_waiting,
    }
    return render(request, 'main/my-tickets.html', context)


def all_tickets_view(request):
    tickets_open = Ticket.objects.exclude(status="DONE")
    context = {"tickets": tickets_open}
    return render(request, 'main/all-tickets.html', context)


def archive_view(request):
    tickets_closed = Ticket.objects.filter(status="DONE")
    context = {"tickets": tickets_closed}
    return render(request, 'main/archive.html', context)


def usersettings_update_view(request):
    user = request.user

    if request.method == 'POST':
        form_user = UserSettingsForm(request.POST)
        if form_user.is_valid():
            user.first_name = form_user.cleaned_data['first_name']
            user.last_name = form_user.cleaned_data['last_name']
            user.save()
            return HttpResponseRedirect(request.GET.get('next', '/inbox/'))
    else:
        form_user = UserSettingsForm(instance=user)

    return render(request, 'main/settings.html', {'form_user': form_user})


def ticket_create_view(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.status = "TODO"
            obj.save()
            return redirect('inbox')
    else:
        form = TicketCreateForm()

    return render(request, 'main/ticket_edit.html', {'form': form})


def ticket_edit_view(request, pk):
    data = Ticket.objects.get(id=pk)
    if request.method == 'POST':
        form = TicketEditForm(request.POST, instance=data)
        if form.is_valid():
            if form.cleaned_data['status'] == "DONE":
                data.closed_date = timezone.now()
            form.save()
            return redirect('inbox')
    else:
        form = TicketEditForm(instance=data)

    return render(request, 'main/ticket_edit.html', {'form': form})


def ticket_detail_view(request, pk):
    ticket = Ticket.objects.get(id=pk)
    attachments = Attachment.objects.filter(ticket=ticket)
    followups = FollowUp.objects.filter(ticket=ticket)

    context = {
        'ticket': ticket,
        'attachments': attachments,
        'followups': followups,
    }
    return render(request, 'main/ticket_detail.html', context)


def followup_create_view(request):
    if request.method == 'POST':
        form = FollowupForm(request.POST)
        if form.is_valid():
            followup = form.save()
            ticket = followup.ticket
            subject = f"[#{ticket.id}] New followup"
            body = (
                f"Hi,\n\nnew followup created for ticket #{ticket.id} "
                f"(http://localhost:8000/ticket/{ticket.id}/)\n\n"
                f"Title: {followup.title}\n\n{followup.text}"
            )          
            return redirect('inbox')
    else:
        form = FollowupForm(initial={'ticket': request.GET.get('ticket'), 'user': request.user})

    return render(request, 'main/followup_edit.html', {'form': form})


def followup_edit_view(request, pk):
    data = FollowUp.objects.get(id=pk)
    if request.method == 'POST':
        form = FollowupForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('inbox')
    else:
        form = FollowupForm(instance=data)

    return render(request, 'main/followup_edit.html', {'form': form})


def attachment_create_view(request):
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = Ticket.objects.get(id=request.GET.get('ticket'))
            attachment = Attachment(
                ticket=ticket,
                file=request.FILES['file'],
                filename=request.FILES['file'].name,
                user=request.user
            )
            attachment.save()
            return redirect('inbox')
    else:
        form = AttachmentForm()

    return render(request, 'main/attachment_add.html', {'form': form})
