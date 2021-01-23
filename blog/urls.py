from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.home,name='home'),
    path('blog/<slug:slug>/',views.post_detail,name='post-detail'),
    path('blog/<slug:slug>/comment/',views.add_comment,name='add_comment'),
    path('category/<str:pk>/',views.view_category,name='view_category'),
    path('subscribe/',views.subscribe,name='subscribe'),
    path('contact/',views.contact,name='contact'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),

# Password reset form
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='users/password-reset.html'),name='password-reset'),
    path('password_reset_done/',auth_view.PasswordResetDoneView.as_view(template_name='users/password-reset-done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='users/password-reset-confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='users/password-reset-complete.html'),name='password_reset_complete'),

#Admin 
    path('dashboard/',views.dashboard,name='dashboard'),
    path('new-post/',views.new_post,name='new-post'),
    path('update_post/<slug:slug>/',views.update_post,name='update_post'),
    path('delete_post/<slug:slug>/',views.delete_post,name='delete_post'),
    path('newsletters/',views.newsletter,name='newsletters'),

]

