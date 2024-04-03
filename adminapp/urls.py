from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Category', views.managecategory, name='category'),
    path('Category_edit', views.managecategory_edit, name='category_edit'),
    path('Login', views.managelogin, name='login'),
    path('logout', views.logoutmanage, name='logout'),
    path('Feedback', views.managefeedback, name='feedback'),
    path('Vendor', views.managevendor, name='vendor'),
    path('Vendor_edit', views.managevendor_edit, name='vendor_edit'),
    path('Member', views.managemember, name='member'),
    path('Submember', views.managesubmember, name='submember'),
    path('Member_verify', views.managememberverify, name='member_verify'),
    path('Submember_edit', views.managesubmemberedit, name='submember_edit'),
    path('Ration_view', views.managerationview, name='ration_view'),
    path('Generate_ration', views.manageration, name='generate_ration'),
    path('User_ration', views.manageuser_ration, name='user_ration'),
    path('Vendor_ration', views.managevendor_ration, name='vendor_ration'),
    path('Member_report', views.managemember_report, name='member_report'),
    path('Submember_report', views.managesubmember_report, name='submember_report'),
    path('Vendor_report', views.managevendor_report, name='vendor_report'),
]