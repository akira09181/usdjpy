from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from .models import PastValue
# Create your views here.
def index(request):
    lists=[]
    c = PastValue.objects.all().values()
    
    response = requests.get('https://info.finance.yahoo.co.jp/history/?code=USDJPY%3DX&sy=2015&sm=8&sd=19&ey=2021&em=11&ed=17&tm=d')
    bs = BeautifulSoup(response.text,'html.parser')
    value = bs.find_all('td')
    if c[0]['date'] == value[2].get_text():
        pass
    else:
        for k in range(80):
            a = k+1
            response = requests.get(f'https://info.finance.yahoo.co.jp/history/?code=USDJPY%3DX&sy=2015&sm=8&sd=19&ey=2021&em=11&ed=17&tm=d&p= { a }')
            bs = BeautifulSoup(response.text,'html.parser')
            value = bs.find_all('td')
        
        
            for i in range(20):
                li = []
                for j in range(5):
                    li.append(value[i*5+j+2].get_text())
                b = PastValue(date=li[0],start=float(li[1]),high=float(li[2]),low=float(li[3]),end=float(li[4]))
                b.save()
                lists.append(li)
    c = PastValue.objects.all().values()
    print(c)
    context={'lists':c}
    return render(request,'ju/index.html',context)
def sma(request):
    sh = int(request.GET['short'])
    lo = int(request.GET['long'])
    val = int(request.GET['val'])/100
    jp = int(request.GET['start'])
    jpy=jp
    c = PastValue.objects.all().values()
    d = list(c)
    result = [['',0,0] for i in range(len(c))]
    avs=0
    avl=0
    usd=0
    flag=0
    buyusd=0
    buyjpy=0
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
        if avs < avl and flag==1:
            flag = 0
            buyjpy = usd*val
            usd -= buyjpy
            jpy += float(c[i]['start'])*buyjpy
        result[i][0]=d[-i-1]['date']
        result[i][1]=jpy
        result[i][2]=usd
    resultend = int(usd*float(d[-1]['start'])+jpy)        
    bai = resultend/jp
    jpy=int(jpy)             
    context={'result':result,'resultend':resultend,'bai':bai,'jpy':jpy}
    return render(request,'ju/result.html',context)