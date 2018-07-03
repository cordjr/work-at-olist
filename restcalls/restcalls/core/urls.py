from django.conf.urls import url
from django.urls import path
from rest_framework.documentation import include_docs_urls
from django.views.generic.base import RedirectView

from restcalls.core import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'calls', views.post_record_call, name='post_record_call'),
    url(r'bill/(?P<number>\d+)?/(?P<month>\d+)-(?P<year>\d+)$', views.get_bill, name='get_bill'),
    url(r'bill/(?P<number>\d+)?/$', views.get_bill, name='get_bill'),
    url(r'docs', include_docs_urls(title='REstCalls API', public=True), name='docs'),
    url(r'^$', RedirectView.as_view(url='api/v1/docs', permanent=False))

]
