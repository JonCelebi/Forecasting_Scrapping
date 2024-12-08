import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator,HourLocator,DayLocator,MonthLocator

locations=['seattle','brecken','norman','grand','miami','ny','laf']
websites=['accu','apple','nws','wb','wund']
days=np.arange(23,28,1)

index = pd.MultiIndex.from_product([websites, locations], names=["website", "location"])

# Initialize the DataFrame with zeros for the metrics
allAverages = pd.DataFrame(0, index=index, columns=["Brier_Score", "Temp_Absolute_Error"])
allAverages["Brier_Score"] = allAverages["Brier_Score"].astype(float)
allAverages["Temp_Absolute_Error"] = allAverages["Temp_Absolute_Error"].astype(float)

averageWebsite_Brier=[]

for website in websites:
    j=0
    while (j < len(locations)):
        current_location = locations[j]
        tempArray_Brier=[]
        tempArray_Temp=[]
        for day in days:  
            forecast=pd.read_csv("C:/Users/jonat/Downloads/vscode/forecasts_11-"+str(day)+"/"+website+"11"+
                             str(day)+"_11-"+str(day+1)+"_"+str(day+2)+"_"+current_location+".csv")
            tempArray_Brier.append(forecast["Brier_Score"])
            tempArray_Temp.append(forecast['Temp_Absolute_Error'])       
            
        allAverages.loc[(website, current_location), "Brier_Score"]+=np.mean(tempArray_Brier)
        allAverages.loc[(website, current_location), "Temp_Absolute_Error"]+=np.mean(tempArray_Temp)
        j+=1 
    averageWebsite_Brier.append(allAverages.loc[website]["Brier_Score"].mean())    

print(allAverages)  

plt.bar(websites, averageWebsite_Brier,color='orange')
# Add labels and title
plt.xlabel("Website")
plt.ylabel("Average Brier Score")
plt.title("Brier Score for All Websites(Nov 24-28)")

# Display the graph
plt.show() 