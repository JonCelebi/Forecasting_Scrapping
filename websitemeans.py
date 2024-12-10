import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator,HourLocator,DayLocator,MonthLocator
import seaborn as sns
from scipy.stats import norm

locations=['seattle','brecken','norman','grand','miami','ny','laf']
websites=['accu','apple','nws','wb','wund']
days=np.arange(23,28,1)

index = pd.MultiIndex.from_product([websites, locations], names=["website", "location"])

# Initialize the DataFrame with zeros for the metrics
allAverages = pd.DataFrame(0, index=index, columns=["Brier_Score", "Temp_Absolute_Error","Temp_Error(forecast-obs)"])
allAverages["Brier_Score"] = allAverages["Brier_Score"].astype(float)
allAverages["Temp_Absolute_Error"] = allAverages["Temp_Absolute_Error"].astype(float)
allAverages["Temp_Error(forecast-obs)"]=allAverages["Temp_Error(forecast-obs)"].astype(float)

index2 = pd.MultiIndex.from_product([websites], names=["website"])

# Initialize the DataFrame with zeros for the metrics
allAveragesBrierDay = pd.DataFrame(0, index=index2, columns=["Day1", "Day2"])
allAveragesTempDay = pd.DataFrame(0, index=index2, columns=["Day1", "Day2"])
averageBrierDay1=[]
averageBrierDay2=[]
averageTempDay=[]

averageWebsite_Brier=[]
averageWebsite_Error=[]

for website in websites:
    j=0
    while (j < len(locations)):
        current_location = locations[j]
        tempArray_Brier=[]
        tempArray_Temp=[]
        tempArray_Error=[]
        for day in days:  
            forecast=pd.read_csv("C:/Users/jonat/Downloads/vscode/forecasts_11-"+str(day)+"/"+website+"11"+
                             str(day)+"_11-"+str(day+1)+"_"+str(day+2)+"_"+current_location+".csv")
            tempArray_Brier.append(forecast["Brier_Score"])
            tempArray_Temp.append(forecast['Temp_Absolute_Error'])
            tempArray_Error.append(forecast['Temp_Error(forecast-obs)']) 

            if(day==23):
                allAveragesBrierDay.loc[(website), "Day2"]+=forecast['Temp_Absolute_Error'][24:48].mean()
            if(day>=24 and day<27):
                allAveragesBrierDay.loc[(website), "Day1"]+=forecast['Temp_Absolute_Error'][0:24].mean()
                allAveragesBrierDay.loc[(website), "Day2"]+=forecast['Temp_Absolute_Error'][24:48].mean()
            if(day==27):
                allAveragesBrierDay.loc[(website), "Day1"]+=forecast['Temp_Absolute_Error'][0:24].mean()        
            
        allAverages.loc[(website, current_location), "Brier_Score"]+=np.mean(tempArray_Brier)
        allAverages.loc[(website, current_location), "Temp_Absolute_Error"]+=np.mean(tempArray_Temp)
        allAverages.loc[(website, current_location), "Temp_Error(forecast-obs)"]+=np.mean(tempArray_Error)

        j+=1 
    averageWebsite_Brier.append(allAverages.loc[website]["Brier_Score"].std()) 
    averageWebsite_Error.append(allAverages.loc[website]["Temp_Absolute_Error"].std())    

    averageBrierDay1.append(allAveragesBrierDay.loc[website]["Day1"]/(5*7))
    averageBrierDay2.append(allAveragesBrierDay.loc[website]["Day2"]/(5*7))


x = np.arange(len(websites))  # positions for main categories
width = 0.35  # width of each bar

fig, ax = plt.subplots()

ax.bar(x + width/2, [2.189286,1.779762,1.811905,1.782143,2.054762], width, label='Day1')
ax.bar(x - width/2, [2.291667,2.008333,2.007143,1.846429,2.232143], width, label='Day2')

ax.set_xlabel('Website')
ax.set_ylabel('Average Brier Score')
ax.set_title('Average Brier Score for Different Websites')
ax.set_xticks(x)
ax.set_xticklabels(websites)
ax.legend()

plt.show()



plt.bar(websites, averageWebsite_Brier,color='purple')
# Add labels and title
plt.xlabel("Website")
plt.ylabel("Average Website Brier Score Standard Deviation")
plt.title("Brier Score Standard Deviation (Nov 24-28)")

# Display the graph
plt.show() 
