import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator,HourLocator,DayLocator,MonthLocator
import seaborn as sns
from scipy.stats import norm
from scipy.stats import t
import matplotlib.lines as mlines
import scipy.stats as stats


locations=['seattle','brecken','norman','grand','miami','ny','laf']
websites=['accu','apple','nws','wb','wund']
days=np.arange(23,28,1)

index = pd.MultiIndex.from_product([websites, locations,days], names=["website", "location","days"])

# Initialize the DataFrame with zeros for the metrics
allAverages = pd.DataFrame(0, index=index, columns=["Brier_Score", "Temp_Absolute_Error","Temp_Error(forecast-obs)"])
allAverages["Brier_Score"] = allAverages["Brier_Score"].astype(float)
allAverages["Temp_Absolute_Error"] = allAverages["Temp_Absolute_Error"].astype(float)
allAverages["Temp_Error(forecast-obs)"]=allAverages["Temp_Error(forecast-obs)"].astype(float)


meansTemp=[]
errors=[]

n = 35
confidence_level = 0.95

# Step 2: Calculate t-critical value
alpha = 1 - confidence_level
df = n - 1  # Degrees of freedom
t_critical = t.ppf(1 - alpha/2, df)  # Two-tailed t-value

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
            allAverages.loc[(website, current_location,day), "Brier_Score"]+=forecast["Brier_Score"].mean()
            allAverages.loc[(website, current_location,day), "Temp_Absolute_Error"]=forecast['Temp_Absolute_Error'].mean()
            allAverages.loc[(website, current_location,day), "Temp_Error(forecast-obs)"]=forecast['Temp_Error(forecast-obs)'].mean()

        j+=1   
    meansTemp.append(allAverages.loc[website]["Temp_Error(forecast-obs)"].mean())
    sample_std = np.std(allAverages.loc[website]['Temp_Error(forecast-obs)'], ddof=1)  # Use ddof=1 for sample standard deviation
    errors.append(t_critical * (sample_std / np.sqrt(n)))

websitehist='wb'






stats.probplot(allAverages.loc[websitehist]['Temp_Error(forecast-obs)'], dist="norm", plot=plt)

# Customize plot
plt.title('Weatherbug QQ Plot')
plt.xlabel('Theoretical Quantiles')
plt.ylabel('Sample Quantiles')
plt.grid(alpha=0.3)
plt.show()



#print(allAverages)
print(allAverages.loc['accu']["Brier_Score"])
plt.figure(figsize=(10, 6))



# Histogram for the data
sns.histplot(allAverages.loc[websitehist]['Temp_Error(forecast-obs)'], bins=6, kde=True, stat="density", color='blue', alpha=0.6)
plt.title('Weatherbug Normal Distribution Plot', fontsize=16)
plt.xlabel('Temperature Error', fontsize=14)
plt.ylabel('Density', fontsize=14)
plt.legend(fontsize=12)
plt.grid(alpha=0.3)

blue_line = mlines.Line2D([], [], color='blue', label="Data Distribution")
red_line = mlines.Line2D([], [], color='red', label='Theoretical Normal Curve')

# Add manual legend
plt.legend(handles=[blue_line, red_line], loc='upper right', fontsize=10)

x = np.linspace(min(allAverages.loc[websitehist]['Temp_Error(forecast-obs)']), max(allAverages.loc[websitehist]['Temp_Error(forecast-obs)']), 35)
plt.plot(x, norm.pdf(x, allAverages.loc[websitehist]['Temp_Error(forecast-obs)'].mean(), allAverages.loc[websitehist]['Temp_Error(forecast-obs)'].std()), color='red', linewidth=2)
plt.show()


print(meansTemp)
print(errors)


plt.bar(websites, meansTemp, yerr=errors, capsize=5, color='skyblue')
# Add labels and title
plt.xlabel("Website")
plt.ylabel("Average Temperature Error")
plt.title("Average Temperature Bias with Confidence Intervals (95%) (Nov 24-28)")

# Display the graph
plt.show() 

ttt=np.arange(0,35,1)
plt.scatter(ttt,allAverages.loc[websitehist]['Temp_Error(forecast-obs)'])
plt.show()