from django.conf.urls import patterns, url
from download import views

urlpatterns = patterns('',
        url(r'^$', views.index, name="download_page"),
        url(r'^(?P<studyid>[a-fA-F\d]{10})$', views.download_media,
            name="download_media"),
)
