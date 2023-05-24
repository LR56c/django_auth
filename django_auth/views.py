from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render


@login_required
def index( request ):
	context = {
		'user': request.session['user']
	}
	return render( request, 'index.html', context )

# registro

def signup( request ):
	if request.method == 'GET':
		return render( request, 'registration/register.html', {
			"form": UserCreationForm
		} )
	else:
		if request.POST["password1"] == request.POST["password2"]:
			try:
				user = User.objects.create_user( request.POST["username"],
					password=request.POST["password1"] )
				user.save()
				login( request, user )
				request.session['user'] = user.username
				return redirect( 'index' )
			except IntegrityError:
				return render( request, 'registration/register.html', {
					"form" : UserCreationForm,
					"error": "Username already exists."
				} )

		return render( request, 'registration/register.html', {
			"form" : UserCreationForm,
			"error": "Passwords did not match."
		} )


# 	logout
@login_required
def signout( request ):
	logout( request )
	return redirect( 'login' )


# login
def signin( request ):
	if request.method == 'GET':
		return render( request, 'registration/login.html', {
			"form": AuthenticationForm
		} )
	else:
		user = authenticate( request, username=request.POST['username'],
			password=request.POST['password'] )
		if user is None:
			return render( request, 'registration/login.html', {
				"form" : AuthenticationForm,
				"error": "Username or password is incorrect."
			} )

		login( request, user )
		request.session['user'] = user.username
		return redirect( 'index' )
