from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
import requests
import json
from django.contrib.auth.views import LoginView  
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from .models import Portfolio
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.edit import DeleteView
from django.contrib.auth.forms import UserCreationForm


# Crypto List with name, current price, and symbol

def home(request):
    api = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    raw_data=requests.get(api).json()
    return render(request, 'crypto/home.html', context={'datas':raw_data})  


def register(request):
    if request.method == 'POST':
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid:
                form.save()
                return redirect('cryptocompare:portfolio_compare')
    else:
        form = UserCreationForm()
    return render(request, 'crypto/register.html', {'form':form})


def crypto_login(request):
    api = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    raw_data=requests.get(api).json()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username , password = password)
        if user is not None:
            login(request , user)
            return redirect('cryptocompare:portfolio_compare')   
        else:
            messages.success(request, 'Wrong password.')
            return redirect('cryptocompare:crypto_login')
    return render(request, 'crypto/crypto_login.html', context={'datas':raw_data})


@login_required(login_url='/crypto_login/')
def logout(request):
    logout(request)
    return redirect(request, '/')


@login_required(login_url='/crypto_login/')
def crypto_list(request):
    api = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    raw_data=requests.get(api).json()
    return render(request, 'crypto/crypto_list.html', context={'datas':raw_data}) 


@login_required(login_url='/crypto_login/')
def portfolio_compare(request):
    print('hi')
    if request.method == 'POST':
        coin_name=request.POST.get('coin_name')
        if coin_name is not None:
            try:
                Portfolio.objects.get_or_create(user=request.user, coin_name=coin_name)     
            except:
                MultipleObjectsReturned
            return redirect('cryptocompare:portfolio_compare')                
    else:
        portfolio_objs=Portfolio.objects.filter(user=request.user)
        portfolio_list=[]
        portfolio_image=[]
        portfolio_pricelist=[]
        portfolio_daylist=[]
        portfolio_percentdaylist=[]
        portfolio_dayhighlist=[]
        portfolio_daylowlist=[]        
        
        for obj in portfolio_objs:
            coin_api=f'https://api.coingecko.com/api/v3/coins/{obj.coin_name}'
            raw_data_single=requests.get(coin_api).json()
            current_price=raw_data_single['market_data']['current_price']['usd']
            price_change_24h=raw_data_single['market_data']['price_change_24h']
            price_change_percentage_24h=raw_data_single['market_data']['price_change_percentage_24h']
            portfolio_dayhigh=raw_data_single['market_data']['high_24h']['usd']
            portfolio_daylow=raw_data_single['market_data']['low_24h']['usd']
            image=raw_data_single['image']['small']
            portfolio_list.append(obj.coin_name)
            portfolio_image.append(image)
            portfolio_pricelist.append(current_price)
            portfolio_daylist.append(float(price_change_24h))
            portfolio_percentdaylist.append(float(price_change_percentage_24h))
            portfolio_dayhighlist.append(float(portfolio_dayhigh))
            portfolio_daylowlist.append(float(portfolio_daylow))
        final_list = zip(portfolio_list,portfolio_image, portfolio_pricelist,portfolio_dayhighlist, portfolio_daylowlist, portfolio_daylist, portfolio_percentdaylist)
    return render(request, 'crypto/portfolio_compare.html', {'final_list':final_list})

@login_required(login_url='/crypto_login/')
def delete_crypto(request):
    if request.method == "POST":
        try:
            clear_crypto = Portfolio.objects.all()
            clear_crypto.delete()
            return HttpResponseRedirect('cryptocompare:portfolio_compare')           
        except:
            None
            print('none')
        return redirect('cryptocompare:portfolio_compare')
