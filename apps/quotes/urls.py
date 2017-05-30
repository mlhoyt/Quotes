from django.conf.urls import url
from . import views

urlpatterns = [
    # render
    url(r'^belt_prep$', views.index, name="index"),

    # # redirect
    # url(r'^', views.catcher, name="catcher"),
]
