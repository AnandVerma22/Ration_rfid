from django.urls import path

from . import views

urlpatterns = [
    path('',views.vindex, name='vindex'),
    path('Vcontact',views.vcontact, name='vcontact'),
    path('Vabout',views.vabout, name='vabout'),
    path('Vrfid',views.vrfid, name='vrfid'),
    path('Vsignin',views.vsignin, name='vsignin'),
    path('Vcenter',views.vcenter, name='vcenter'),
    path('Vsignout',views.vsignout, name='vsignout'),
    path('Vprofile',views.vprofile, name='vprofile'),
    path('Vcard_holder',views.vcard_holder, name='vcard_holder'),
    path('Vmember_edit',views.vmember_edit, name='vmember_edit'),
    path('Vmember',views.vmember, name='vmember'),
    path('Vsubmember',views.vsubmember, name='vsubmember'),
    path('Vsubmember_edit',views.vsubmember_edit, name='vsubmember_edit'),
    path('Vsubmember_add',views.vsubmember_add, name='vsubmember_add'),
    path('Vpending',views.vpending, name='vpending'),
    path('Vgive',views.vgive, name='vgive'),
    path('Vcollected',views.vcollected, name='vcollected'),
    path('Vfinal',views.vfinal, name='vfinal'),
]