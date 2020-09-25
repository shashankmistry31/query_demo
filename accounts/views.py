from django.shortcuts import render
from django.http import HttpResponse
from django.http import  HttpResponseRedirect
# Create your views here.
from .forms import *
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
#from datetime import datetime
import requests #,time

def home(request):
    converted = ''
    print('OnLoad')
    if not request.session.exists(request.session.session_key):
        request.session.create()
    #print(request.session.session_key)
    if request.method == 'POST':
        print('OnAsk')
        form = BinForm(request.POST)
        if form.is_valid():
            db_session_key= request.session.session_key
            #db_timestamp = datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
            db_input = form.cleaned_data['query']
            #db_time = time.time()
            db_type = 2
            if db_input :
                #Christian AWS account url
                url = "https://t41v93n5u5.execute-api.eu-west-2.amazonaws.com/prod/processask?session_key="+db_session_key+"&db_input="+db_input+"&db_type=2"
                #Shashank AWS account url
                #url = "https://7q539nw8rl.execute-api.ap-southeast-1.amazonaws.com/default/dynamodb_update?session_key="+db_session_key+"&db_input="+db_input+"&db_type=2"
                print(url)
                query_resp = requests.get(url)
                try:
                    query_resp.raise_for_status()
                    converted = query_resp.json()['Lex Response']['message']
                    intents = query_resp.json()['Intent List']
                    context= {'form':form ,'converted':converted,'alert_flag': True,'intents':intents}
                except:
                    converted = 'Sorry .Something went wrong.'
                    context= {'form':form ,'converted':converted,'alert_flag': True}
                    return render(request,'accounts/dashboard.html',context)

            else:
                context= {'form':form ,'converted':converted,'alert_flag': True}
                return render(request,'accounts/dashboard.html',context)
                #messages.info(request, 'Data is incorrect!')

            # return HttpResponse('/thanks-bin/')
        else:
            return HttpResponse('/Nothanks/')
    else:
        db_session_key= request.session.session_key
        #db_time = time.time()
        #db_timestamp = datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
        url = "https://t41v93n5u5.execute-api.eu-west-2.amazonaws.com/prod/processask?session_key="+db_session_key+"&db_input=NULL&db_type=1"
        #mistry url
        #url = "https://7q539nw8rl.execute-api.ap-southeast-1.amazonaws.com/default/dynamodb_update?session_key="+db_session_key+"&db_input=NULL&db_type=1"
        print(url)
        response = requests.get(url)
        print(response)
        intents = response.json()['Intent List']
        print(intents)
        form = BinForm()
    context= {'form':form ,'converted':converted,'intents':intents , 'db_session_key':db_session_key}
    return render(request,'accounts/dashboard.html',context)


def d2b(request):
    converted = 0
    if not request.session.exists(request.session.session_key):
        request.session.create()
    if request.method == 'POST':
        print('Hello From here')
        form = DecForm(request.POST)
        if form.is_valid():
            db_session_key= request.session.session_key
            #db_timestamp = datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
            #db_time = time.time()
            db_input = form.cleaned_data['decimal_data']
            #Christian url
            url = "https://t41v93n5u5.execute-api.eu-west-2.amazonaws.com/prod/processask?session_key="+db_session_key+"&db_input="+db_input+"&db_type=4"
            #Shashank Url
            #url = "https://7q539nw8rl.execute-api.ap-southeast-1.amazonaws.com/default/dynamodb_update?session_key="+db_session_key+"&db_input="+db_input+"&db_type=4"
            response = requests.get(url)
            if db_input.isdigit():
                try:
                    converted  = bin(int(db_input))[2:]
                    print(converted)
                except:
                     form = DecForm()
                     context= {'form':form ,'converted':converted,'alert_flag': True}
                     return render(request,'accounts/d2b.html',context)
            else:
                context= {'form':form ,'converted':converted,'alert_flag': True}
                return render(request,'accounts/d2b.html',context)
                #messages.info(request, 'Data is incorrect!')

            # return HttpResponse('/thanks-bin/')
        else:
            return HttpResponse('/Nothanks/')
    else:
        db_session_key= request.session.session_key
        #db_timestamp = datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
        #db_time = time.time()
        #Christian url
        url = "https://t41v93n5u5.execute-api.eu-west-2.amazonaws.com/prod/processask?session_key="+db_session_key+"&db_input=NULL&db_type=3"
        #Shashank url
        #url = "https://7q539nw8rl.execute-api.ap-southeast-1.amazonaws.com/default/dynamodb_update?session_key="+db_session_key+"&db_input=NULL&db_type=4"
        response = requests.get(url)
        form = DecForm()
    context= {'form':form ,'converted':converted,'db_session_key':db_session_key}
    return render(request,'accounts/d2b.html',context)


def askintent(request,pk):
    print(pk)
    db_session_key= request.session.session_key
    #Shashank AWS url
    #url = 'https://bzchkm42h7.execute-api.ap-southeast-1.amazonaws.com/default/intent_conclusion_statement?intent='+pk
    #Christian AWS url
    url = 'https://l83nginvgb.execute-api.eu-west-2.amazonaws.com/prod/getresponse?session_key='+db_session_key+'&intent='+pk
    response = requests.get(url)
    print(response)
    return HttpResponse(response.json()['response'])
