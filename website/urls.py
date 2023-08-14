from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import (cm_detail,cm_update,cm_Delete 
                    ,client_detail,client_update,Client_Delete
                    ,order_update,order_Delete,order_detail)

urlpatterns = [
    path('', views.lin, name = 'login'),
    path('404/',views.error_404_view,name='404'),
    path('logout/',views.sign_out,name='logout'),
    path('home/', views.home, name = 'home'),
    path('change_password/',views.change_password,name='change_password'),
    path('profileupdate/',views.UserUpdate,name='user_profile'),
    path('profile/',views.profile_view,name='profile'),
    path('registration/',views.UserRegistration,name='user-registration'),
    path('users/',views.user_View,name='user'),

    #Cameraman
    path('addcm/',views.AddCameraMan,name='addcameraman'),
    path('cm/',views.CamerManView,name='cameraman'),
    path('cm/<pk>',cm_detail.as_view(),name='cm_detail'),
    path('cm/<pk>/update',cm_update.as_view(),name='cm_update'),
    path('cm/<pk>/delete',cm_Delete.as_view(template_name = 'cm_delete.html'),name='cm_delete'),



    #client
    path('client/',views.Client_View,name='client'),
    path('add_client/',views.cleint_add,name='add_client'),
    path('client/<pk>',client_detail.as_view(),name='client_detail'),
    path('client/<pk>/update',client_update.as_view(),name='client_update'),
    path('client/<pk>/delete',Client_Delete.as_view(template_name = 'client_delete.html'),name='client_delete'),
    

    #order
    path('order/',views.Order_view,name= 'order'),
    path('add_order/',views.Order_Add,name='order_add'),
    path('admin_approval/',views.admin_approval,name= 'admin_approval'),
    path('order/<pk>',order_detail.as_view(),name='order_detail'),
    path('order/<pk>/update',order_update.as_view(template_name='order_update.html'),name='order_update'),
    path('order/<pk>/delete',order_Delete.as_view(template_name = 'order_delete.html'),name='order_delete'),

 
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
