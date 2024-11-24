import re
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


dates=["11-25","11-26"]
actDate="1124"
date=dates[0]+"_"+dates[1][3:5]

def url(p,k):
    urls=["https://www.accuweather.com/en/us/seattle/98104/hourly-weather-forecast/351409?day="+str(k),
          "https://www.accuweather.com/en/us/breckenridge/80424/hourly-weather-forecast/332155?day="+str(k),
          "https://www.accuweather.com/en/us/norman/73069/hourly-weather-forecast/330127?day="+str(k),
          "https://www.accuweather.com/en/us/grand-forks/58203/hourly-weather-forecast/329834?day="+str(k),
          "https://www.accuweather.com/en/us/miami/33128/hourly-weather-forecast/347936?day="+str(k),
          "https://www.accuweather.com/en/us/new-york/10021/hourly-weather-forecast/349727?day="+str(k),
          "https://www.accuweather.com/en/us/west-lafayette/47906/hourly-weather-forecast/2135952?day="+str(k)]        

    return urls[p]

p=0
while (p<7):

    actual = pd.DataFrame()
    actual['Hour']=pd.date_range(start="2024-"+dates[0]+" 00:00", end="2024-"+dates[1]+" 23:00", freq="h")
    df = pd.concat(
        [
            actual,
            pd.DataFrame(
                columns=['Temperature','Feels_Like','Precip_Chance','Cloud_Cover','Dew_Point',
        'Humidity','Wind_Speed','Wind_Gusts']
            )
        ], axis=1
    )

    Wind_Speed=[]
    Wind_Gusts=[]
    Humidity=[]
    Dew_Point=[]
    Cloud_Cover=[]

    Temperature=[]
    Feels_Like=[]
    Precip_Chance=[]


    temp=[]
    temp2=[]

    browser = webdriver.Chrome()
    values=[2,3]
    for day in values:

        browser.get(url(p,day))
        time.sleep(15)
        html = browser.page_source
        soup = BeautifulSoup(html, features='html.parser')

        s = soup.find('div',class_="hourly-wrapper content-module")
        lines = s.find_all('p')

        s2 = soup.find('div',class_="hourly-wrapper content-module")
        lines2 = s.find_all('div',class_=['temp','real-feel__text','precip'])

        for line in lines:
            if((line.get_text()[0:3]=="Air") or (line.get_text()[0:3]=="Max") or (line.get_text()[0:3]=="Rea") or (line.get_text()[0:3]=="Rai") or (line.get_text()[0:3]=="Sno")):
                continue
            else:
                temp.append(line.get_text())

        for line in lines2:
            temp2.append(re.sub('\\D', '', line.get_text()))
    browser.quit()

    i=0
    j=0
    while(j<48):
        if(i==0):
            Wind_Speed.append(int(re.sub('\\D', '', temp[j*8])))
        if(i==1):
            Wind_Gusts.append(int(re.sub('\\D', '', temp[1+j*8])))
        if(i==2):
            Humidity.append(int(re.sub('\\D', '', temp[2+j*8])))
        if(i==4):
            Dew_Point.append(int(re.sub('\\D', '', temp[4+j*8])))
        if(i==5):
            Cloud_Cover.append(int(re.sub('\\D', '', temp[5+j*8]))) 
            i=-1
            j+=1
        i+=1
    k=0
    while(k<48):
        Temperature.append(int(re.sub('\\D', '', temp2[k*3])))
        Feels_Like.append(int(re.sub('\\D', '', temp2[1+k*3])))
        Precip_Chance.append(int(re.sub('\\D', '', temp2[2+k*3])))
        k+=1
        
    df['Temperature']=Temperature
    df['Feels_Like']=Feels_Like
    df['Precip_Chance']=Precip_Chance
    df['Cloud_Cover']=Cloud_Cover
    df['Dew_Point']=Dew_Point
    df['Humidity']=Humidity
    df['Wind_Speed']=Wind_Speed
    df['Wind_Gusts']=Wind_Gusts

    if(p==0):
        file_name='accu'+actDate+'_'+date+'_seattle.csv'
    if(p==1):
        file_name='accu'+actDate+'_'+date+'_brecken.csv'
    if(p==2):
        file_name='accu'+actDate+'_'+date+'_norman.csv'
    if(p==3):
        file_name='accu'+actDate+'_'+date+'_grand.csv'
    if(p==4):
        file_name='accu'+actDate+'_'+date+'_miami.csv'
    if(p==5):
        file_name='accu'+actDate+'_'+date+'_ny.csv'
    if(p==6):
        file_name='accu'+actDate+'_'+date+'_laf.csv'

    folder_path="C:/Users/jonat/Downloads/vscode/forecasts_"+actDate[0:2]+"-"+actDate[2:4]+"/"

    file_path = folder_path + file_name
    df.to_csv(file_path,index=False)

    p=p+1









