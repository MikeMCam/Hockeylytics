from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView, PostUpdateView, PostDeleteView)
from . import views

urlpatterns = [
    # Generic paths
    path('', views.home, name='home'),
    path('news/', views.news, name='news'),
    path('about/', views.about, name='about'),
    path('stats/', views.my_stats, name='my_stats'),
    path('clients/', views.clients, name='clients'),

    # Feedback paths
    path('feedback/', PostListView.as_view(), name='feedback'),
    path('feedback/<int:pk>/', PostDetailView.as_view(), name='feedback-detail'),
    path('feedback/new/', PostCreateView.as_view(), name='feedback-create'),
    path('feedback/<int:pk>/update/', PostUpdateView.as_view(), name='feedback-update'),
    path('feedback/<int:pk>/delete/', PostDeleteView.as_view(), name='feedback-delete'),

    # Coach paths
    path('coach-dashboard/', views.coach_dashboard, name='coach-dashboard'),
    path('invite-players/', views.invite_players, name='invite-players'),
    path('enter-game/', views.enter_game, name='enter-game'),
    path('game-list/', views.game_list, name='game-list'),

    # Player paths
    path('player-dashboard/', views.player_dashboard, name='player-dashboard'),
    path('season-stats/', views.season_stats, name='season-stats'),
    path('team_comparison/', views.team_comparison, name='team-comparison'),
]
