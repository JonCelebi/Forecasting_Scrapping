import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, AutoDateLocator,HourLocator,DayLocator,MonthLocator
from scipy.stats import pearsonr
import seaborn as sns


locations=['seattle','brecken','norman','grand','miami','ny','laf']
websites=['accu','apple','nws','wb','wund']
days=np.arange(23,28,1)
brackets = [(0, 0.10), (0.10, 0.20), (0.20, 0.30), (0.30, 0.40), (0.40, 0.50), (0.50, 0.60), (0.60, 0.70),
             (0.70, 0.80), (0.80, 0.90), (0.90, 1)]


bracket_sums_accu = {f"{low}-{high}": 0 for low, high in brackets}
bracket_sums_apple = {f"{low}-{high}": 0 for low, high in brackets}
bracket_sums_nws = {f"{low}-{high}": 0 for low, high in brackets}
bracket_sums_wb = {f"{low}-{high}": 0 for low, high in brackets}
bracket_sums_wund = {f"{low}-{high}": 0 for low, high in brackets}


bracket_sums={'accu':bracket_sums_accu,
        'apple':bracket_sums_apple,
        'nws':bracket_sums_nws,
        'wb':bracket_sums_wb,
        'wund':bracket_sums_wund}
#5 websites, 10 brackets,

lafObs = pd.read_csv("C:/Users/jonat/Downloads/vscode/observations/laf.csv")
breckenObs=pd.read_csv("C:/Users/jonat/Downloads/vscode/observations/brecken.csv")
miamiObs=pd.read_csv("C:/Users/jonat/Downloads/vscode/observations/miami.csv")
normanObs=pd.read_csv("C:/Users/jonat/Downloads/vscode/observations/norman.csv")
seattleObs=pd.read_csv("C:/Users/jonat/Downloads/vscode/observations/seattle.csv")
nyObs=pd.read_csv("C:/Users/jonat/Downloads/vscode/observations/ny.csv")
grandObs=pd.read_csv("C:/Users/jonat/Downloads/vscode/observations/grand.csv")

allObs={'seattle':seattleObs,
        'brecken':breckenObs,
        'norman':normanObs,
        'grand':grandObs,
        'miami':miamiObs,
        'ny':nyObs,
        'laf':lafObs,}

bracket_sums_real_accu={f"{low}-{high}": 0 for low, high in brackets}
bracket_sums_real_apple={f"{low}-{high}": 0 for low, high in brackets}
bracket_sums_real_nws={f"{low}-{high}": 0 for low, high in brackets}
bracket_sums_real_wb={f"{low}-{high}": 0 for low, high in brackets}
bracket_sums_real_wund={f"{low}-{high}": 0 for low, high in brackets}

bracket_sums_real={'accu':bracket_sums_real_accu,
        'apple':bracket_sums_real_apple,
        'nws':bracket_sums_real_nws,
        'wb':bracket_sums_real_wb,
        'wund':bracket_sums_real_wund}


percentage_correct_real_accu={f"{low}-{high}": 0 for low, high in brackets}
percentage_correct_real_apple={f"{low}-{high}": 0 for low, high in brackets}
percentage_correct_real_nws={f"{low}-{high}": 0 for low, high in brackets}
percentage_correct_real_wb={f"{low}-{high}": 0 for low, high in brackets}
percentage_correct_real_wund={f"{low}-{high}": 0 for low, high in brackets}

percentage_correct={'accu':percentage_correct_real_accu,
        'apple':percentage_correct_real_apple,
        'nws':percentage_correct_real_nws,
        'wb':percentage_correct_real_wb,
        'wund':percentage_correct_real_wund}



