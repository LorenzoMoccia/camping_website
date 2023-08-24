from django.urls import include
from django.urls import path

from . import registration
from . import views

urlpatterns = [path('', include('django.contrib.auth.urls')),
               path('', views.UserListView.as_view(), name='listUtenti'),
               path('subaccounts/', views.ManageSubaccounts.as_view(), name='manage-SubAccounts'),
               path('delete/<int:pk>', views.UserDeleteView.as_view(), name='deleteUtente'),
               path('goodbye/', views.logoutpage, name='goodbye'),
               path('<int:pk>', views.Profilo.as_view(), name='detailUtente'),
               path('edit/<int:pk>', views.Modifica.as_view(), name='updateUtente'),
               path('password_reset',
                    views.PassReset.as_view(html_email_template_name='emails/registration/reimposta_password.html',
                                            subject_template_name='registration/password_reset_subject.txt'),
                    name='resetta-pass'),

               # views per la registrazione
               path('signup/', registration.signup, name='signup'),
               path('<str:uidb64>/<str:token>', registration.activate, name='activate'),
               path('complete', registration.registration_complete, name='registrationComplete')
               ]
