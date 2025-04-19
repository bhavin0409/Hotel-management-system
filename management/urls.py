"""
URL configuration for management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hotelpro.views import *
from django.conf import settings
from django.conf.urls.static import static
from hotelpro import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('cus_login/' , cus_login),
    path('cus_registration/' , cus_registration ),
    path('customerlist/' , customerlist ,name="customerlist"),
    path('cuslogout/',cuslogout,name="cuslogout"),

    path('profile/<int:cus_id>' , profile , name="profile"),
    path('updateprofile/<int:cus_id>',updateprofile,name="updateprofile"),
    
    path('' , home ),
    path('about/' , aboutus),
    path('gallery/', gallery),
    path('contact/', contact),
    path('ourroomr/<slug:data>/' , ourroomr),
    path('ourroom/' , ourroom),
    path('roomdetail/<int:room_id>/' , roomDetail),
    path('booknow/<int:room_id>/' , booknow),
    path('foodmenu/' , foodmenu),
    path('menu/<slug:f>/', views.menu, name='menu'),
    path('my_reservation/<int:cus_id>/' , booking),
    path('delete_my_reservation/<int:Booking_id>/' , deletebooking , name="deletebooking"),

    path('customadmin/', custumAdmin , name="customadmin"),
    path('login_admin/' , login_admin , name="admin_login"),
    path('admin_logout/' , admin_logout),

    path('a_booking/' , a_booking , name='a_booking'),
    path('update_b_status/<int:booking_id>' , update_b_status , name='update_b_status'),

    path('packageform/' , packageform , name="packageform"),
    path('packagelist/' , packagelist , name="packagelist"),
    path('package_deletepost/<int:delete_id>',package_deletepost,name="deletepost"),
    path('editpost/<int:edit_id>',editpost,name="package_editpost"),

    path('employeelist/' , employeelist , name="employeelist"),
    path('employeeform/' , employeeform , name="employeeform"),
    path('emp_editpost/<int:edit_id>',emp_editpost,name="editpost"),
    path('deletepost/<int:delete_id>',deletepost,name="deletepost"),

    path('food/' , food , name="food"),
    path('foodlist/' , foodlist , name="foodlist"),
    path('fe_editpost/<int:edit_id>' , fe_editpost , name="f_editpost"),
    path('f_deletepost/<int:delete_id>',f_deletepost,name="f_deletepost"),
    
    path('food_category/',f_category,name="food_category"),
    path('food_categorylist/',f_list,name="food_list"),
    path('food_category_edit/<int:edit_id>',f_edit,name="food_category_edit"),
    path('food_category_delete/<int:delete_id>',f_delete,name="food_category_delete"),

    path('designation/' , designation , name="designation"),
    path('designationlist/' ,  designationlist , name="designationlist"),
    path('designation_delete/<int:delete_id>' , des_delete , name="designation_delete"),
    path('designation_edit/<int:edit_id>' , designation_edit , name="designation_edit"),

    path('room/' , room , name="room"),
    path('roomlist/' , roomlist ,name="roomlist"),
    path('r_deletepost/<int:delete_id>' , r_deletepost),
    path('r_editpost/<int:edit_id>' , r_editpost ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)