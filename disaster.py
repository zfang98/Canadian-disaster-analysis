import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


data=pd.read_csv('disaster.csv')
data.fillna
unique_event_type=data["EVENT TYPE"].unique()
# print (len(unique_event_type))
###----------------------------------------
## question 1
q1=pd.DataFrame(data.groupby('EVENT TYPE',as_index=False)["ESTIMATED TOTAL COST"].sum())
q1['ESTIMATED TOTAL COST IN BILLIONS']=q1['ESTIMATED TOTAL COST']/1000000000
q1=q1.sort_values(by=['ESTIMATED TOTAL COST'])
# print("first 10 rows of q1 are:")
# print (q1.head(10))
# print (q1.shape)
zero_cost=q1[q1['ESTIMATED TOTAL COST']==0]
nonzero_cost=q1[q1['ESTIMATED TOTAL COST']>0]
# print ('list of event type that has zero estimated total cost:')
# print (zero_cost.shape)
# print ('shape of nonzero rows:')
# print (nonzero_cost['EVENT TYPE'])
# plt.figure(figsize=(10,5))
# ax=plt.barh(nonzero_cost['EVENT TYPE'],nonzero_cost['ESTIMATED TOTAL COST IN BILLIONS'],color='b')
# plt.ylabel('Estiamted total cost in billions')
# plt.xlabel('Event type')
#
# plt.ylabel('Event type')
# plt.xlabel("Estimated total cost in billions")
# plt.title("Estimated total cost for each event type")
# plt.show()

###---------------------------------------------
 ##q2 number of events happend each year where DFAA payments (both federal and provincial) have been applied.
data['EVENT START DATE']=pd.to_datetime(data['EVENT START DATE'],dayfirst=True)
data['EVENT END DATE']=pd.to_datetime(data['EVENT END DATE'],dayfirst=True)
data['YEAR']=data['EVENT START DATE'].apply(lambda x:x.year)
data_extract=data[data["FEDERAL DFAA PAYMENTS"].notnull()& data["PROVINCIAL DFAA PAYMENTS"].notnull()]
count=data_extract.groupby('YEAR').size()
print (data['YEAR'].max())
print (data['YEAR'].min())
# plt.figure(figsize=(10,5))
# sns.countplot(x="YEAR",data=data_extract,color='blue')
# plt.xticks(rotation=90)
# plt.xlabel('Year',fontsize=16)
# # print ('number of unique years')
#
# plt.yticks(np.arange(0, 25, step=5))
# plt.ylabel('Number of events happened each year')
# plt.title('Number of events happened each year where DFAA payments applied ')
#
# plt.show()


### data is from 40 different years
##----------------------------------------------------
### q3  duration of flood event
data_flood=data[data['EVENT TYPE']=='Flood']
data_flood['DURATION']=data_flood["EVENT END DATE"]-data_flood["EVENT START DATE"]

data_flood['DURATION_DAYS']=data_flood['DURATION'].apply(lambda x: int(str(x)[:-14]))
duration_max=data_flood['DURATION_DAYS'].max()
id=data_flood['DURATION_DAYS'].idxmax()
print ('The duration (number of days) of the longest lasting Flood event.:')
print (duration_max)
print (id)

#---------------------------------------------
# # solve question 4
# ## most of elements in column'PLACE' are instanfard format which means the last two letters in the content is the abbreviationf of the province_unique
# ## the rest are not
abbre=['NU','QC','NT','ON','BC','AB','SK','MB','YT','NL','NL','NB','NS','PE','MB, SK',
'NS, NB, PE','NS, PE','NB, NL, NS, ON, PE, QE','NU, QC, NT, ON, BC, AB, SK, MB, YT, NL, NB, NS, PE',
'QC, ON','AB, BC, MB, SK','NB, NS, PE','NT','NL','NU, QC, NT, ON, BC, AB, SK, MB, YT, NL, NB, NS, PE','BC','QE','ON','NB, NS, PE']
province=['Nunavut','Quebec','Nothwest Territories','Ontario','British Columbia','Alberta',
'Saskatchewan','Manitoba','Yukon','Newfoundland and Labrador','Newfoundland','New Brunswick',
'Nova Scotia','Prince Edward Island','Prairie','Maritime Provinces','Northumberland Strait',
'Eastern Canada','Across Canada','St. Lawrence River','Western Canada',
'Maritime provinces','Northwest Territories','Labrador','Across Toronto, Canada, and internationally',
'Vancouver Island','Québec','Fort Albany and Kashcewan First Nation','Martime Provinces']
## abstract the last two letters in 'PLACE'

## generate a map dictionary, maping provinces' full name to two-letter abbreviations
abbre_map = zip(province,abbre)
abbre_map =dict(abbre_map)
data.loc[:,"LAST_TWO"]=data.loc[:,'PLACE'].apply(lambda x: x[-2:])
## determine if the LAST_TWO are from abbre list/ if the 'PLACE' is in stanfard format

## q4 is a smaller dataframe contains the columns we need for question 4
q4=data[['PLACE','LAST_TWO']]
q4.loc[:,'result']=""
for full, abbreviation in abbre_map.items():
    q4.loc[q4.loc[:,'PLACE'].str.contains(full),abbreviation]=abbreviation

for element in abbre:
    q4.loc[:,'result']=q4.loc[:,'result'].map(str)+q4.loc[:,element].map(str)+" "


## check if all the PLACE have been converted
data.loc[:,'PROVINCE']=q4.loc[:,'result']
##### print ('nan provinces:')--------------
# for row in range(len(data.loc[:,'PROVINCE'])):
#     if str(data.loc[row,'PROVINCE'])=='nan':
#         print (data.loc[row,'PLACE'])
        # data.loc[:,'PROVINCE']='SK,MB'
### There are still many PLACE such as Vancouver Island are not in the mapping idctionary.
 ##the above for loop list all the places that missing in PROVINCE column.
 ##These PLACES have been added in the abbre_map dictionary


##------------------------
## quwaation number 5
q5=dict()

abbre_single=['NU','QC','NT','ON','BC','AB','SK','MB','YT','NL','NL','NB','NS','PE']
for  abbre in abbre_single:
    list=(data.loc[:,'PROVINCE'].str.contains(abbre)).tolist()
    list=str(list)
    q5[abbre]=list.count('True')
q5=pd.DataFrame.from_dict(q5,orient='index')
q5['Region']=q5.index
q5.columns=['Count','Region']
q5=q5.sort_values(by='Count')


### print chart for question 5

plt.figure(figsize=(10,5))
plt.barh(q5['Region'],q5['Count'],color='blue')
plt.xlabel=('Province')
plt.ylabel=('Number of disaster events happened')
plt.title=('Number of disaster events happened in each province')
plt.show()
