from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.base, name='base'),
    path('accounts/login',views.login_user, name='login'),
    path('account/logout',views.logout_user, name='logout'),
    path('add/pack', views.add_pack, name='add pack')
]
