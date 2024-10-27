from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login, name='login'),  # Login
    path('logout/', views.logout, name='logout'),  # Logout
    path('signup/', views.signup, name='signup'),  # Signup
    path('resources/', views.resources, name='resources'),
    path('chatbot_message/', views.chatbot_message, name='chatbot_message'),  # New chatbot URL
    path('add_inventory/', views.add_inventory, name='add_inventory'),
    path('request_item/<int:item_id>/', views.request_item, name='request_item'),
    path('update_user_state/', views.update_user_state, name='update_user_state'),
    path('prevention/', views.prevention, name='prevention'),  # Prevention page
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
