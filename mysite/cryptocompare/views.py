from django.contrib import auth
import requests
import json
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
from .forms import Cryptoform
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.views.generic.edit import DeleteView




# Crypto List with name, current price, and symbol


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']

        if User.objects.filter(email=email).exists():
            messages.info(request,'E-mail already exists')
            return redirect ('cryptocompare:register')
        elif User.objects.filter(username=username).exists():
            messages.info(request,'User Name already exists')
            return redirect ('cryptocompare:register')
        else:    
            user = User.objects.create(username=username, password=password1, email=email, first_name=first_name, last_name=last_name )
            user.save()
        return redirect('cryptocompare:login')
    else:
        return render(request, 'crypto/register.html')


def login(request):
    api = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    raw_data=requests.get(api).json()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        

        return redirect ('cryptocompare:crypto_list')

    else:
        return render(request, 'crypto/login.html', context={'datas':raw_data})


def logout(request):
    
    return redirect(request, '/')

def home(request):
    api = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    raw_data=requests.get(api).json()

    return render(request, 'crypto/home.html', context={'datas':raw_data})  


def crypto_list(request):
    api = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    raw_data=requests.get(api).json()
    
    return render(request, 'crypto/crypto_list.html', context={'datas':raw_data}) 



def portfolio_compare(request):
    print('hi')
    if request.method == 'POST':
        coin_name=request.POST.get('coin_name')
        
        print('no')
        print(coin_name)
        print(coin_name)
        if coin_name:
            try:
                Portfolio.objects.get_or_create(user=request.user, coin_name=coin_name)
                print(coin_name)
                
            except:
                MultipleObjectsReturned
                print('multiple')
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
        print('note')
        for obj in portfolio_objs:

            coin_api=f'https://api.coingecko.com/api/v3/coins/{obj.coin_name}'
            print('why')
            raw_data_single=requests.get(coin_api).json()

            print(coin_api)
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
        
    print('nope')
    print(portfolio_list,portfolio_pricelist, portfolio_image)
    print(portfolio_objs)       
        
    return render(request, 'crypto/portfolio_compare.html', {'final_list':final_list})


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
    # else:
        
    #     portfolio_objs=Portfolio.objects.filter(user=request.user)
    #     portfolio_list=[]
    #     portfolio_image=[]
    #     portfolio_pricelist=[]
    #     portfolio_daylist=[]
    #     portfolio_percentdaylist=[]
    #     portfolio_dayhighlist=[]
    #     portfolio_daylowlist=[]
    #     print('note')
    #     for obj in portfolio_objs:

    #         coin_api=f'https://api.coingecko.com/api/v3/coins/{obj.coin_name}'
    #         print('why')
    #         raw_data_single=requests.get(coin_api).json()

    #         print(coin_api)
    #         current_price=raw_data_single['market_data']['current_price']['usd']
    #         price_change_24h=raw_data_single['market_data']['price_change_24h']
    #         price_change_percentage_24h=raw_data_single['market_data']['price_change_percentage_24h']
    #         portfolio_dayhigh=raw_data_single['market_data']['high_24h']['usd']
    #         portfolio_daylow=raw_data_single['market_data']['low_24h']['usd']
    #         image=raw_data_single['image']['small']

    #         portfolio_list.append(obj.coin_name)
    #         portfolio_image.append(image)
    #         portfolio_pricelist.append(current_price)
    #         portfolio_daylist.append(float(price_change_24h))
    #         portfolio_percentdaylist.append(float(price_change_percentage_24h))
    #         portfolio_dayhighlist.append(float(portfolio_dayhigh))
    #         portfolio_daylowlist.append(float(portfolio_daylow))


    #     final_list = zip(portfolio_list,portfolio_image, portfolio_pricelist,portfolio_dayhighlist, portfolio_daylowlist, portfolio_daylist, portfolio_percentdaylist)
        
    #     print('nope')
    #     print(portfolio_list,portfolio_pricelist, portfolio_image)
    #     print(portfolio_objs)       
        
    # return render(request, 'crypto/portfolio_compare.html', {'final_list':final_list})


    
# class PortfolioDeleteView(DeleteView):
#     model = Portfolio
#     success_url ="/"
#     def get_queryset(self):
#         return Portfolio.objects.filter(pk=id)



# def delete_crypto(request, id):
#     Portfolio.objects.filter(id=id).delete
    # portfolio=get_object_or_404(Portfolio, id=id)
    # context={'portfolio':portfolio, 'id':id}
    # print(context)
    # if request.method =='DELETE':
    #     print("Richard")
    #     print(context)
    #     print(id)
    #     print(portfolio)
    #     print("Danny")
    #     portfolio.delete()
    #     portfolio.save()
    #     print("Harrison")
    #     # return redirect(reverse('cryptocompare:portfolio_compare'))
    #     context={'portfolio':portfolio}
    # print("jones")
    # print(context)
    # print(id)
    # print(portfolio)
    # return render (request, 'crypto/portfolio_compare.html', context)
# def about(request):
#     return render(request, 'crypto/about.html', {})


# def search_crypto(request):
    #  request.method == "POST"
    #  searched = request.POST['searched']
    #  cryptos=Crypto.objects.filter(name__contains=searched)
        
    #  return render(request, 'search_crypto.html', {'searched':searched, 'cryptos':cryptos})
    
 

# class CryptoListView(generic.ListView):
#     model=Crypto
#     template_name= 'crypto/crypto_list.html'
#     context_object_name = 'crypto_list'

#     def get_queryset(self):
#         return Crypto.objects.order_by('name')


# class CryptoDetailView(generic.DetailView):
#      model=Crypto 
#      template_name= 'crypto/detail.html'



# class NewsListView(generic.ListView):
#     model=News
#     template_name= 'news_list.html'
#     context_object_name = 'news_list'
    

#     def get_queryset(self):
#         return News.objects.order_by('headline')
