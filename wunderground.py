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
url = "https://www.wunderground.com/hourly/us/in/west-lafayette/KLAF/date/2024-11-02"
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, features='html.parser')
time.sleep(15)

s = soup.find(id="hourly-forecasts")
lines = s.find_all('lib-display-unit')

for line in lines:
    print(line.get_text())
    temp.append(line.get_text())

i=0
j=0
while(j<24):
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
print(Temperature)
    
df['Temperature']=Temperature
df['Feels_Like']=Feels_Like
df['Precip_Chance']=Precip_Chance
df['Precip_Amount']=Precip_Amount
df['Cloud_Cover']=Cloud_Cover
df['Dew_Point']=Dew_Point
df['Humidity']=Humidity
df['Wind_Speed']=Wind_Speed
df['Pressure']=Pressure

df.to_csv('wunderground11-02.csv',index=False)
print(df)




