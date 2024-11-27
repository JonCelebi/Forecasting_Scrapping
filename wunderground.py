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
date=dates[0]+"_"+dates[1][3:5]

def url(p,k):
    urls=["https://www.wunderground.com/hourly/us/wa/seattle/47.60,-122.33/date/2024-"+dates[k],
          "https://www.wunderground.com/hourly/us/co/breckenridge/39.48,-106.05/date/2024-"+dates[k],
          "https://www.wunderground.com/hourly/us/ok/norman/35.22,-97.44/date/2024-"+dates[k],
          "https://www.wunderground.com/hourly/us/nd/grand-forks/47.92,-97.03/date/2024-"+dates[k],
          "https://www.wunderground.com/hourly/us/fl/miami/25.77,-80.19/date/2024-"+dates[k],
          "https://www.wunderground.com/hourly/us/ny/manhattan/40.71,-74.01/date/2024-"+dates[k],
    "https://www.wunderground.com/hourly/us/in/west-lafayette/40.42,-86.91/date/2024-"+dates[k]]

    return urls[p]

p=0
while (p<7):

    actual = pd.DataFrame()
    actual['Hour']=pd.date_range(start="2024-"+dates[0]+" 00:00", end="2024-"+dates[1]+" 23:00", freq="h")
    df = pd.concat(
        [
            actual,
            pd.DataFrame(
                columns=['Temperature','Feels_Like','Precip_Chance','Precip_Amount','Cloud_Cover','Dew_Point',
        'Humidity','Wind_Speed','Pressure']
            )
        ], axis=1
    )
    Temperature=[]
    Feels_Like=[]
    Precip_Chance=[]
    Precip_Amount=[]
    Cloud_Cover=[]
    Dew_Point=[]
    Humidity=[]
    Wind_Speed=[]
    Pressure=[]
    temp=[]


    browser = webdriver.Chrome()
    values=[0,1]
    for day in values:
        browser.get(url(p,day))
        time.sleep(15)
        html = browser.page_source
        soup = BeautifulSoup(html, features='html.parser')

        s = soup.find(id="hourly-forecasts")
        lines = s.find_all('lib-display-unit')
        for line in lines:
            temp.append(line.get_text())
    browser.quit()

      

    i=0
    j=0
    while(j<48):
        if(i==0):
            Temperature.append(int(temp[j*9].split()[0]))
        if(i==1):
            Feels_Like.append(int(temp[1+j*9].split()[0]))
        if(i==2):
            Precip_Chance.append(float(temp[2+j*9].split()[0]))
        if(i==3):
            Precip_Amount.append(float(temp[3+j*9].split()[0]))
        if(i==4):
            Cloud_Cover.append(int(temp[4+j*9].split()[0]))
        if(i==5):
            Dew_Point.append(int(temp[5+j*9].split()[0]))
        if(i==6):
            Humidity.append(int(temp[6+j*9].split()[0]))
        if(i==7):
            Wind_Speed.append(int(temp[7+j*9].split()[0]))        
        if(i==8):
            Pressure.append(float(temp[8+j*9].split()[0]))
            i=-1
            j+=1
        i+=1
        
    df['Temperature']=Temperature
    df['Feels_Like']=Feels_Like
    df['Precip_Chance']=Precip_Chance
    df['Precip_Amount']=Precip_Amount
    df['Cloud_Cover']=Cloud_Cover
    df['Dew_Point']=Dew_Point
    df['Humidity']=Humidity
    df['Wind_Speed']=Wind_Speed
    df['Pressure']=Pressure


    if(p==0):
        file_name='wund'+actDate+'_'+date+'_seattle.csv'
    if(p==1):
        file_name='wund'+actDate+'_'+date+'_brecken.csv'
    if(p==2):
        file_name='wund'+actDate+'_'+date+'_norman.csv'
    if(p==3):
        file_name='wund'+actDate+'_'+date+'_grand.csv'
    if(p==4):
        file_name='wund'+actDate+'_'+date+'_miami.csv'
    if(p==5):
        file_name='wund'+actDate+'_'+date+'_ny.csv'
    if(p==6):
        file_name='wund'+actDate+'_'+date+'_laf.csv'


    folder_path="C:/Users/jonat/Downloads/vscode/forecasts_"+actDate[0:2]+"-"+actDate[2:4]+"/"
    file_path = folder_path + file_name
    df.to_csv(file_path,index=False)

    p=p+1




