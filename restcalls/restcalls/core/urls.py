from django.conf.urls import url
from django.urls import path
from rest_framework.documentation import include_docs_urls
from django.views.generic.base import RedirectView

from restcalls.core import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'api/v1/calls', views.post_record_call, name='post_record_call'),
    path('api/v1/bill/<int:number>', views.get_bill, name='get_bill'),
    url(r'api/v1/docs', include_docs_urls(title='REstCalls API', public=True), name='docs'),
    url(r'', RedirectView.as_view(url='api/v1/docs', permanent=True))


]
