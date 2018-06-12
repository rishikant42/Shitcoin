from django.conf.urls import url

from coin import views

urlpatterns = [
     url(r'^home/$', views.Home.as_view()),
]
