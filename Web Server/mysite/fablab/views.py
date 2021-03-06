# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response

from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import Machine, Machine_User, CardID, Logs

from .forms import RegisterFormUser, RegisterFormMachine, RegisterFormCard

from django.views.decorators.csrf import csrf_exempt

import json, time, datetime

from django.utils import timezone

def index(request):
    latest_machine_list = Machine.objects.order_by('-machine_name')
    context = { 'latest_machine_list': latest_machine_list }
    return render(request, 'fablab/index.html', context)

def index2(request):
    latest_machine_list = Machine.objects.order_by('-machine_name')
    context = { 'latest_machine_list': latest_machine_list }
    if request.user.is_authenticated():
        return HttpResponseRedirect('/fablab/machines/')
    else:
        return render(request, 'fablab/index2.html', context)

# /////////////////////////// login, logout and register machine, user and card //////////////////////////////////

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
                return HttpResponse("Your NextLab account is disabled.")
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

#register user
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

#register machine
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
			machine_id = form.cleaned_data['machine_id']
			machine = Machine.objects.filter(machine_name__exact = machineName)
			if machine.exists():
				return HttpResponse("This machine already exists")
			else:
				m = Machine(machine_name = machineName, machine_id = machine_id, machine_status="Available")
				print(m)
				m.save()
				# redirect to a new URL:
				return HttpResponseRedirect('/fablab/machines/')
				
	# if a GET (or any other method) we'll create a blank form
	else:
		form = RegisterFormMachine()

	return render(request, 'fablab/new-machine.html', {'form': form})

