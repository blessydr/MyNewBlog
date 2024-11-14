
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_blog', views.create_blogs, name='create_blog'),
    path('blog_details/<int:id>/',views.blog_details,name='blog_details' ),
    path('delete_blog/<int:id>/', views.delete_blog, name='delete_blog'),
    path('edit_blog/<int:id>/', views.edit_blog, name='edit_blog'),
    path('custom_tag',views.create_tag,name='custom_tag' ),
    path('comment/edit/<int:id>/', views.edit_cmt, name='edit_comment'),
    path('comment/delete/<int:id>/', views.delete_cmt, name='delete_comment'),

]
