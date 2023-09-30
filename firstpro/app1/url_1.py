from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginpage,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutpage,name='logout'),
    path('',views.Home,name='home'),
    path('root/<str:ky>/',views.root,name="root"),
    path('create-room/',views.createroom,name='createrooms'),
    path('update-room/<str:pk>/',views.updateroom,name='updaterooms'),
    path('delete-room/<str:ky>/',views.deleteform,name='deleterooms'),
    path('delete-comment/<str:ky>/',views.deletecomment,name='delete-comment'),
    path('profile/<str:pk>/',views.userprofile,name='profile')
]
