from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
	# /index
    url(r'^$', views.index2, name='index2'),
    url(r'^index/$', views.index2, name='index2'),
    url(r'^index.html/$', views.index, name='index'),
    # /index2
    url(r'^index2/$', views.index2, name='index2'),
    
    #url(r'^(?P<machine_id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^results/$', views.detail2, name='detail2'),
    #url(r'^drinks/(?P<drink_name>\D+)/', TemplateView.as_view(template_name='fablab/index.html')),
    
    # /testpage
    url(r'^testpage/$', views.testpage, name='testpage'),
    
    # /users
    url(r'^users/$', views.users, name='users'),
    # /users/<user_name>
    url(r'^users/(?P<user_name>\D+)/$', views.detail_user,),
    # /new-user
    url(r'^new-user/$', views.new_user),
    # /register-user
    url(r'^register-user/$', views.register_user),
    # /register-machine
    url(r'^register-machine/$', views.register_machine),
    # /machines
    url(r'^machines/$', views.machines, name='machines'),
    # /machines/<machine_name>
    url(r'^machines/(?P<machine_name>\D+)/$', views.detail_machine),
    # /machines/<card_id>
    url(r'^cards/(?P<card_id>\w+)/$', views.detail_card),
    
    # /access/<cardID>
    url(r'^access/(?P<cardID>\w+)/$', views.access_machine),
    # /new-machine
    url(r'^new-machine/$', views.new_machine),
    # /delete_machine/<machine_name>
    url(r'^delete_machine/(?P<machine_name>\D+)/$', views.delete_machine),
    # /delete_user/<user_name>
    url(r'^delete_user/(?P<user>[\w|\W]+)/$', views.delete_user),
    # /add_machine_to_user/{{ machine.machine_name }}/ {{ user }}
    url(r'^add_machine_to_user/(?P<machine_name>[\w|\W]+)/(?P<user>[\w|\W]+)/$', views.add_machine_to_user),
    #url(r'^add_user_to_machine/$', views.add_user_to_machine),
    # /remove_user_from_machine
    url(r'^remove_user_from_machine/(?P<user>[\w|\W]+)/(?P<machine_name>[\w|\W]+)/$', views.remove_user_from_machine),
    # /add_user_to_machine/{{ machine.machine_name }}/ {{ user }}
    url(r'^add_user_to_machine/(?P<machine_name>[\w|\W]+)/(?P<user>[\w|\W]+)/$', views.add_user_to_machine),
    # /remove_machine_from_user
    url(r'^remove_machine_from_user/(?P<user>[\w|\W]+)/(?P<machine_name>[\w|\W]+)/$', views.remove_machine_from_user),
    # /login/
    url(r'^login/$', views.login_view, name='login'),
    # /logout/
    url(r'^logout/$', views.logout_view, name='logout'),
]
