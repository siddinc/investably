from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from . import forms
from app.models import Portfolio, Stock
from app.forms import StockForm
from django.views.generic import (View, TemplateView, DetailView, CreateView)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import requests
import json
from app.utility_functions import get_funds


class LogoutSuccessView(TemplateView):
    template_name = 'app/app_templates/logout_success.html'

class SignupView(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'app/registration/signup.html'

def Portfolioinit(request):
    Portfolio.objects.create(user=request.user)

def IndexView(request):
    return render(request, "app/app_templates/index.html", {})

@login_required
def DashboardView(request):
    try:
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        Portfolioinit(request) 
    symbols = [
             {
                "symbol": "GOOGL",
                "name": "Google",
                "price": 1007.7,
                "dividend_yield": 0,
                "earning_share": 22.27
            },
            {
                "symbol": "MSFT",
                "name": "Microsoft",
                "price": 85.01,
                "dividend_yield": 1.874,
                "earning_share": 2.97
            },
            {
                "symbol": "MSI",
                "name": "Motorola",
                "price": 98.74,
                "dividend_yield": 2.0266,
                "earning_share": -1.08
            },
            {
                "symbol": "NFLX",
                "name": "Netfilx",
                "price": 250.1,
                "dividend_yield": 0,
                "earning_share": 1.25
            },
            {
                "symbol": "NKE",
                "name": "Nike",
                "price": 62.59,
                "dividend_yield": 1.2189548,
                "earning_share": 2.51
            },
            {
                "symbol": "AZO",
                "name": "AutoZone",
                "price": 718.57,
                "dividend_yield": 0,
                "earning_share": 44.09
            },
            {
                "symbol": "PCLA",
                "name": "PriceLine",
                "price": 1806.06,
                "dividend_yield": 0,
                "earning_share": 42.66
            },
            {
                "symbol": "AGN",
                "name": "Allergan",
                "price": 164.2,
                "dividend_yield": 1.6432,
                "earning_share": 38.35
            },
            {
                "symbol": "CHTR",
                "name": "CharterComm",
                "price": 348.65,
                "dividend_yield": 0,
                "earning_share": 34.08
            },
            {
                "symbol": "BKL",
                "name": "BlackRock",
                "price": 509.38,
                "dividend_yield": 2.164,
                "earning_share": 30.3
            },
            {
                "symbol": "RE",
                "name": "EverestRgroup",
                "price": 241.06,
                "dividend_yield": 2.1078,
                "earning_share": 23.71
            },
            {
                "symbol": "MCK",
                "name": "McKesson",
                "price": 150.23,
                "dividend_yield": 0.8898,
                "earning_share": 22.74
            },
            {
                "symbol": "NSE",
                "name": "Norfolk Southern",
                "price": 136.89,
                "dividend_yield": 2.0185,
                "earning_share": 18.73
            },
            {
                "symbol": "SHW",
                "name": "Sherwing Williams",
                "price": 387.65,
                "dividend_yield": 0.8426,
                "earning_share": 18.61
            },
            {
                "symbol": "URI",
                "name": "United Rentals",
                "price": 161.99,
                "dividend_yield": 0,
                "earning_share": 58.72
            },
            {
                "symbol": "ANTM",
                "name": "Anthem",
                "price": 230.57,
                "dividend_yield": 1.2581,
                "earning_share": 14.36
            },
            {
                "symbol": "MTD",
                "name": "Mettler Toledo",
                "price": 601,
                "dividend_yield": 0,
                "earning_share": 14.24
            },
            {
                "symbol": "ADS",
                "name": "Alliance Data Systems",
                "price": 240.6,
                "dividend_yield": 0.9240,
                "earning_share": 14.13
            }
    ]
    user_portfolio_stocks = Stock.objects.filter(portfolio=Portfolio.objects.get(user=request.user))
    return render(request, 'app/app_templates/dashboard.html', {"symbols": symbols,"user_portfolio_stocks":user_portfolio_stocks})

@login_required
def StockAddView(request, symbol):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    form = StockForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            stock = form.save(commit=False)
            jdata = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey=xxxxxxxxxxxxxx".format(symbol))
            data = jdata.json()
            stock.portfolio = portfolio
            stock.symbol = symbol
            stock.day_open = float(data['Global Quote']['02. open'])
            stock.day_high = float(data['Global Quote']['03. high'])
            stock.day_low = float(data['Global Quote']['04. low'])
            stock.price = float(data['Global Quote']['05. price'])
            stock.previous_close = float(data['Global Quote']['08. previous close'])
            stock.change = float(data['Global Quote']['09. change'])
            stock.change_percent = (data['Global Quote']['10. change percent'][0:6])
            stock.roc = stock.change_percent
            stock.save()
            return redirect('dashboard')
    jdata1 = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey=xxxxxxxxxxxxxxx".format(symbol))
    data = jdata1.json()
    opened = data["Global Quote"]["02. open"]
    high = data["Global Quote"]["03. high"]
    low = data["Global Quote"]["04. low"]
    price = data["Global Quote"]["05. price"]
    change_percent = data["Global Quote"]["10. change percent"]
    return render(request, 'app/app_templates/stock_detail.html', {'form':form, 'symbol': symbol, "opened": opened, "high": high, "low": low, "change_percent": change_percent, "price": price})
    
@login_required
def StockEditView(request, symbol):
    stock = Stock.objects.filter(portfolio=Portfolio.objects.get(user=request.user)).get(symbol=symbol)
    print(stock)
    form = StockForm(request.POST or None, instance=stock)
    if request.method == "POST":
        
        if form.is_valid():
            stock = form.save()
            stock.save()
            return redirect('dashboard')
    jdata1 = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey=xxxxxxxxxxxxxxxxxxxx".format(symbol))
    data = jdata1.json()
    opened = data["Global Quote"]["02. open"]
    high = data["Global Quote"]["03. high"]
    low = data["Global Quote"]["04. low"]
    price = data["Global Quote"]["05. price"]
    change_percent = data["Global Quote"]["10. change percent"]
    return render(request, 'app/app_templates/stock_detail.html', {'form':form, 'symbol': symbol, "opened": opened, "high": high, "low": low, "change_percent": change_percent, "price": price})

@login_required
def StockDeleteView(request, symbol):
    stock = Stock.objects.filter(portfolio=Portfolio.objects.get(user=request.user)).get(symbol=symbol)
    stock.delete()
    return redirect('dashboard')

def stock_search(request):
    if request.method == "POST":
        symbol = request.POST.get('symbol')
        jdata = requests.get("https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey=xxxxxxxxxxxxx".format(symbol))
        data = jdata.json()
        results = []
        for item in data["bestMatches"]:
            results.append({"symbol": item["1. symbol"], "name": item["2. name"]})
        return render(request,'app/app_templates/search_results.html',{'results': results})
                
    else:
        return render(request,'app/app_templates/search_stocks.html',{})