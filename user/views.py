from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    if 'next' in request.GET:
        request.session['next']=request.GET['next']
    return render(request,'user/login.html',)



def login_post(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        request.session['uid']=user.id
        return HttpResponseRedirect(request.session['next'] if 'next' in request.session else '/')
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Wrong password")

@login_required
def logout_view(request):
    logout(request)
    request.session.clear()
    return HttpResponseRedirect('/user/login')