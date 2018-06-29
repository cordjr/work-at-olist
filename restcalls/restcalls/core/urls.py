from django.conf.urls import url
from rest_framework.documentation import include_docs_urls

from restcalls.core import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'api/v1/calls', views.post_record_call, name='post_record_call'),
    url(r'api/v1/docs', include_docs_urls(title='REstCalls API', public=True))
]
