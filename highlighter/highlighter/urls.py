from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect



urlpatterns = [
    url(r'^$', lambda r:redirect('home:project_list'), name='root'),
    url(r'^admin/', admin.site.urls),
    url(r'^home/',include('home.urls',namespace='home')),
    url(r'^study/',include('study.urls',namespace='study')),
    url(r'^accounts/',include('accounts.urls')),
    url(r'^accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/',include(debug_toolbar.urls)),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)