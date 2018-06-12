from django.conf.urls import url

from coin import views

urlpatterns = [
     url(r'^$', views.Index.as_view()),
     url(r'^home/$', views.Home.as_view()),
     url(r'^wallet/new/$', views.Wallet.as_view()),
]