#register card
@login_required(login_url='/fablab/index2')
def register_card(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RegisterFormCard(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			cardNumber = form.cleaned_data['cardNumber']
			print(cardNumber)
			card_id = CardID.objects.filter(cardID__exact = cardNumber)
			if card_id.exists():
				return HttpResponse("This card id already exists")
			else:
				c = CardID(cardID = cardNumber)
				c.save()
				# redirect to a new URL:
				return HttpResponseRedirect('/fablab/cards/')
				
	# if a GET (or any other method) we'll create a blank form
	else:
		form = RegisterFormCard()

	return render(request, 'fablab/new-card.html', {'form': form})

#logout
@login_required(login_url='/fablab/index2')
def logout_view(request):

    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/fablab/index2/')


# ////////////////////////////////////////// Users, machines, cards, dashboard, logs ////////////////////////////


#user-list
@login_required(login_url='/fablab/index2')
def users(request):
	context = {}
	try:
		user_list = Machine_User.objects.order_by('id')
		context = { 'user_list': user_list }
	except Machine_User.DoesNotExist:
		raise Http404("No users available")
	return render(request, 'fablab/user-list.html', context)

#machine-list
@login_required(login_url='/fablab/index2')
def machines(request):
	context = {}
	try:
		machine_list = Machine.objects.order_by('id')
		context = { 'machine_list': machine_list }
	except Machine.DoesNotExist:
		raise Http404("You have no machines listed.")
	return render(request, 'fablab/machine-list.html', context)

#card-list
@login_required(login_url='/fablab/index2')
def cards(request):
	context = {}
	try:
		card_list = CardID.objects.order_by('id')
		context = { 'card_list': card_list }
	except CardID.DoesNotExist:
		raise Http404("You have no card listed.")
	return render(request, 'fablab/card-list.html', context)

#dashboard
@login_required(login_url='/fablab/index2')
def dashboard(request):
	ontext = {}
	try:
		machine_list = Machine.objects.order_by('id')
		context = { 'machine_list': machine_list }
	except Machine.DoesNotExist:
		raise Http404("You have no machines listed.")
	return render(request, 'fablab/dashboard.html', context)

#logs
@login_required(login_url='/fablab/index2')
def logs(request):
	context = {}
	duration = {}
	logs = []
	try:
		all_logs = Logs.objects.all()
		for obj in all_logs:
			if obj.finish_time is not None:
				logs.append(obj)
		#logs = Logs.objects.filter(finish_time != None)
		if all_logs:
			context = { 'logs': logs }
	except Logs.DoesNotExist:
		raise Http404("You have no logs yet.")
	return render(request, 'fablab/logs.html', context)



# ////////////////////////////////////////// Detail users, machines, cards & access ////////////////////////////


#detail machine
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
'''
#access machine
@csrf_exempt
def access_machine(request):
    context = {}
    print(request.body)
    try:
        body = json.loads(request.body)
        if body["type"] == "access_demand":
            cardID = body["card_uid"]
            module_id = body["module_id"]
            m = Machine.objects.get(machine_id = module_id)
            m.machine_status = "In use"
            log = Logs(cardID = cardID, machine = m.machine_name)
            log.save()
        elif body["type"] == "access_end":
			module_id = body["module_id"]
    except Machine.DoesNotExist:
	return JsonResponse ({"type":"access_error","reason":"module_unknown"})
    except ValueError:
        return HttpResponseBadRequest()
    except KeyError:
        return HttpResponseBadRequest()
    
    if body["type"] == "access_demand":
		try:
			numModule = Machine.objects.get(machine_id__exact = module_id)
		except Machine.DoesNotExist:
			return JsonResponse ({"type":"access_error","reason":"module_unknown"})
		
		try:
			numCard = CardID.objects.get(cardID__exact = cardID)
		except CardID.DoesNotExist:
			return JsonResponse({"type":"access_error","reason":"card_unknown"})
		
		if(numCard.machine_user is None):
			return JsonResponse({"type":"access_error","reason":"card_unown"})
		
		if(numCard.machine_user in numModule.machine_user.all()):
			return JsonResponse({"type":"access_answer","access":"granted"})
		else :
			return JsonResponse({"type":"access_answer","access":"denied"})
    elif body["type"] == "access_end":
		m = Machine.objects.get(machine_id = module_id)
		m.machine_status = "Available"
		log = Logs.objects.filter(machine__exact = m.machine_name, finish_time = None).distinct()
		log[0].finish_time = datetime.timenow()
		duration = logs[0].finish_time - logs[0].start_time
		th = duration.seconds/3600
		tm = duration.seconds/60 - th*60
		ts = duration.seconds - th*3600 - tm*60
		th = str(th)
		tm = str(tm)
		ts = str(ts)
		duration = th + " h " + tm + " mins " + ts + " s"
		obj.duration = duration
		log[0].save()
'''

#access machine
@csrf_exempt
def access_machine(request):
    context = {}
    print(request.body)
    try:
        body = json.loads(request.body)
        if body["type"] == "access_demand":
            cardID = body["card_uid"]
            module_id = body["module_id"]
            try:
                numModule = Machine.objects.get(machine_id__exact = module_id)
            except Machine.DoesNotExist:
                return JsonResponse ({"type":"access_error","reason":"module_unknown"})
            try:
                numCard = CardID.objects.get(cardID__exact = cardID)
            except CardID.DoesNotExist:
                return JsonResponse({"type":"access_error","reason":"card_unknown"})
            if(numCard.machine_user is None):
                return JsonResponse({"type":"access_error","reason":"card_unown"})
            if(numCard.machine_user in numModule.machine_user.all()):
                numModule.machine_status = "In use"
                numModule.save()
                log = Logs(cardID = cardID, machine = module_id)
                log.save()
                return JsonResponse({"type":"access_answer","access":"granted"})
            else :
                return JsonResponse({"type":"access_answer","access":"denied"})
           
        elif body["type"] == "access_end":
            module_id = body["module_id"]
            m = Machine.objects.get(machine_id = module_id)
            m.machine_status = "Available"
            m.save()
            log = Logs.objects.get(machine__exact = module_id, finish_time = None)
            print(log)
	    log.finish_time = timezone.now()
            duration = log.finish_time - log.start_time
            th = duration.seconds/3600
            tm = duration.seconds/60 - th*60
            ts = duration.seconds - th*3600 - tm*60
            th = str(th)
            tm = str(tm)
            ts = str(ts)
            duration = th + " h " + tm + " mins " + ts + " s"
            log.duration = duration
            log.save()
            return HttpResponse("") 
            
    except ValueError:
        return HttpResponseBadRequest()
    except KeyError:
        return HttpResponseBadRequest()


#detail user
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

#detail card
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




# //////////////////////////////////// new user, new machine, new card //////////////////////

#new user
@login_required(login_url='/fablab/index2')
def new_user(request):
	form = RegisterFormUser(request.POST)
	return render(request, 'fablab/new-user.html', {'form': form})

#new machine
@login_required(login_url='/fablab/index2')
def new_machine(request):
	form = RegisterFormMachine(request.POST)
	return render(request, 'fablab/new-machine.html', {'form': form})

#new card
@login_required(login_url='/fablab/index2')
def new_card(request):
	form = RegisterFormCard(request.POST)
	return render(request, 'fablab/new-card.html', {'form': form})


# //////////////////////////////////// delete user, machine and card //////////////////////


#delete machine
@login_required(login_url='/fablab/index2')
def delete_machine(request, machine_name):
	m = Machine.objects.get(machine_name__exact = machine_name)
	m.delete()
	return HttpResponseRedirect('/fablab/machines/')

#delete user
@login_required(login_url='/fablab/index2')
def delete_user(request, user):
	u = user.split()
	u = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	u.delete()
	return HttpResponseRedirect('/fablab/users/')

#delete card
@login_required(login_url='/fablab/index2')
def delete_card(request, card_id):
	card = CardID.objects.get(cardID__exact = card_id)
	card.delete()
	return HttpResponseRedirect('/fablab/cards/')




# ////////////////////////////////// add machine to user , add user to ... /////////////////////////

#add machine machine to user
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

#add user to machine
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

#add user to card
@login_required(login_url='/fablab/index2')
def add_user_to_card(request, user, card_id):
	u = user.split()
	user = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	card = CardID.objects.get(cardID__exact = card_id)
	
	#if card.machine_user is None:
	if user:
		user = user[0]
		#card.machine_user = user
		user.cardid_set.add(card)
		user.save()
	the_url = '/fablab/cards/'+card_id
	return HttpResponseRedirect(the_url)

#add machine to card
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




# /////////////////////////////////////////// remove user from machine, remove machine from ... //////////////////////////

#remove user from machine
@login_required(login_url='/fablab/index2')
def remove_user_from_machine(request, user, machine_name):
	u = user.split()
	u = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	m = Machine.objects.get(machine_name__exact = machine_name)
	m.machine_user.remove(u[0])
	the_url = '/fablab/machines/'+machine_name
	return HttpResponseRedirect(the_url)

#remove user from card
@login_required(login_url='/fablab/index2')
def remove_user_from_card(request, user, card_id):
	u = user.split()
	u = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	c = CardID.objects.get(cardID=card_id)
	c.machine_user=None
	c.save()
	the_url = '/fablab/cards/'+card_id
	return HttpResponseRedirect(the_url)

#remove card from user
@login_required(login_url='/fablab/index2')
def remove_card_from_user(request, user, card_id):
	u = user.split()
	u = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	c = CardID.objects.get(cardID=card_id)
	c.machine_user=None
	c.save()
	the_url = '/fablab/users/'+user
	return HttpResponseRedirect(the_url)

#remove machine from user
@login_required(login_url='/fablab/index2')
def remove_machine_from_user(request, user, machine_name):
	u = user.split()
	u = Machine_User.objects.filter(first_name__exact=u[0], last_name__exact=u[1])
	m = Machine.objects.get(machine_name__exact = machine_name)
	m.machine_user.remove(u[0])
	the_url = '/fablab/users/'+user
	return HttpResponseRedirect(the_url)




# /////////////////////////////////////////// Change user's name, change machine's name ... , update machine status //////////////////////////


#Change user's name
@login_required(login_url='/fablab/index2')
def change_user_name(request, old_user_name, new_user_name):
	if request.method == 'POST':
		old_u = old_user_name.split()
		new_u = new_user_name.split()
		u = Machine_User.objects.get(first_name__exact=old_u[0], last_name__exact=old_u[1])
		u.first_name = new_u[0]
		u.last_name = new_u[1]
		u.save()
		the_url = '/fablab/users/'+new_user_name
		return HttpResponseRedirect(the_url)
	else:
		return HttpResponseRedirect('/fablab/users/')

#Change machine details
@login_required(login_url='/fablab/index2')
def change_machine_details(request, old_machine_name, old_machine_id, new_machine_name, new_machine_id):
	if request.method == 'POST':
		m = Machine.objects.get(machine_name__exact=old_machine_name)
		m.machine_name = new_machine_name
		if old_machine_id != new_machine_id:
			m.machine_id = new_machine_id
		m.save()
		the_url = '/fablab/machines/'+new_machine_name
		return HttpResponseRedirect(the_url)
	else:
		return HttpResponseRedirect('/fablab/machines/')


#Change card details
@login_required(login_url='/fablab/index2')
def change_card_details(request, old_card_number, new_card_number):
	if request.method == 'POST':
		c = CardID.objects.get(cardID = old_card_number)
		c.cardID = new_card_number
		c.save()
		the_url = '/fablab/cards/'+new_card_number
		return HttpResponseRedirect(the_url)
	else:
		return HttpResponseRedirect('/fablab/cards/')

#Update machine status
@login_required(login_url='/fablab/index2')
def update_machine_status(request):
	machine_id = request.GET.get('machine_id', None)
	print(machine_id)
	print("here")
	m = Machine.objects.filter(machine_id = machine_id)
	data = {
		'machine_status': m.machine_status
	}
	return JsonResponse(data)


