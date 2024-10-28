
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_dashboard/', include('admin_dashboard.urls')),
    path('', include('user.urls')),
    path('colorpic/', include('colorpic.urls')),
    path('textetoimage/', include('textetoimage.urls')),
    path('reclamations/', include('reclamation.urls') , name='reclamations'),
    

]
