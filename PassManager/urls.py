from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as users_view
from generator import views as gen_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', users_view.user_logout, name='logout'),
    path('register/', users_view.register, name='register'),
    path('' ,gen_view.home, name='manager-home'),
    
    #  user passwords
    path('manage-passwords/', gen_view.manage_passwords, name="manage-passwords"),
    path('add-password/', gen_view.add_new_password, name="add-password"),
    path('edit-password/<str:pk>/',gen_view.edit_password, name="edit-password"),
    
    # path for generating random password
    path('generate-password/', gen_view.generate_password, name='generate-password'),
]
