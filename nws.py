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




browser = webdriver.Chrome()
url = "https://forecast.weather.gov/MapClick.php?w0=t&w1=td&w2=wc&w3=sfcwind&w3u=1&w4=sky&w5=pop&w6=rh&w7=rain&w8=thunder&w9=snow&w10=fzg&w11=sleet&w13u=0&w15u=1&w16u=1&AheadHour=26&Submit=Submit&FcstType=digital&textField1=40.4447&textField2=-86.9119&site=ind&unit=0&dd=&bw="
browser.get(url)
html = browser.page_source
soup = BeautifulSoup(html, features='html.parser')
time.sleep(10)

s = soup.find('div',class_="contentArea")
lines = s.find_all('b')

for line in lines:
    print(line.get_text())
    temp.append(line.get_text())

#0,50
i=0
j=0
while(j<9):
    if(j==0):
        Temperature.append(int(temp[i+53]))
    if(j==1):
        Dew_Point.append(int(temp[i+77]))
    if(j==3):
        Wind_Speed.append(int(temp[i+125]))
    if(j==6):
        Cloud_Cover.append(int(temp[i+197]))
    if(j==7):
        Precip_Chance.append(int(temp[i+221]))   
    if(j==8):
        Humidity.append(int(temp[i+245]))          
    if(i==23):
        i=-1
        j+=1
    i+=1
print(Temperature)
    
df['Temperature']=Temperature
df['Precip_Chance']=Precip_Chance
df['Cloud_Cover']=Cloud_Cover
df['Dew_Point']=Dew_Point
df['Humidity']=Humidity
df['Wind_Speed']=Wind_Speed

df.to_csv('nws10-18.csv',index=False)
print(df)




