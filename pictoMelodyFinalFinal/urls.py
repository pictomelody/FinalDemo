from django.conf.urls import include, url
from django.contrib import admin
from pictoMelodyWebApp import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'pictoMelodyFinalFinal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.detect1),
    url(r'^$', views.detect),
]
