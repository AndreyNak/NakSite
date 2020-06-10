from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comment/<int:id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/comment/<int:id>/edit/', views.update_comment, name='update_comment'),
    path('about/', views.about, name='about'),
    path('forbidden/', views.forbidden, name='forbidden'),

]
