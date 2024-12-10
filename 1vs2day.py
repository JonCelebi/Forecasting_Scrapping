import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator,HourLocator,DayLocator,MonthLocator


locations=['seattle','brecken','norman','grand','miami','ny','laf']
websites=['accu','apple','nws','wb','wund']
days=np.arange(23,28,1)

#7 locations, day1-2, 5 websites, 5 days

day1=0
day2=0

index = pd.MultiIndex.from_product([websites], names=["website"])

# Initialize the DataFrame with zeros for the metrics
allAveragesBrier = pd.DataFrame(0, index=index, columns=["Day1", "Day2"])
allAveragesTemp = pd.DataFrame(0, index=index, columns=["Day1", "Day2"])

averageWebsite_Brier1=[]


for day in days:
    for website in websites:
        j=0
        while (j < len(locations)):
            current_location = locations[j]

            forecast=pd.read_csv("C:/Users/jonat/Downloads/vscode/forecasts_11-"+str(day)+"/"+website+"11"+
                             str(day)+"_11-"+str(day+1)+"_"+str(day+2)+"_"+current_location+".csv")
            if(day==23):
                day2+=forecast['Temp_Absolute_Error'][24:48].mean()
            if(day>=24 and day<27):
                day1+=forecast['Temp_Absolute_Error'][0:24].mean()
                day2+=forecast['Temp_Absolute_Error'][24:48].mean()
            if(day==27):
                day1+=forecast['Temp_Absolute_Error'][0:24].mean()

            j+=1
    averageWebsite_Brier1.append(allAveragesBrier.loc[website]["Day1"].mean()) 

print(day1)
day1=day1/(5*7*5)
day2=day2/(5*7*5)
print(day1)



#Can just replace brier score with mean absolute error for different graph
plt.bar(["Day 2","Day 1"], [day2,day1],color='orange')
# Add labels and title
plt.xlabel("Forecast Days Out")
plt.ylabel("Average Absolute Temperature Error")
plt.title("Absolute Temperature Error for All Websites(Nov 24-28)")

# Display the graph
plt.show()

