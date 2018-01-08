# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response

from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import Machine, Machine_User, CardID

from .forms import RegisterFormUser, RegisterFormMachine


def index(request):
    latest_machine_list = Machine.objects.order_by('-machine_name')
    context = { 'latest_machine_list': latest_machine_list }
    return render(request, 'fablab/index.html', context)

def index2(request):
    latest_machine_list = Machine.objects.order_by('-machine_name')
    context = { 'latest_machine_list': latest_machine_list }
    return render(request, 'fablab/index2.html', context)

# /////////////////////////// login, logout and register //////////////////////////////////

#login
def login_view(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/fablab/machines/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your SmartLab account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return HttpResponseRedirect('/fablab/index2/')

#logout
@login_required(login_url='/fablab/index2')
def register_user(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RegisterFormUser(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			firstname = form.cleaned_data['firstname']
			surname = form.cleaned_data['surname']
			user = Machine_User.objects.filter(first_name__exact = firstname, last_name__exact = surname)
			if user.exists():
				return HttpResponse("This name already exists")
			else:
				u = Machine_User(first_name=firstname, last_name=surname)
				u.save()
				# redirect to a new URL:
				return HttpResponseRedirect('/fablab/users/')
				
	# if a GET (or any other method) we'll create a blank form
	else:
		form = RegisterFormUser()

	return render(request, 'fablab/new-user.html', {'form': form})

@login_required(login_url='/fablab/index2')
def register_machine(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RegisterFormMachine(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			machineName = form.cleaned_data['machineName']
			machine = Machine.objects.filter(machine_name__exact = machineName)
			if machine.exists():
				return HttpResponse("This machine already exists")
			else:
				#u = Machine_User.objects.filter(first_name__exact='Kali', last_name__exact='Linux')
				#m = Machine(machine_name=machineName, machine_user=u[0])
				m = Machine(machine_name=machineName)
				
				m.save()
				# redirect to a new URL:
				return HttpResponseRedirect('/fablab/machines/')
				
	# if a GET (or any other method) we'll create a blank form
	else:
		form = RegisterFormMachine()

	return render(request, 'fablab/new-machine.html', {'form': form})

#register machine
@login_required(login_url='/fablab/index2')
def logout_view(request):

    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/fablab/index2/')


# ////////////////////////////////////////// Users, machines and cards ////////////////////////////


@login_required(login_url='/fablab/index2')
def users(request):
	context = {}
	try:
		user_list = Machine_User.objects.order_by('id')
		context = { 'user_list': user_list }
	except Machine_User.DoesNotExist:
		raise Http404("No users available")
	return render(request, 'fablab/user-list.html', context)

@login_required(login_url='/fablab/index2')
def machines(request):
	context = {}
	try:
		machine_list = Machine.objects.order_by('id')
		context = { 'machine_list': machine_list }
	except Machine.DoesNotExist:
		raise Http404("You have no machines listed.")
	return render(request, 'fablab/machine-list.html', context)

@login_required(login_url='/fablab/index2')
def cards(request):
	context = {}
	try:
		card_list = CardID.objects.order_by('id')
		context = { 'card_list': card_list }
	except CardID.DoesNotExist:
		raise Http404("You have no card listed.")
	return render(request, 'fablab/card-list.html', context)


@login_required(login_url='/fablab/index2')
def detail_machine(request, machine_name):
	context = {}
	machine_users = {}
	user_list = {}
	try:
		machine = Machine.objects.get(machine_name__exact = machine_name)
		machine_users = machine.machine_user.all()
	except Machine.DoesNotExist:
		raise Http404("This machine does not exist")
	
	user_list = Machine_User.objects.order_by('id')
	
	context = { 'machine': machine , 'machine_users' : machine_users , 'user_list': user_list}
	return render(request, 'fablab/machine-details.html', context)

def access_machine(request, cardID):
	context = {}
	try:
		numCard = CardID.objects.get(cardID__exact = cardID)
		access='Yes'
		context = { 'access': access}
	except CardID.DoesNotExist:
		access='No'
		context = { 'access': access}
	return render(request, 'fablab/access.html', context)

@login_required(login_url='/fablab/index2')
def detail_user(request, user_name):
	context = {}
	user = {}
	machine_list = {}
	try:
		user_name = user_name.split()
		user = Machine_User.objects.filter(first_name__exact = user_name[0], last_name__exact = user_name[1])
		user = user[0]
	except IndexError:
		raise Http404("Machine_User does not exist")
	machine_list = Machine.objects.order_by('id')
	context = { 'user': user , 'machine_list' : machine_list }
	return render(request, 'fablab/user-details.html', context)

@login_required(login_url='/fablab/index2')
def detail_card(request, card_id):
	context = {}
	machine_user = []
	try:
		card = CardID.objects.get(cardID__exact = card_id)
		if card.machine_user is not None:
			machine_user.append(card.machine_user)
	except CardID.DoesNotExist:
		raise Http404("This card does not exist")
	
	user_list = Machine_User.objects.order_by('id')
	
	context = { 'cardID': card , 'machine_user' : machine_user , 'user_list':user_list }
	return render(request, 'fablab/card-details.html', context)






@login_required(login_url='/fablab/index2')
def detail(request, machine_id):
    return HttpResponse("You're looking at machine %s." % machine_id)

@login_required(login_url='/fablab/index2')
def testpage(request):
	machine_list = Machine.objects.all()
	user_list = Machine_User.objects.all()
	cardID_list = CardID.objects.all();
	context = { 'machine_list': machine_list, 'user_list' : user_list, 'cardID_list' : cardID_list }
	return render(request, 'fablab/testpage.html', context)

@login_required(login_url='/fablab/index2')
def detail2(request):
    machine_name = request.GET['machine_name']
    return HttpResponse("You're looking at machine %s." % machine_name)

# //////////////////////////////////// new user, new machine, new card & delete //////////////////////

@login_required(login_url='/fablab/index2')
def new_user(request):
	form = RegisterFormUser(request.POST)
	return render(request, 'fablab/new-user.html', {'form': form})

@login_required(login_url='/fablab/index2')
def new_machine(request):
	form = RegisterFormMachine(request.POST)
	return render(request, 'fablab/new-machine.html', {'form': form})

@login_required(login_url='/fablab/index2')
def new_card(request):
	form = RegisterFormMachine(request.POST)
	return render(request, 'fablab/new-card.html', {'form': form})

@login_required(login_url='/fablab/index2')
def delete_machine(request, machine_name):
	m = Machine.objects.get(machine_name__exact = machine_name)
	m.delete()
	return HttpResponseRedirect('/fablab/machines/')

@login_required(login_url='/fablab/index2')
def delete_user(request, user):
	u = user.split()
	u = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	u.delete()
	return HttpResponseRedirect('/fablab/users/')


# /////////////////////////////////////////// remove user, machine and card //////////////////////////

@login_required(login_url='/fablab/index2')
def remove_user_from_machine(request, user, machine_name):
	u = user.split()
	u = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	m = Machine.objects.get(machine_name__exact = machine_name)
	m.machine_user.remove(u[0])
	the_url = '/fablab/machines/'+machine_name
	return HttpResponseRedirect(the_url)

@login_required(login_url='/fablab/index2')
def remove_user_from_card(request, user, card_id):
	u = user.split()
	u = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	#m = Machine.objects.get(machine_name__exact = machine_name)
	c = CardID.objects.get(cardID=card_id)
	c.machine_user=None
	c.save()
	the_url = '/fablab/cards/'+card_id
	return HttpResponseRedirect(the_url)

@login_required(login_url='/fablab/index2')
def remove_machine_from_user(request, user, machine_name):
	u = user.split()
	u = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	m = Machine.objects.get(machine_name__exact = machine_name)
	m.machine_user.remove(u[0])
	the_url = '/fablab/users/'+user
	return HttpResponseRedirect(the_url)


# ////////////////////////////////// add machine, user and card /////////////////////////

@login_required(login_url='/fablab/index2')
def add_machine_to_user(request, user, machine_name):
	u = user.split()
	user_name = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	m = Machine.objects.get(machine_name__exact = machine_name)
	machine_set = user_name[0].machine_set.all()
	machine_list = list(machine_set)
	if m not in machine_set:
		m.machine_user.add(user_name[0])
	the_url = '/fablab/users/'+user
	return HttpResponseRedirect(the_url)

@login_required(login_url='/fablab/index2')
def add_user_to_machine(request, user, machine_name):
	u = user.split()
	user_name = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	m = Machine.objects.get(machine_name__exact = machine_name)
	machine_set = user_name[0].machine_set.all()
	if m not in machine_set:
		m.machine_user.add(user_name[0])
	the_url = '/fablab/machines/'+machine_name
	return HttpResponseRedirect(the_url)

@login_required(login_url='/fablab/index2')
def add_user_to_card(request, user, card_id):
	u = user.split()
	user_name = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	card = CardID.objects.get(cardID__exact = card_id)
	#card_set = user_name[0].cardid_set.all()
	
	if card.machine_user is None:
		if user_name:
			card.machine_user = user_name[0]
			card.save()
	the_url = '/fablab/cards/'+card_id
	return HttpResponseRedirect(the_url)

@login_required(login_url='/fablab/index2')
def add_machine_to_card(request, machine_name, card_id):
	u = user.split()
	m = Machine.objects.get(machine_name__exact = machine_name)
	card = CardID.objects.get(cardID__exact = card_id)
	card_set = m.cardid_set.all()
	if card not in card_set:
		card.machine.add(user_name[0])
	the_url = '/fablab/cards/'+card_id
	return HttpResponseRedirect(the_url)

