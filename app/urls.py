from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from . import views_anggota
from . import views_admin_set
from . import views_admin

urlpatterns = [

    ###### ALL ###### 
    
    path('', views.index, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),      
    path('', views.index, name='index'),      

    ###### DOSEN ######
    path('profile/anggota/', views_anggota.profile_anggota, name='profile_anggota'),
    path('profile/admin/', views_admin_set.profile_admin, name='profile_admin'),
    path('user_list', views_admin_set.user_list, name='user_list'),      
    path('user_edit/<str:id>/<str:role>/', views_admin_set.user_edit, name='user_edit'),
    path('reset_password/dosen/', views_anggota.reset_password_anggota, name='reset_password_anggota'),
    # path('dosen/delete-pustaka/', views_dosen.delete_pustaka, name='delete_pustaka'),

    ###### PRODI ######
    path('page/', views_admin.page_list, name='page_list'),
    path('page_create/', views_admin.page_create, name='page_create'),
    path('page_edit/<uuid:id>/', views_admin.page_edit, name='page_edit'),
    path('page/delete/<uuid:id>/', views_admin.page_delete, name='page_delete'),
    path('article/', views_admin.article_list, name='article_list'),
    path('article_create/', views_admin.article_create, name='article_create'),
    path('article_edit/<uuid:id>/', views_admin.article_edit, name='article_edit'),
    path('article/delete/<uuid:id>/', views_admin.article_delete, name='article_delete'),
    path('topic/', views_admin.topic_list, name='topic_list'),
    path('topic_create/', views_admin.topic_create, name='topic_create'),
    path('topic/delete/<uuid:id>/', views_admin.topic_delete, name='topic_delete'),

    
]