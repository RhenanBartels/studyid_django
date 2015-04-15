from django.conf.urls import patterns, url
from download import views

urlpatterns = patterns('',
        url(r'^$', views.index, name="download_page"),
)
