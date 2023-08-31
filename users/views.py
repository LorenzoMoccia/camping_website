# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from . import forms
from .models import Utente


class ManageSubaccounts(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Utente
    success_url = reverse_lazy('manage-SubAccounts')
    form_class = forms.CustomUserCreationForm
    template_name = 'users/utente_form.html'

    def get_success_message(self, cleaned_data):
        success_message = _(f"Utente: <strong>{self.object.email}</strong> creato con successo!")
        return success_message


class UserListView(ListView):
    model = Utente
    template_name = 'users/utente_form.html'

    def get_queryset(self):
        return Utente.objects.filter(parent=self.request.user)


class UserDeleteView(DeleteView):
    model = Utente
    template_name = 'components/confirm_delete.html'
    success_url = reverse_lazy('manage-SubAccounts')


class Modifica(LoginRequiredMixin, UpdateView):
    model = Utente
    form_class = forms.CustomUserChangeForm
    template_name = 'registration/edituser.html'


class Profilo(LoginRequiredMixin, DetailView):
    model = Utente
    template_name = 'registration/profile.html'


class PassReset(PasswordResetView):
    html_email_template_name = 'emails/registration/reimposta_password.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    extra_email_context = {'domain': 'www.yada.digital'}
    extra_context = {'domain': 'www.yada.digital'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = 'www.yada.digital'
        context['subject'] = 'www.yada.digital'
        return context


def logoutpage(request):
    return render(request, 'registration/logout.html')
