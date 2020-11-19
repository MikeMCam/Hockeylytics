from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView, PostUpdateView, PostDeleteView)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.news, name='news'),
    path('about/', views.about, name='about'),
    path('stats/', views.my_stats, name='my_stats'),
    path('clients/', views.clients, name='clients'),
    path('feedback/', PostListView.as_view(), name='feedback'),
    path('feedback/<int:pk>/', PostDetailView.as_view(), name='feedback-detail'),
    path('feedback/new/', PostCreateView.as_view(), name='feedback-create'),
    path('feedback/<int:pk>/update/', PostUpdateView.as_view(), name='feedback-update'),
    path('feedback/<int:pk>/delete/', PostDeleteView.as_view(), name='feedback-delete'),
    # path('feedback/', views.feedback, name='feedback'),
]
