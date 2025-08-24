
from django.contrib import admin
from django.urls import path, include
from account import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.signIn, name='login'),
    path('account/', include('account.urls')),
    path('rccm/', include('rccm.urls')),
    path('role/', include('role.urls')),
    path('accueil/', include('_base.urls')),
    path('magistrats/', include('magistrats.urls')),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)