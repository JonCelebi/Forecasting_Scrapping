import pandas as pd
import numpy as np


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
locations=list(allObs.keys())
websites=['accu','apple','nws','wb','wund']
days=np.arange(23,28,1)

i=0  
while (i < len(locations)):
    # Current location name
    current_location = locations[i]
    
    # Select the DataFrame for the current location
    allObs[current_location]['precip_flag']=allObs[current_location]['p01i'].apply(lambda x: 1 if (x != 'T' and float(x) >= 0.01) else 0)

    allObs[current_location].to_csv("C:/Users/jonat/Downloads/vscode/observations/"+current_location+
                     ".csv",index=False)
    
    # Increment the counter
    i += 1

print(lafObs[23:167])

random = pd.read_csv("C:/Users/jonat/Downloads/vscode/forecasts_11-27/accu1127_11-28_29_norman.csv")

print(pd.to_numeric(np.abs(random['Temperature'])))
print(allObs['norman'][(23+(23-23)*24):23+(((23+2)-23)*24)]["tmpf"].reset_index(drop=True))
print(np.abs(random['Temperature']-allObs['norman'][(23+(27-23)*24):23+(((27+2)-23)*24)]["tmpf"].reset_index(drop=True)))


#7 locations, day1-2, 4 websites



for day in days:
    for website in websites:
        j=0
        while (j < len(locations)):
            current_location = locations[j]

            forecast=pd.read_csv("C:/Users/jonat/Downloads/vscode/forecasts_11-"+str(day)+"/"+website+"11"+
                             str(day)+"_11-"+str(day+1)+"_"+str(day+2)+"_"+current_location+".csv")
            forecast['Brier_Score']=((forecast['Precip_Chance']/100)-allObs[current_location]
                                     [(24+(day-23)*24):24+(((day+2)-23)*24)]["precip_flag"].reset_index(drop=True))**2
            forecast['Temp_Absolute_Error']=np.abs(forecast['Temperature']-allObs[current_location]
                                                   [(23+(day-23)*24):23+(((day+2)-23)*24)]["tmpf"].reset_index(drop=True))
            forecast['Temp_Error(forecast-obs)']=forecast['Temperature']-allObs[current_location][(23+(day-23)*24):23+(((day+2)-23)*24)]["tmpf"].reset_index(drop=True)
            
            forecast.to_csv("C:/Users/jonat/Downloads/vscode/forecasts_11-"+str(day)+"/"+website+"11"+
                             str(day)+"_11-"+str(day+1)+"_"+str(day+2)+"_"+current_location+".csv",index=False)

            j+=1




#7 locations, day1-2, 4 websites

