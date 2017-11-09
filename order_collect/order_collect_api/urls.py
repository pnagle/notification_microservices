from django.conf.urls import url, include
from order_collect_api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^orders/$', views.order_list.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
