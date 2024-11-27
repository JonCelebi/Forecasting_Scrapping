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

date="11-28_29"
actDate="1127"
endDate="1129"
estTime=15

urls=["https://www.weatherbug.com/weather-forecast/hourly/seattle-wa-98104?hour=2024"+endDate+"18",
"https://www.weatherbug.com/weather-forecast/hourly/breckenridge-co-80424?hour=2024"+endDate+"18",
"https://www.weatherbug.com/weather-forecast/hourly/norman-ok-73071?hour=2024"+endDate+"18",
"https://www.weatherbug.com/weather-forecast/hourly/grand-forks-nd-58201?hour=2024"+endDate+"18",
"https://www.weatherbug.com/weather-forecast/hourly/miami-fl-33134?hour=2024"+endDate+"18",
"https://www.weatherbug.com/weather-forecast/hourly/new-york-ny-10001?hour=2024"+endDate+"18",
"https://www.weatherbug.com/weather-forecast/hourly/west-lafayette-in-47906?hour=2024"+endDate+"18"]


p=0
while (p<7):
    if(p==0):
        hourDiff=-3
        actual = pd.DataFrame()
        actual['Hour']=pd.date_range(start="2024-"+actDate[0:2]+"-"+actDate[2:4]+" "+str(estTime-3)+":00", periods=(24-(estTime+hourDiff)+48), freq=f"{1}H")
    elif(p==1):
        hourDiff=-2
        actual = pd.DataFrame()
        actual['Hour']=pd.date_range(start="2024-"+actDate[0:2]+"-"+actDate[2:4]+" "+str(estTime-2)+":00", periods=(24-(estTime+hourDiff)+48), freq=f"{1}H")
    elif(p==(2 or 3)):
        hourDiff=-1
        actual = pd.DataFrame()
        actual['Hour']=pd.date_range(start="2024-"+actDate[0:2]+"-"+actDate[2:4]+" "+str(estTime-1)+":00", periods=(24-(estTime+hourDiff)+48), freq=f"{1}H")
    else:
        hourDiff=0
        actual = pd.DataFrame()
        actual['Hour']=pd.date_range(start="2024-"+actDate[0:2]+"-"+actDate[2:4]+" "+str(estTime)+":00", periods=(24-(estTime+hourDiff)+48), freq=f"{1}H")




    df = pd.concat(
        [
            actual,
            pd.DataFrame(
                columns=['Temperature','Precip_Chance','Feels_Like','Humidity','Wind_Speed',
        'Dew_Point']
            )
        ], axis=1
    )
    Temperature,Precip_Chance,Feels_Like,Humidity,Wind_Speed,Dew_Point,temp,temp2=[],[],[],[],[],[],[],[]



    browser = webdriver.Chrome()

    browser.get(urls[p])
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html, features='html.parser')
    s = soup.find('div',class_='largeHourlyForecastView__Container-sc-1s0yy92-0 jGqJls')
    lines = s.find_all('div',class_=['temperatureInfo__Temp-sc-6xsku9-1 dZGMNF',
                                    'temperatureInfo__FeelsLike-sc-6xsku9-2 cxbMTs',
                                    'cardDetailsItem__Value-sc-c2o75t-2 bytuOC'])



    browser.set_window_size(500,1000)
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html, features='html.parser')

    s2 = soup.find('div',class_='mobileHourlyForecastView__Container-sc-b1xhmu-0 fSaaqb')
    lines2 = s2.find_all('div',class_=['hourCardCondition__PrecipReading-sc-113pse-2 JlKXn'])
    browser.quit()


    for line in lines:
        temp.append(line.get_text().strip())

    for line in lines2:
        temp2.append(line.get_text().strip())


        
    # #0,50e
        
    i=0
    j=0
    while(j<(24-(estTime+hourDiff)+48)):
        if(i==0):
            Temperature.append(int(re.sub('\\D', '', temp[j*5])))
        if(i==1):
            Feels_Like.append(int(re.sub('\\D', '', temp[1+j*5])))
        if(i==2):
            Humidity.append(int(re.sub('\\D', '', temp[2+j*5])))
        if(i==3):
            Wind_Speed.append(int(re.sub('\\D', '', temp[3+j*5])))
        if(i==4):
            Dew_Point.append(int(re.sub('\\D', '', temp[4+j*5])))  
            i=-1
            j+=1
        i+=1 
    k=0
    while(k<(24-(estTime+hourDiff)+48)):
        Precip_Chance.append(int(re.sub('\\D', '', temp2[k])))
        k+=1


    df['Temperature']=Temperature
    df['Precip_Chance']=Precip_Chance
    df['Feels_Like']=Feels_Like
    df['Humidity']=Humidity
    df['Wind_Speed']=Wind_Speed
    df['Dew_Point']=Dew_Point


    if(p==0):
        file_name='wb'+actDate+'_'+date+'_seattle.csv'
        df2=df[(24-(estTime-3)):(24-(estTime+hourDiff)+48)]
    if(p==1):
        file_name='wb'+actDate+'_'+date+'_brecken.csv'
        df2=df[(24-(estTime-2)):(24-(estTime+hourDiff)+48)]
    if(p==2):
        file_name='wb'+actDate+'_'+date+'_norman.csv'
        df2=df[(24-(estTime-1)):(24-(estTime+hourDiff)+48)]
    if(p==3):
        file_name='wb'+actDate+'_'+date+'_grand.csv'
        df2=df[(24-(estTime-1)):(24-(estTime+hourDiff)+48)]
    if(p==4):
        file_name='wb'+actDate+'_'+date+'_miami.csv'
        df2=df[(24-estTime):(24-(estTime+hourDiff)+48)]
    if(p==5):
        file_name='wb'+actDate+'_'+date+'_ny.csv'
        df2=df[(24-estTime):(24-(estTime+hourDiff)+48)]
    if(p==6):
        file_name='wb'+actDate+'_'+date+'_laf.csv'
        df2=df[(24-estTime):(24-(estTime+hourDiff)+48)]

    folder_path="C:/Users/jonat/Downloads/vscode/forecasts_"+actDate[0:2]+"-"+actDate[2:4]+"/"
    file_path = folder_path + file_name
    df2.to_csv(file_path,index=False)

    p=p+1
