from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.ListGroupView.as_view(), name='all'),
    path('create/', views.CreateGroupView.as_view(), name='create'),
    path('posts/in/<slug>', views.SingleGroupView.as_view(), name='single'),
    path('join/<slug>/', views.JoinGroupView.as_view(), name='join'),
    path('leave/<slug>/', views.LeaveGroupView.as_view(), name='leave'),

]
