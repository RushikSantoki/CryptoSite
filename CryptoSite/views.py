import plotly.graph_objs
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from CryptoSite import apiCall, models
from plotly.offline import plot
from plotly.graph_objs import Scatter

from CryptoSite.forms import UserUpdateForm


def welcomePage(request):
    prices = apiCall.downloadingData()
    slugs = ['bitcoin',
             'ethereum',
             'dogecoin',
             'tether',
             'binancecoin',
             'cardano',
             'solana',
             'terra-luna']
    apiCall.downloadIcons(slugs)
    if request.user.is_active:
        active = True
        return render(request, 'CryptoSite/homepage.html', {'prices': prices, 'active': active})
    else:
        print("This is being Called")
        return render(request, 'CryptoSite/homepage.html', {'prices': prices})


def aboutPage(request):
    return render(request, 'CryptoSite/about.html')


def signInPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'CryptoSite/signIn.html',
                          {'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('mainPage')
        # return render(request, 'CryptoSite/signIn.html', {'form': AuthenticationForm()})
    else:
        pass
    return render(request, 'CryptoSite/signIn.html')


def signUpPage(request):
    if request.method == "GET":
        print("GET method called")
        return render(request, 'CryptoSite/signUp.html')
    else:
        if request.POST['password1'] == request.POST['password2'] and len(request.POST['username']) > 0 and len(
                request.POST['password1']) > 5 and len(request.POST['first_name']) > 0 and len(
                request.POST['last_name']) > 0:
            print('Matched password')
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'])
                user.save()
                login(request, user)
                return redirect('mainPage')
            except IntegrityError:
                return render(request, 'CryptoSite/signUp.html',
                              {'error': 'Username is already been taken, Please choose another username'})
        else:
            if request.POST['username'] == '' or request.POST['password1'] == '' or request.POST['first_name'] == '' or \
                    request.POST['last_name'] == '':
                return render(request, 'CryptoSite/signUp.html', {'error': 'Enter all Fields'})
            elif request.POST['password1'] != request.POST['password2']:
                return render(request, 'CryptoSite/signUp.html', {'error': 'Password did not match'})
            else:
                return render(request,'CryptoSite/signUp.html', {'error':'Error while creating user'})


def profile(request):
    u_form = UserUpdateForm(instance=request.user)
    data = models.currencyUser.objects.filter(unique=request.user.username)
    context = {
        'user': request.user,
        'data': data,
        'u_form': u_form,
    }
    return render(request, 'CryptoSite/profile.html', context)


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('http://127.0.0.1:8000/')


def success(request, rank, coins):
    data = models.Status.objects.get(currency_rank=rank)
    try:
        models.currencyUser(rank,
                            request.user.username,
                            coins,
                            data.currency_name,
                            data.currency_price,
                            str(float(coins) * float(data.currency_price))).save()
    except:
        print("Error occured while saving Data")
    return render(request, 'CryptoSite/success.html')


def confirm(request, rank, coins):
    data = models.Status.objects.get(currency_rank=rank)
    url = models.Icons.objects.get(name=data.currency_name).icon
    return render(request, 'CryptoSite/confirm.html',
                  {'user': request.user, 'data': data, 'image': url, 'coins': coins})


def buyPage(request, curr_rank):
    data = models.Status.objects.get(currency_rank=curr_rank)
    url = models.Icons.objects.get(name=data.currency_name).icon
    if request.method == 'POST':
        print('Buypage Here')
        amount = request.POST['amount']
        coins = float(amount) / float(data.currency_price)
        return redirect('confirm', rank=curr_rank, coins=str(coins))
    else:
        conversion = 1 / float(data.currency_price)
        return render(request, 'CryptoSite/buy.html',
                      {'user': request.user, 'data': data, 'image': url, 'conversion': conversion})


def mainPage(request):
    currencies = {
        'bitcoin': '1',
        'ethereum': '1027',
        'dogecoin': '74',
        'tether': '825',
        'bnb': '1839',
        'cardano': '2010',
        'solana': '5426',
        'terra-luna': '4172'
    }

    for key, value in currencies.items():
        apiCall.downloadingSpecificData(key, value)

    items = models.Status.objects.all()

    return render(request, 'CryptoSite/main.html', {'data': items})


def detailPage(request, rank):
    data1 = models.Status.objects.get(currency_rank=rank)
    graphTitle = 'Fluctuation of ' + data1.currency_name
    y_data = [float(data1.percent_change_90d), float(data1.percent_change_60d), float(data1.percent_change_30d),
              float(data1.percent_change_7d), float(data1.percent_change_24h), float(data1.percent_change_1h)]
    xticks = ['90d', '60d', '30d', '7d', '24h', 'Now']
    fig = plotly.graph_objs.Figure()
    fig.add_trace(Scatter(x=xticks, y=y_data,
                          mode='lines', name='Crypto',
                          opacity=0.7, marker_color='blue'))
    fig.update_layout(
        title={
            'text': graphTitle,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Time",
        yaxis_title="Percent Change(%)"
    )
    plot_div = plot(fig,
                    output_type='div')
    print(data1.currency_name)
    for i in models.Icons.objects.all():
        print(i.name)
    url = models.Icons.objects.get(name=data1.currency_name).icon
    return render(request, 'CryptoSite/detail.html',
                  {'data1': data1, 'plot_div': plot_div, 'image': url, 'active': request.user.is_active})
