from django.urls import path
from mychatapp import views

urlpatterns = [
    path('', views.index, name='rota_index'),
    path('friend/<str:pk>', views.details, name='rota_details'),
    path('sent_msg/<str:pk>', views.sentMessages, name='rota_sent'),
    path('received_msg/<str:pk>', views.receivedMessages, name='rota_received'),
    path('notifications', views.chatNotification, name='rota_notification'),
]