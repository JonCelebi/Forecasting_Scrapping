import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator,HourLocator,DayLocator,MonthLocator


locations=['seattle','brecken','norman','grand','miami','ny','laf']
websites=['accu','apple','nws','wb','wund']
days=np.arange(23,28,1)

#7 locations, day1-2, 4 websites

day1=0
day2=0



for day in days:
    for website in websites:
        j=0
        while (j < len(locations)):
            current_location = locations[j]

            forecast=pd.read_csv("C:/Users/jonat/Downloads/vscode/forecasts_11-"+str(day)+"/"+website+"11"+
                             str(day)+"_11-"+str(day+1)+"_"+str(day+2)+"_"+current_location+".csv")
            if(day==23):
                day2+=forecast['Brier_Score'][24:48].mean()
            if(day>=24 and day<27):
                day1+=forecast['Brier_Score'][0:24].mean()
                day2+=forecast['Brier_Score'][24:48].mean()
            if(day==27):
                day1+=forecast['Brier_Score'][0:24].mean()

            j+=1
print(day1)
day1=day1/(4*7*5)
day2=day2/(4*7*5)
print(day1)


plt.bar(["Day 2","Day 1"], [day2,day1],color='orange')
# Add labels and title
plt.xlabel("Forecast Days Out")
plt.ylabel("Average Brier Score")
plt.title("Brier Score for All Websites(Nov 24-28)")

# Display the graph
plt.show()

