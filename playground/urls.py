from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('home/', home, name='home'),
    path('logout/', logout, name='logout'),
    path('process-audio/', process_audio, name='process_audio'),
    path('watson/', watson_prompter, name='watson_prompter'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)