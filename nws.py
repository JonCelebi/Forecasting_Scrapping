import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator,HourLocator,DayLocator,MonthLocator


dates=["11-28","11-29"]
actDate="1127"
estTime=14
date=dates[0]+"_"+dates[1][3:5]

def url(p,k):
    urls=["https://forecast.weather.gov/MapClick.php?w0=t&w1=td&w2=wc&w3=sfcwind&w3u=1&w4=sky&w5=pop&w6=rh&w7=rain&w8=thunder&w9=snow&w10=fzg&w11=sleet&w13u=0&w16u=1&AheadHour="+str(24-(estTime-3)+k)+"&Submit=Submit&FcstType=digital&textField1=47.6218&textField2=-122.3503&site=all&unit=0&dd=&bw=",
          "https://forecast.weather.gov/MapClick.php?w0=t&w1=td&w2=wc&w3=sfcwind&w3u=1&w4=sky&w5=pop&w6=rh&w7=rain&w8=thunder&w9=snow&w10=fzg&w11=sleet&w13u=0&w16u=1&w17u=1&pqpfhr=6&psnwhr=6&AheadHour="+str(24-(estTime-2)+k)+"&Submit=Submit&FcstType=digital&textField1=39.4979&textField2=-106.0471&site=all&unit=0&dd=&bw=",
    "https://forecast.weather.gov/MapClick.php?w0=t&w1=td&w2=wc&w3=sfcwind&w3u=1&w4=sky&w5=pop&w6=rh&w7=rain&w8=thunder&w9=snow&w10=fzg&w11=sleet&w13u=0&w14u=1&w15u=1&AheadHour="+str(24-(estTime-1)+k)+"&Submit=Submit&FcstType=digital&textField1=35.223&textField2=-97.439&site=all&unit=0&dd=&bw=",
    "https://forecast.weather.gov/MapClick.php?w0=t&w1=td&w2=wc&w3=sfcwind&w3u=1&w4=sky&w5=pop&w6=rh&w7=rain&w8=thunder&w9=snow&w10=fzg&w11=sleet&w13u=0&w16u=1&pqpfhr=6&psnwhr=6&AheadHour="+str(24-(estTime-1)+k)+"&Submit=Submit&FcstType=digital&textField1=47.917&textField2=-97.0555&site=all&unit=0&dd=&bw=",
    "https://forecast.weather.gov/MapClick.php?w0=t&w1=td&w2=hi&w3=sfcwind&w3u=1&w4=sky&w5=pop&w6=rh&w7=rain&w8=thunder&w10u=0&w12u=1&w13u=1&pqpfhr=6&AheadHour="+str(24-(estTime)+k)+"&Submit=Submit&FcstType=digital&textField1=25.77&textField2=-80.2&site=all&unit=0&dd=&bw=",
    "https://forecast.weather.gov/MapClick.php?w0=t&w1=td&w2=wc&w3=sfcwind&w3u=1&w4=sky&w5=pop&w6=rh&w7=rain&w8=thunder&w9=snow&w10=fzg&w11=sleet&AheadHour="+str(24-(estTime)+k)+"&Submit=Submit&FcstType=digital&textField1=40.7198&textField2=-73.993&site=all&unit=0&dd=&bw=",
    "https://forecast.weather.gov/MapClick.php?w0=t&w1=td&w2=wc&w3=sfcwind&w3u=1&w4=sky&w5=pop&w6=rh&w7=rain&w8=thunder&w9=snow&w10=fzg&w11=sleet&w13u=0&w15u=1&w16u=1&AheadHour="+str(24-(estTime)+k)+"&Submit=Submit&FcstType=digital&textField1=40.4447&textField2=-86.9119&site=all&unit=0&dd=&bw="]

    return urls[p]

p=0
while (p<7):
    actual = pd.DataFrame()
    actual['Hour']=pd.date_range(start="2024-"+dates[0]+" 00:00", end="2024-"+dates[1]+" 23:00", freq="h")
    df = pd.concat(
        [
            actual,
            pd.DataFrame(
                columns=['Temperature','Precip_Chance','Cloud_Cover','Dew_Point',
        'Humidity','Wind_Speed']
            )
        ], axis=1
    )
    Temperature=[]
    Precip_Chance=[]
    Cloud_Cover=[]
    Dew_Point=[]
    Humidity=[]
    Wind_Speed=[]

    temp=[]
    temp2=[]

    browser = webdriver.Chrome()
    values=[0,24]

    browser.get(url(p,values[0]))
    html = browser.page_source
    soup = BeautifulSoup(html, features='html.parser')
    time.sleep(15)

    s = soup.find('div',class_="contentArea")
    lines = s.find_all('b')

    for line in lines:
        temp.append(line.get_text())

    browser.get(url(p,values[1]))
    html = browser.page_source
    soup = BeautifulSoup(html, features='html.parser')
    time.sleep(15)

    s = soup.find('div',class_="contentArea")
    lines = s.find_all('b')

    for line in lines:
        temp2.append(line.get_text())
    browser.quit()


    if(p==0):
        file_name='nws'+actDate+'_'+date+'_seattle.csv'
        offset=50
    if(p==1):
        file_name='nws'+actDate+'_'+date+'_brecken.csv'
        offset=67
    if(p==2):
        file_name='nws'+actDate+'_'+date+'_norman.csv'
        offset=51
    if(p==3):
        file_name='nws'+actDate+'_'+date+'_grand.csv'
        offset=64
    if(p==4):
        file_name='nws'+actDate+'_'+date+'_miami.csv'
        offset=55
    if(p==5):
        file_name='nws'+actDate+'_'+date+'_ny.csv'
        offset=48
    if(p==6):
        file_name='nws'+actDate+'_'+date+'_laf.csv'
        offset=54

    i=0
    j=0
    while(j<9):
        if(j==0):
            Temperature.append(int(temp[i+offset]))
        if(j==1):
            Dew_Point.append(int(temp[i+24+offset]))
        if(j==3):
            Wind_Speed.append(int(temp[i+72+offset]))
        if(j==6):
            Cloud_Cover.append(int(temp[i+144+offset]))
        if(j==7):
            Precip_Chance.append(int(temp[i+168+offset]))   
        if(j==8):
            Humidity.append(int(temp[i+192+offset]))          
        if(i==23):
            i=-1
            j+=1
        i+=1
    i=0
    j=0
    while(j<9):
        if(j==0):
            Temperature.append(int(temp2[i+offset]))
        if(j==1):
            Dew_Point.append(int(temp2[i+24+offset]))
        if(j==3):
            Wind_Speed.append(int(temp2[i+72+offset]))
        if(j==6):
            Cloud_Cover.append(int(temp2[i+144+offset]))
        if(j==7):
            Precip_Chance.append(int(temp2[i+168+offset]))   
        if(j==8):
            Humidity.append(int(temp2[i+192+offset]))          
        if(i==23):
            i=-1
            j+=1
        i+=1


        
    df['Temperature']=Temperature
    df['Precip_Chance']=Precip_Chance
    df['Cloud_Cover']=Cloud_Cover
    df['Dew_Point']=Dew_Point
    df['Humidity']=Humidity
    df['Wind_Speed']=Wind_Speed

    folder_path="C:/Users/jonat/Downloads/vscode/forecasts_"+actDate[0:2]+"-"+actDate[2:4]+"/"
    file_path = folder_path + file_name
    df.to_csv(file_path,index=False)

    p=p+1




