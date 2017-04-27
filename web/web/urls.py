from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Login/Logout
    url(
        r'^accounts/login/',
        auth_views.login,
        name='login',
        kwargs={
            'template_name': 'login.html'
        }
    ),
    url(
        r'^accounts/logout/',
        auth_views.logout,
        name='logout',
        kwargs={
            'next_page': settings.LOGIN_URL,
        }
    ),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^daily/$', 'melon.views.index'),
    url(r'^daily/(?P<page>[0-9]+)/$', 'melon.views.index'),
    url(r'^isgather/$', 'melon.views.is_gather'),
    url(r'^dogather/$', 'melon.views.do_gather'),
]