for website in websites:
    for day in days:
        j=0
        while (j < len(locations)):
            current_location = locations[j]

            forecast=pd.read_csv("C:/Users/jonat/Downloads/vscode/forecasts_11-"+str(day)+"/"+website+"11"+
                                    str(day)+"_11-"+str(day+1)+"_"+str(day+2)+"_"+current_location+".csv")
            data=forecast['Precip_Chance']/100
            realData=allObs[current_location][(24+(day-23)*24):24+(((day+2)-23)*24)]["precip_flag"].reset_index(drop=True)
            for low, high in brackets:   
            # Find values in the current bracket and sum them
                condition=(data >= low) & (data < high)
                bracket_sums[website][str(low)+"-"+str(high)] += condition.sum()
                matching_indexes = data[condition].index
                bracket_sums_real[website][str(low)+"-"+str(high)]+=np.sum(realData.loc[matching_indexes])
            j+=1
    for low, high in brackets:
        percentage_correct[website][str(low)+"-"+str(high)]=bracket_sums_real[website][str(low)+"-"+str(high)]/bracket_sums[website][str(low)+"-"+str(high)]
#count how many events from 0-10
#and then i see how many of those events actually has a precip flag

print(percentage_correct_real_accu.__len__)


x_labels = [f"{low}-{high}" for low, high in brackets]

y1=np.arange(0, 1, 0.1)
y2=np.arange(0.1, 1.1, 0.1)
# Scatter plot
plt.figure(figsize=(10, 6))
x_positions = np.arange(len(brackets))  # Numeric positions for x-axis labels
plt.plot(x_positions, list(percentage_correct_real_accu.values()), color="blue", marker="o", markersize=6, label="AccuWeather")
plt.plot(x_positions, list(percentage_correct_real_wb.values()), color="red", marker="o", markersize=6, label="Weatherbug")
plt.plot(x_positions, list(percentage_correct_real_wund.values()), color="green", marker="o", markersize=6, label="Wunderground")
plt.plot(x_positions, list(percentage_correct_real_apple.values()), color="orange", marker="o", markersize=6, label="Apple")
plt.plot(x_positions, list(percentage_correct_real_nws.values()), color="magenta", marker="o", markersize=6, label="NWS")
plt.plot(x_positions, y1, color="black")
plt.plot(x_positions, y2, color="black")
plt.fill_between(x_positions, y1, y2, color='gray', alpha=0.5, label='Expected Confidence vs. Accuracy')


# Customize plot
plt.xticks(x_positions, x_labels, rotation=45)
plt.xlabel("Predicted Probability of Precipitation(%)")
plt.yticks(np.arange(0, 1.1, 0.1))
plt.ylabel("Percentage of Events Rained")
plt.title("Precipitation Calibration for Different Websites")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()

# Show plot
plt.tight_layout()
plt.show()

m1, b1 = np.polyfit(x_positions[0:9], list(percentage_correct_real_accu.values())[0:9], 1)
m2, b2 = np.polyfit(x_positions, list(percentage_correct_real_wb.values()), 1)
m3, b3 = np.polyfit(x_positions, list(percentage_correct_real_wund.values()), 1)
m4, b4 = np.polyfit(x_positions[0:8], list(percentage_correct_real_apple.values())[0:8], 1)
m5, b5 = np.polyfit(x_positions, list(percentage_correct_real_nws.values()), 1)

print(m1,b1)
print(x_positions)

plt.plot(x_positions, m1*x_positions + b1, color='blue', label="AccuWeather")
plt.plot(x_positions, m2*x_positions + b2, color='red', label=f'Weatherbug')
plt.plot(x_positions, m3*x_positions + b3, color='green', label=f'Wunderground')
plt.plot(x_positions, m4*x_positions + b4, color='orange', label=f'Apple')
plt.plot(x_positions, m5*x_positions + b5, color='magenta', label=f'NWS')


plt.plot(x_positions, y1, color="black")
plt.plot(x_positions, y2, color="black")
plt.fill_between(x_positions, y1, y2, color='gray', alpha=0.5, label='Expected Confidence vs. Accuracy')

# Customize plot
plt.xticks(x_positions, x_labels, rotation=45)
plt.xlabel("Predicted Probability of Precipitation(%)")
plt.yticks(np.arange(0, 1.1, 0.1))
plt.ylabel("Percentage of Events Rained")
plt.title("Precipitation Calibration Regression Lines for Different Websites")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()

# Show plot
plt.tight_layout()
plt.show()

sns.regplot(data=data, x='x', y='y', ci=95)  # `ci=95` for 95% confidence interval
plt.title('Seaborn Regression Plot with Confidence Bands')
plt.grid(alpha=0.3)
plt.show()

