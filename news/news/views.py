from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
import requests
from datetime import date, timedelta
from django.db import IntegrityError


def index(request):
    return render(request,'index.html')
   
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        try:
            if password1 != password2:
                messages.error(request, 'Passwords should match')
                return redirect('home')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request,'User Created Successfully')
                return redirect('home')
        except IntegrityError :
            messages.error(request, 'Username is taken')
            return redirect('home')


def signin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
       
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request,'Logged in successfully')
            print('Logged in successfully')
            print(request.user)
            return render(request, 'filter.html')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('home')
    else:
        return render(request,'index.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')
    

def filter(request):
    if request.method == 'POST':
        return render(request,'filter.html')
    else:
        return redirect('home')

def newspage(request):
    country_dict = {'India':'in','United States':'us','United Kingdom':'gb','Singapore':'sg','Germany':'de','France':'fr','Canada':'ca','Russia':'ru','Saudi Arabia':'sa','Ukraine':'ua'}
    key_lst = list(country_dict.keys())
    val_lst = list(country_dict.values())
    country = request.GET.get('Country','in')
    category = request.GET.get('Category','headline')
    search = request.GET.get('search','')
    search_btn = request.GET.get('search_btn','not_ok')
    if category == 'headlines': 
        r = requests.get(f'https://newsapi.org/v2/top-headlines?country={country}&language=en&apiKey=7c053139fa444fd1b03371509b60b9b2')
        data = json.loads(r.content)
        title = []
        link_news = []
        desc = []
        for i in range(15):
            news = data['articles'][i]['title']
            url =  data['articles'][i]['url']
            description = data['articles'][i]['description']
            title.append(news)
            link_news.append(url)
            desc.append(description)
        lst = zip(title,link_news,desc)
        string = f'Top 15 Headlines from {key_lst[val_lst.index(country)]}'
        params = {'range':range(15),'lst':lst,'country':key_lst[val_lst.index(country)],'string':string}
        return render(request,'newspage.html',params)
    
    elif category != 'headlines' and search_btn == 'not_ok':
        r = requests.get(f'https://newsapi.org/v2/top-headlines?country={country}&category={category}&language=en&apiKey=7c053139fa444fd1b03371509b60b9b2')
        data = json.loads(r.content)
        title = []
        link_news = []
        desc = []
        for i in range(15):
            news = data['articles'][i]['title']
            url =  data['articles'][i]['url']
            description = data['articles'][i]['description']
            title.append(news)
            link_news.append(url)
            desc.append(description)
        lst = zip(title,link_news,desc)
        string = f'Top 15 {category.capitalize()} News from {key_lst[val_lst.index(country)]}'
        params = {'range':range(15),'lst':lst,'country':key_lst[val_lst.index(country)],'string':string}
        return render(request,'newspage.html',params)

    elif search_btn == 'ok':
        from_news = str(date.today() - timedelta(10))
        to_news = str(date.today())
        r = requests.get(f'https://newsapi.org/v2/everything?q={search}&from={from_news}&to={to_news}&sortBy=popularity&apiKey=7c053139fa444fd1b03371509b60b9b2')
        data = json.loads(r.content)
        title = []
        link_news = []
        desc = []
        for i in range(15):
            news = data['articles'][i]['title']
            url =  data['articles'][i]['url']
            description = data['articles'][i]['description']
            title.append(news)
            link_news.append(url)
            desc.append(description)
    
        lst = zip(title,link_news,desc)
        string = f'Top 15 articles based on {search.upper()}'
        params = {'range':range(15),'lst':lst,'country':key_lst[val_lst.index(country)],'string':string}
        return render(request,'newspage.html',params)

