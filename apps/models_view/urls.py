from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^models_view$', views.index, name="index" ),
]
