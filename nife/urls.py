from django.conf.urls import url, include
from nife import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'login/', views.login, name="login"),
    url(r'getfilelist', views.getFile, name="getfilelist"),
    url(r'download', views.download, name='download'),
]