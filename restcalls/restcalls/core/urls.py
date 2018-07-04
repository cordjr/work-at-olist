from django.conf.urls import url

from restcalls.core import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'calls', views.post_record_call, name='post_record_call'),
    url(r'bill/(?P<number>\d+)?/(?P<month>\d+)-(?P<year>\d+)$', views.get_bill, name='get_bill'),
    url(r'bill/(?P<number>\d+)?/$', views.get_bill, name='get_bill'),

]
