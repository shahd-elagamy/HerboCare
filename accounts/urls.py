from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_to_favorites/<int:herb_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:herb_id>/', views.remove_from_favorites, name='remove_from_favorites'),

]