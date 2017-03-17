from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import *
from django.contrib.auth.views import login
import django
import squid.views
import squidguard.views
import tasker.views
import licenses.views
import certs.views
import mail.views
import hashez.views

admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'gibloc.views.home', name='home'),
    # url(r'^gibloc/', include('gibloc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',TemplateView.as_view(template_name='topmenu.html')),
    url(r'^accounts/login/$',django.contrib.auth.views.login,{'template_name':'accounts/login.html'}),
    url(r'^accounts/logout/$',django.contrib.auth.views.logout,{'next_page':'/'}),
    #urls for guests
    url(r'^squidguard/whitesites/$',squidguard.views.WhiteSites.as_view()),
    #squid
    url(r'^squid/$',squid.views.Squid.as_view()),
    url(r'^squid/(?P<model>\w+)/(?P<acl>\w+)/$',squid.views.SquidDetail.as_view()),
    #squidGuard
    url(r'^squidguard/$',squidguard.views.SquidGuard.as_view()),
    url(r'^squidguard/(\w+/){1,5}$',squidguard.views.SquidGuardDetail.as_view()),
    #licenses
    url(r'^licenses/$',licenses.views.Nothing.as_view()),
    url(r'^licenses/create/(?P<model>\w+)/$',licenses.views.Create.as_view()),
    url(r'^licenses/list/(?P<model>\w+)/(?P<pk>\w+)/$',licenses.views.List.as_view()),
    url(r'^licenses/detail/(?P<model>\License)/(?P<pk>\w+)/$',licenses.views.DetailOfLicense.as_view()),
    url(r'^licenses/detail/(?P<model>\Owner)/(?P<pk>\w+)/$',licenses.views.DetailOfOwner.as_view()),
    url(r'^licenses/report/(?P<model>License)/(?P<pk>\w+)/$',licenses.views.ReportOfLicense.as_view()),
    url(r'^licenses/import/$',licenses.views.Import.as_view()),
    #tasker
    url(r'^tasker/$',tasker.views.SimpleView.as_view()),
    url(r'^tasker/listof/(?P<model>TaskG)/(?P<pk>\w+)/$',tasker.views.ListOfTask.as_view()),
    url(r'^tasker/detailof/(?P<model>\w+)/(?P<pk>\w+)/$',tasker.views.DetailOfTask.as_view()),
    url(r'^tasker/edit/(?P<model>\w+)/(?P<pk>\w+)/$',tasker.views.EditTask.as_view()),
    url(r'^tasker/create/(?P<model>\w+)/$',tasker.views.Create.as_view()),
    url(r'^tasker/create/(?P<model>\w+)/(?P<pk>\w+)/$',tasker.views.CreateTask.as_view()),
    #certs
    url(r'^certs/$',certs.views.SimpleView.as_view()),
    url(r'^certs/list/$',certs.views.List.as_view()),
    url(r'^certs/create/(?P<model>\w+)/$',certs.views.Create.as_view()),
    url(r'^certs/detail/(?P<pk>\w+)/$',certs.views.Detail.as_view()),
    url(r'^certs/edit/(?P<pk>\w+)/$',certs.views.Edit.as_view()),
    #mail
    url(r'^mail/list/$',mail.views.List.as_view()),
    url(r'^mail/list/(?P<model>\w+)/(?P<pk>\w+)/$',mail.views.List.as_view()),
    url(r'^mail/create/(?P<model>\w+)/$',mail.views.Create.as_view()),
    url(r'^mail/update/(?P<model>\w+)/(?P<pk>\w+)/$',mail.views.Update.as_view()),
    #hashez
    url(r'^hashez/$',hashez.views.Simple.as_view()),
    url(r'^hashez/events/client/(?P<pk>\w+)/$',hashez.views.EventList.as_view()),
    url(r'^hashez/detail/client/(?P<pk>\w+)/$',hashez.views.ClientDetail.as_view()),
]
