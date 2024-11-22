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

hours=72
actual = pd.DataFrame()
actual['Hour']=pd.date_range(start="2024-11-22 04:00", periods=hours, freq=f"{1}H")
df = pd.concat(
    [
        actual,
        pd.DataFrame(
            columns=['Temperature','Precip_Chance','Feels_Like','Humidity','Wind_Speed',
       'Dew_Point']
        )
    ], axis=1
)
Temperature=[]
Precip_Chance=[]
Feels_Like=[]
Humidity=[]
Wind_Speed=[]
Dew_Point=[]

temp=[]
temp2=[]



browser = webdriver.Chrome()

url = "https://www.weatherbug.com/weather-forecast/hourly/west-lafayette-in-47906?hour=2024112410"
browser.get(url)
time.sleep(10)
html = browser.page_source
soup = BeautifulSoup(html, features='html.parser')
s = soup.find('div',class_='largeHourlyForecastView__Container-sc-1s0yy92-0 jGqJls')
lines = s.find_all('div',class_=['temperatureInfo__Temp-sc-6xsku9-1 dZGMNF',
                                 'temperatureInfo__FeelsLike-sc-6xsku9-2 cxbMTs',
                                 'cardDetailsItem__Value-sc-c2o75t-2 bytuOC'])


#browser.quit()

browser.set_window_size(500,1000)
time.sleep(10)
html = browser.page_source
soup = BeautifulSoup(html, features='html.parser')

s2 = soup.find('div',class_='mobileHourlyForecastView__Container-sc-b1xhmu-0 fSaaqb')
lines2 = s2.find_all('div',class_=['hourCardCondition__PrecipReading-sc-113pse-2 JlKXn'])
browser.quit()


for line in lines:
    print(line.get_text().strip())
    temp.append(line.get_text().strip())

for line in lines2:
    print(line.get_text().strip())
    temp2.append(line.get_text().strip())


    
# #0,50e
    
i=0
j=0
while(j<hours):
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
print(Temperature)
print(temp2)
k=0
while(k<hours):
    Precip_Chance.append(int(re.sub('\\D', '', temp2[k])))
    k+=1


df['Temperature']=Temperature
df['Precip_Chance']=Precip_Chance
df['Feels_Like']=Feels_Like
df['Humidity']=Humidity
df['Wind_Speed']=Wind_Speed
df['Dew_Point']=Dew_Point

#df.to_csv('nws10-18.csv',index=False)
print(df)