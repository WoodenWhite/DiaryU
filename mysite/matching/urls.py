from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('emotion/', views.emotion, name='emotion'),
    path('depair/', views.depair, name='depair'),
    path('depair_action/', views.depair_action, name='depair_action'),
    path('store/', views.store, name='store'),
    path('store_action/', views.store_action, name='store_action'),
    path('get_user/', views.get_user, name='get_user'),
    path('get_user_action/',
         views.get_user_action, name='get_user_action'),
    path('get_diary/', views.get_diary, name='get_diary'),
    path('get_diary_action/',
         views.get_diary_action, name='get_diary_action'),
    path('get_user_diary/', views.get_user_diary, name='get_user_diary'),
    path('get_user_diary_action/', views.get_user_diary_action,
         name='get_user_diary_action'),
    path('alt_diary/', views.alt_diary, name='alt_diary'),
    path('alt_diary_action/', views.alt_diary_action, name='alt_diary_action'),
    path('get_openId/', views.get_openId, name='get_openId'),
    path('get_openId_action/',
         views.get_openId_action, name='get_openId_action'),
    path('select_chat_room/', views.select_chat_room, name='select_char_room'),
    path('room/<room_name>/', views.room, name='room'),
    path('get_pair/', views.get_pair, name='get_pair'),
    path('get_pair_action/', views.get_pair_action, name='get_pair_action'),
    path('get_history/', views.get_history, name='get_history'),
    path('get_history_action/', views.get_history_action,
         name='get_history_action'),
    path('delete_diary/', views.delete_diary, name='delete_diary'),
    path('delete_diary_action/', views.delete_diary_action,
         name='delete_diary_action'),

]
