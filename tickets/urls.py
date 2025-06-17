# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, include

import main.views as views   # alias for brevity

urlpatterns = [
    # ────────────── Authentication ──────────────
    path(
        "",                                              # /
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    # Optional: password-reset, change-password, etc.
    path("accounts/", include("django.contrib.auth.urls")),

    # ─────────────── User settings ───────────────
    path("settings/", login_required(views.usersettings_update_view),
         name="user-settings"),

    # ───────────────── Django admin ──────────────
    path("admin/", admin.site.urls),

    # ─────────────────── Tickets ──────────────────
    path("ticket/new/",        login_required(views.ticket_create_view), name="ticket_new"),
    path("ticket/edit/<int:pk>/",  login_required(views.ticket_edit_view),   name="ticket_edit"),
    path("ticket/<int:pk>/",   login_required(views.ticket_detail_view), name="ticket_detail"),

    # ────────────────── Follow-Ups ────────────────
    path("followup/new/",      login_required(views.followup_create_view), name="followup_new"),
    path("followup/edit/<int:pk>/", login_required(views.followup_edit_view), name="followup_edit"),

    # ───────────────── Attachments ────────────────
    path("attachment/new/",    login_required(views.attachment_create_view), name="attachment_new"),

    # ─────────────────── Overviews ────────────────
    path("inbox/",        login_required(views.inbox_view),       name="inbox"),
    path("my-tickets/",   login_required(views.my_tickets_view),  name="my-tickets"),
    path("all-tickets/",  login_required(views.all_tickets_view), name="all-tickets"),
    path("archive/",      login_required(views.archive_view),     name="archive"),
]

# ────────────── Static/Media in development ──────────────
if settings.DEBUG:          # only when DEBUG = True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
