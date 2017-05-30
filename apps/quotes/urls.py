from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^quotes$', views.index, name="index"),

    url(r'^quotes/add_quote$', views.add_quote, name="add_quote"),
    url(r'^quotes/add_favorite/(?P<u_id>\d+)/(?P<q_id>\d+)$', views.add_favorite, name="add_favorite"),
    url(r'^quotes/remove_favorite/(?P<u_id>\d+)/(?P<q_id>\d+)$', views.remove_favorite, name="remove_favorite"),
    url(r'^users/(?P<id>\d+)$', views.view_user, name="view_user"),

    url(r'^', views.catcher, name="catcher"),
]
