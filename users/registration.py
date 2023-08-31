from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from six import text_type

from . import forms
from .models import Utente


class AppTokenGenerator(PasswordResetTokenGenerator):
    """ Inherited from PasswordResetTokenGenerator """

    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


account_activation_token = AppTokenGenerator()


def signup(request):
    form = forms.SignupForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            data = request.POST
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.is_blocked = True
            user.save()
            email = data['email']
            email_body = {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            link = reverse('activate', kwargs={'uidb64': email_body['uid'], 'token': email_body['token']})
            html_message = render_to_string('emails/mail_body.html',

                                            {'activate_url': 'https://' + get_current_site(request).domain + link}
                                            )

            send_mail(from_email='MySite <noreply@example.site>', html_message=html_message, message=email,
                      subject='Attiva il tuo account!', recipient_list=[user.email])

            send_mail(from_email='MySite <noreply@example.site>',
                      html_message=f'{user.email} ha appena registrato un account', message=email,
                      subject='Nuova registrazione', recipient_list=['admin@example.site'])
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('registrationComplete')
    else:
        form = forms.SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def registration_complete(request):
    return render(request, 'registration/registration_complete.html')


def activate(request, uidb64, token):
    """ Activate user from link sent to email post registration """
    user_id = force_str(urlsafe_base64_decode(uidb64))
    user = Utente.objects.get(pk=user_id)
    if not account_activation_token.check_token(user, token):
        return HttpResponse('il token non è valido')
    if user.is_active:
        messages.success(request, f'Il tuo account è già attivo')
        return redirect('dashboard')
    user.is_active = True
    user.save()
    login(request, user)
    messages.success(request,
                     f'L\' account <strong>{user.email}</strong> è stato attivato con successo. Usa il form per completare il tuo account!')
    return redirect('modifica-utente', user.pk)
