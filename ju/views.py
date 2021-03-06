from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from .models import PastValue
import math
from .forms import Sma,BreForm
# Create your views here.
def index(request):
    
    c = PastValue.objects.all().values().order_by('date').reverse()
    Bre = BreForm(request.GET)
    SmaForm = Sma(request.GET)
    context={'lists':c,'Sma':SmaForm,'Bre':Bre}
    return render(request,'ju/index.html',context)
def sma(request):
    sh = int(request.GET['short'])
    lo = int(request.GET['long'])
    val = int(request.GET['val'])/100
    jp = int(request.GET['sjpy'])
    jpy=jp
    c = PastValue.objects.all().values().order_by('date').reverse()
    d = list(c)
    result = [['',0,0] for i in range(len(c))]
    avs=0
    avl=0
    usd=0
    flag=0
    buyusd=0
    buyjpy=0
    countbuy=0
    countsell=0
    for i in range(len(c)):
        avs=0
        avl=0
        if i > lo:
            for j in range(sh):
                avs+=float(c[i-j]['start'])
            avs/=sh
            for j in range(lo):
                avl+=float(c[i-j]['start'])
            avl/=lo
        if avs >avl and flag==0:
            flag=1
            buyusd = jpy*val
            jpy-=buyusd
            usd+=buyusd/float(c[i]['start'])
            countbuy+=1
        if avs < avl and flag==1:
            flag = 0
            buyjpy = usd*val
            usd -= buyjpy
            jpy += float(c[i]['start'])*buyjpy
            countsell+=1
            
        result[i][0]=d[-i-1]['date']
        result[i][1]=jpy
        result[i][2]=usd
    resultend = int(usd*float(d[-1]['start'])+jpy)        
    bai = resultend/jp
    jpy=int(jpy)             
    context={'result':result,'resultend':resultend,'bai':bai,'jpy':jpy,'countbuy':countbuy,'countsell':countsell}
    return render(request,'ju/result.html',context)
def update(request):
    f=0
    for k in range(80):
        a = k+1
        response = requests.get(f'https://info.finance.yahoo.co.jp/history/?code=USDJPY%3DX&sy=2015&sm=8&sd=19&ey=2021&em=11&ed=17&tm=d&p= { a }')
        bs = BeautifulSoup(response.text,'html.parser')            
        value = bs.find_all('td')
        
        
        for i in range(20):
            li = []
            for j in range(5):
                li.append(value[i*5+j+2].get_text())    
            if len(li[0])==11:
                e = ((li[0][:4])+'-'+(li[0][5:7])+'-'+li[0][8:10])
            elif len(li[0])==10:
                if li[0][-3]=='???':
                    e= li[0][:4]+'-'+li[0][5:7]+'-'+li[0][8:9]
                else:
                    e= li[0][:4]+'-'+li[0][5:6]+'-'+li[0][7:9]
            else:
                e = li[0][:4]+'-'+li[0][5:6]+'-'+li[0][7:8]
            f = PastValue.objects.filter(date=e).count()
            
            b = PastValue(date=e,start=float(li[1]),high=float(li[2]),low=float(li[3]),end=float(li[4]))
            b.save()
            
        if f==1:
            break
    
    c = PastValue.objects.all().values().order_by('date').reverse()
    Bre = BreForm(request.GET)
    SmaForm = Sma(request.GET)
    context = {'lists':c,'Bre':Bre,'Sma':SmaForm}
    return render(request,'ju/index.html',context)

def breverse(request):
    ml = int(request.GET['moveline'])
    val = int(request.GET['val'])/100
    sjpy = int(request.GET['sjpy'])
    a = PastValue.objects.all().values().order_by('date')
    jpy=sjpy
    usd=0
    results = [['',0,0] for i in range(len(a))]
    ave=0
    deviation=0
    buyusd = 0
    buyjpy = 0
    countbuy=0
    countsell=0
    for i in range(len(a)):
        ave=0
        s=0
        if i > ml:
            for j in range(ml):
                ave+=a[i-j]['start']
            ave/=ml
            for j in range(ml):
                s += (a[i-j]['start']-ave)**2
            deviation = math.sqrt(s)/ml
            
            if ave-deviation*2 > a[i]['start']:
                buyusd = jpy * val
                jpy -= buyusd
                usd += buyusd/a[i]['start']
                countbuy+=1
            if ave+deviation*2 < a[i]['start']:
                buyjpy = usd * val
                jpy += buyjpy*a[i]['start']
                usd -= buyjpy
                countsell+=1
        results[i][0]=a[i]['date']
        results[i][1]=jpy
        results[i][2]=usd
    finalresult = int(jpy+usd*a[len(a)-1]['start'])
    bai = finalresult/sjpy
    context = { 'bai':bai,'result':results ,'resultend':finalresult,'countbuy':countbuy,'countsell':countsell}    
    return render(request,'ju/result.html',context)

def bbr(request):
    mov = int(request.GET['moveline'])
    val = int(request.GET['val'])/100
    sjpy=int(request.GET['sjpy'])
    jpy=sjpy
    usd=0
    ave=0
    devi=0
    c = PastValue.objects.all().values().order_by('date')
    result = [["",0,0]for i in range(len(c))]
    cb=0
    cs=0
    for i in range(len(c)):
        ave=0
        devi=0
        if i >mov:
            for j in range(mov):
                ave+=float(c[i-j]['start'])
            ave/=mov
            for j in range(mov):
                devi+=(ave-float(c[i-j]['start']))**2
            devi=math.sqrt(devi)/mov
            if ave-devi*2 > float(c[i]['start']):
                buyusd = usd*val
                jpy += buyusd*float(c[i]['start'])
                usd-=buyusd
                cs+=1
            elif ave+devi*2 <float(c[i]['start']):
                buyjpy = jpy*val
                jpy-=buyjpy
                usd+= buyjpy/c[i]['start']
                cb+=1
        result[i][0]=c[i]['date']
        result[i][1]=jpy
        result[i][2]=usd
    end = int(jpy+usd*c[len(c)-1]['start'])
    bai=end/sjpy
    context={'result':result,'resultend':end,'bai':bai,'countbuy':cb,'countsell':cs}
    return render(request,'ju/result.html',context)
def rsi(request):
    day = int(request.GET['moveline'])
    val = int(request.GET['val'])/100
    sjpy = int(request.GET['sjpy'])
    jpy = sjpy
    usd = 0
    minus=0
    plus=0
    c = PastValue.objects.all().values().order_by('date')
    result=[["",0,0]for i in range(len(c))]
    bc=0
    sc=0
    a=0
    for i in range(len(c)):
        minus=0
        plus=0
        if day < i:
            for j in range(day):
                a = float(c[i-j-1]['start'])-float(c[i-j]['start'])
                if a < 0:
                    minus-=a
                else:
                    plus+=a
            minus/=day
            plus/=day
            rsi=plus/(plus+minus)*100
            if rsi < 30:
                buyusd = jpy*val
                jpy-=buyusd
                usd+=buyusd/c[i]['start']
                bc+=1
            elif rsi > 70:
                buyjpy=usd*val
                jpy+=buyjpy*c[i]['start']
                usd-=buyjpy
                sc+=1
        result[i][0]=c[i]['date']
        result[i][1]=jpy
        result[i][2]=usd
    end = int(jpy+usd*c[len(c)-1]['start'])
    bai = end/sjpy
    context={'result':result,'resultend':end,'bai':bai,'countbuy':bc,'countsell':sc}
    return render(request,'ju/result.html',context)     