from django.urls import path,include
from . import views

app_name = 'blog'

urlpatterns= [
    path('',views.Index.as_view(),name='index_name'),
    path('posts/',views.PostListView.as_view(),name='posts_list'),
    path('posts/<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
    path('posts_create/',views.PostCreateView.as_view(),name='post_create'),
    path('posts_update_form/<int:pk>',views.PostUpdateView.as_view(),name='post_update'),
    path('post_delete_confirm/<int:pk>',views.PostDeleteView.as_view(),name='post_delete_confirm'),
    path('add_comment/<int:pk>',views.add_comment_to_post,name='comment_add_form'),
    path('delete_comment/<int:pk>',views.delete_comment_from_post,name='comment_delete_form'),
    path('post_publish_confirm/<int:pk>',views.PostPublishConfirm,name='post_publish_confirm'),
    
]
