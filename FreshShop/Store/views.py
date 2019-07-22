from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from Store.models import *

def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        seller=Seller.objects.filter(username=username)
        if seller:
            return HttpResponseRedirect('store/login.html')
        else:
            seller=Seller()
            seller.username = username
            seller.password = password
            seller.save()
            return HttpResponseRedirect('store/login.html')
    else:
        return render(request,'store/register.html')

def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user=request.COOKIES.get('username')
        s_user=request.session.get('username')
        if c_user and s_user and c_user==s_user:
            user=Seller.objects.filter(username=c_user).first()
            if user:
                return fun(request,*args,**kwargs)
        return  HttpResponseRedirect('Store/login')
    return inner
import hashlib
def set_password(password):
    result=hashlib.md5().update(password.encode()).hexdigest()
    return result
def login(request):
    response=render(request,'store/login.html')
    response.set_cookie('login_from','login_page')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username and password:
            user=Seller.objects.filter(username=username).first()
            if user:
                web_password=set_password(password)
                cookies=request.COOKIES.get('login_from')
                if user.password==web_password and cookies=='login_page':
                    response=HttpResponseRedirect('/Store/index/')
                    response.set_cookie('username',username)
                    request.session['username']=username
                    return response
    return response

def index(request):
    return render(request,'store/index.html')