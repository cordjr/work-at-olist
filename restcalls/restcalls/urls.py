"""restcalls URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="RestCalls API",
        default_version='v1',
        description="",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="cordjr@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

doc_view = schema_view.with_ui('redoc', cache_timeout=None)
urlpatterns = [
    # path('admin/', admin.site.urls),
    url('^api/v1/', include('restcalls.core.urls')),
    url(r'^docs/$', doc_view, name='schema-swagger-ui'),
    url(r'^$', doc_view),
]
