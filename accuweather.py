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

actual = pd.DataFrame()
actual['Hour']=pd.date_range(start="2024-11-02 00:00", end="2024-11-02 23:00", freq="h")
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
url = "https://www.accuweather.com/en/us/west-lafayette/47906/hourly-weather-forecast/2135952?day=2"
browser.get(url)
time.sleep(15)
html = browser.page_source
soup = BeautifulSoup(html, features='html.parser')

s = soup.find('div',class_="hourly-wrapper content-module")
lines = s.find_all('p')

s2 = soup.find('div',class_="hourly-wrapper content-module")
lines2 = s.find_all('div',class_=['temp','real-feel__text','precip'])

for line in lines:
    if((line.get_text()[0:3]=="Air") or (line.get_text()[0:3]=="Max") or (line.get_text()[0:3]=="Rea")):
        continue
    else:
        print(line.get_text())
        temp.append(line.get_text())

for line in lines2:
    print(line.get_text())
    temp2.append(re.sub('\\D', '', line.get_text()))

i=0
j=0
while(j<24):
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
print(temp2)
k=0
while(k<24):
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

#df.to_csv('wunderground11-02.csv',index=False)
print(df)




