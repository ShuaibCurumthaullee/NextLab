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
    
    # /register-card
    url(r'^register-card/$', views.register_card),
    
    # /machines
    url(r'^machines/$', views.machines, name='machines'),
    
    # /machines/<machine_name>
    url(r'^machines/(?P<machine_name>\D+)/$', views.detail_machine),
    
    # /access/<cardID>
    url(r'^access/$', views.access_machine),
    
    # /new-machine
    url(r'^new-machine/$', views.new_machine),
    
    # /dashboard
    url(r'^dashboard/$', views.dashboard),
    
    # /logs
    url(r'^logs/$', views.logs),
    
    
    
    
    # /new-card
    url(r'^new-card/$', views.new_card),
    # /cards
    url(r'^cards/$', views.cards),
    # /machines/<card_id>
    url(r'^cards/(?P<card_id>\w+)/$', views.detail_card),
    
    
    
    # /delete_machine/<machine_name>
    url(r'^delete_machine/(?P<machine_name>\D+)/$', views.delete_machine),
    
    # /delete_user/<user_name>
    url(r'^delete_user/(?P<user>[\w|\W]+)/$', views.delete_user),
    
    # /delete_card/<card_number>
    url(r'^delete_card/(?P<card_id>[\w|\W]+)/$', views.delete_card),
    
    
    # /change_username/<old_user_name>/new_user_name
    url(r'^change_username/(?P<old_user_name>[\w|\W]+)/(?P<new_user_name>[\w|\W]+)/$', views.change_user_name),
    
    # /change_machine_details/old_machine_name/old_machine_id/new_machine_name/new_machine_id
    url(r'^change_machine_details/(?P<old_machine_name>[\w|\W]+)/(?P<old_machine_id>[\w|\W]+)/(?P<new_machine_name>[\w|\W]+)/(?P<new_machine_id>[\w|\W]+)/$', views.change_machine_details),
    
    # /change_card_details/<old_card_number>/new_card_number
    url(r'^change_card_details/(?P<old_card_number>[\w|\W]+)/(?P<new_card_number>[\w|\W]+)/$', views.change_card_details),
    
    
    # /add_machine_to_user/{{ machine.machine_name }}/ {{ user }}
    url(r'^add_machine_to_user/(?P<machine_name>[\w|\W]+)/(?P<user>[\w|\W]+)/$', views.add_machine_to_user),
    
    # /remove_user_from_machine
    url(r'^remove_user_from_machine/(?P<user>[\w|\W]+)/(?P<machine_name>[\w|\W]+)/$', views.remove_user_from_machine),
    
    # /add_user_to_machine/{{ machine.machine_name }}/ {{ user }}
    url(r'^add_user_to_machine/(?P<machine_name>[\w|\W]+)/(?P<user>[\w|\W]+)/$', views.add_user_to_machine),
    
    # /add_user_to_card/{{ user_name }}/ {{ card_id }}
    url(r'^add_user_to_card/(?P<user>[\w|\W]+)/(?P<card_id>\w+)/$', views.add_user_to_card),
    
    # /remove_machine_from_user
    url(r'^remove_machine_from_user/(?P<user>[\w|\W]+)/(?P<machine_name>[\w|\W]+)/$', views.remove_machine_from_user),
    
    # /remove_user_from_card
    url(r'^remove_user_from_card/(?P<user>[\w|\W]+)/(?P<card_id>\w+)/$', views.remove_user_from_card),
    
    # /remove_card_from_card
    url(r'^remove_card_from_user/(?P<user>[\w|\W]+)/(?P<card_id>\w+)/$', views.remove_card_from_user),
    
    # /login/
    url(r'^login/$', views.login_view, name='login'),
    
    # /logout/
    url(r'^logout/$', views.logout_view, name='logout'),
]
