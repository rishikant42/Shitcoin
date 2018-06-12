from django.conf.urls import url

from coin import views

urlpatterns = [
     url(r'^$', views.Index.as_view()),
     url(r'^home/$', views.Home.as_view()),
     url(r'^wallet/new/$', views.NewWallet.as_view()),
     url(r'^make/transaction/$', views.MakeTransaction.as_view()),
     url(r'^generate/transaction/$', views.generate_txn),
]
