from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start_game, name='start_game'),
    path('play/', views.game_board, name='game_board'),
    path('guess/', views.make_guess, name='make_guess'),
]
