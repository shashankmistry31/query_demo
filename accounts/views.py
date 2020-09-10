from django.shortcuts import render
from django.http import HttpResponse
from django.http import  HttpResponseRedirect
# Create your views here.
from .forms import *
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from datetime import datetime
import requests

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
            db_timestamp = datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
            db_input = form.cleaned_data['query']
            db_type = 2
            url = "https://jkl86ei2j1.execute-api.ap-southeast-1.amazonaws.com/quality/dynamodb-update?session_key="+db_session_key+"&timestamp="+ str(db_timestamp) +"&db_input="+db_input+"&db_type=2"
            response = requests.get(url)
            #print(db_session_key,db_timestamp,db_input,db_type)
            bin = form.cleaned_data['query']

            if bin :
                query_resp = requests.get('https://zscga0herg.execute-api.ap-southeast-1.amazonaws.com/default/lexdemo?operand1='+bin)
                try:
                    query_resp.raise_for_status()
                    converted = query_resp.json()['response']['message']
                    context= {'form':form ,'converted':converted,'alert_flag': True}
                except:
                    converted = 'Sorry .Something went wrong.'
                    context= {'form':form ,'converted':converted,'alert_flag': True}
                    return render(request,'accounts/dashboard.html',context)

            # if bin.isdigit():
            #     try:
            #         converted  = int(bin,2)
            #         print(converted)
            #     except:
            #         form = BinForm()
            #         context= {'form':form ,'converted':converted,'alert_flag': True}
            #         return render(request,'accounts/dashboard.html',context)
            else:
                context= {'form':form ,'converted':converted,'alert_flag': True}
                return render(request,'accounts/dashboard.html',context)
                #messages.info(request, 'Data is incorrect!')

            # return HttpResponse('/thanks-bin/')
        else:
            return HttpResponse('/Nothanks/')
    else:
        db_session_key= request.session.session_key
        db_timestamp = datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
        url = "https://jkl86ei2j1.execute-api.ap-southeast-1.amazonaws.com/quality/dynamodb-update?session_key="+db_session_key+"&timestamp="+ str(db_timestamp) +"&db_input=NULL"+"&db_type=1"
        response = requests.get(url)
        form = BinForm()
    context= {'form':form ,'converted':converted}
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
            db_timestamp = datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
            db_input = form.cleaned_data['decimal_data']
            url = "https://jkl86ei2j1.execute-api.ap-southeast-1.amazonaws.com/quality/dynamodb-update?session_key="+db_session_key+"&timestamp="+ str(db_timestamp) +"&db_input="+db_input+"&db_type=4"
            response = requests.get(url)
            dec = form.cleaned_data['decimal_data']
            print(dec)
            if dec.isdigit():
                try:
                    converted  = bin(int(dec))[2:]
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
        db_timestamp = datetime.now().strftime("%Y-%m-%d|%H:%M:%S")
        url = "https://jkl86ei2j1.execute-api.ap-southeast-1.amazonaws.com/quality/dynamodb-update?session_key="+db_session_key+"&timestamp="+ str(db_timestamp) +"&db_input=NULL"+"&db_type=3"
        response = requests.get(url)
        form = DecForm()
    context= {'form':form ,'converted':converted}
    return render(request,'accounts/d2b.html',context)