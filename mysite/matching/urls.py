from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('emotion/', views.emotion, name='emotion'),
    path('depair/', views.depair, name='depair'),
    path('depair_action/', views.depair_action, name='depair_action'),
    path('store/', views.store, name='store'),
    path('store_action/', views.store_action, name='store_action'),
    # path('get_user/', views.get_user, name='get_user'),
    path('get_user_action/<openId>/',
         views.get_user_action, name='get_user_action'),
    # path('get_diary/', views.get_diary, name='get_diary'),
    path('get_diary_action/<diaryid>',
         views.get_diary_action, name='get_diary_action'),
    # path('get_user_diary/', views.get_user_diary, name='get_user_diary'),
    path('get_user_diary_action/<userid>', views.get_user_diary_action,
         name='get_user_diary_action'),
    path('alt_diary/', views.alt_diary, name='alt_diary'),
    path('alt_diary_action/', views.alt_diary_action, name='alt_diary_action'),
    # path('get_openId/', views.get_openId, name='get_openId'),
    path('get_openId_action/',
         views.get_openId_action, name='get_openId_action')
]
