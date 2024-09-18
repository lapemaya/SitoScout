from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home_page,action,calculator,conti,login_page,create_user,contability,creazioneSpesa,modificaSpesa,eliminaspesa,branco,creazionePersona,modificaPersona,eliminaPersona
urlpatterns = [
    path('', home_page, name='home'),
    path('action', action, name='action'),
    path('calculator', calculator, name='calculator'),
    path('conti',conti, name='conti'),
    path('login',login_page, name='login_page'),
    path('create_user',create_user, name='create_user'),
    path('contability',contability, name='contability'),
    path('creazioneSpesa',creazioneSpesa, name='creazioneSpesa'),
    path('modificaSpesa/<int:id>/', modificaSpesa, name='modificaSpesa'),
    path('eliminaspesa/<int:id>/', eliminaspesa, name='eliminaspesa'),
    path('branco', branco, name='branco'),
    path('creazionePersona', creazionePersona, name='creazionePersona'),
    path('modificaPersona/<int:id>/', modificaPersona, name='modificaPersona'),
    path('eliminaPersona/<int:id>/', eliminaPersona, name='eliminaPersona'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)