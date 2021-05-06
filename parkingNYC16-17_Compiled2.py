print("################## STEP 0 - DATA LOADING ##################")

import pandas as pd
import matplotlib.pyplot as plt

f = open("Parking_Violations_Issued_-_Fiscal_Year_2017.csv")
df = pd.read_csv(f)
print(len(df), "records were read from file.")

print("\n################## STEP 1 - DATA CLEANING ##################")

df_headers = df.head()
print(df_headers)

clean = df[(
            (df["Registration State"] != '99')
            & (df["Plate Type"] != '999')
)]
print(len(clean), "records left after cleaning.")

new = clean.dropna( axis = 0,
                    how = 'any',
                    subset = ['Plate ID'
                              , 'Registration State'
                              , 'Plate Type'
                              , 'Issue Date'
                              , 'Violation Code'
                              , 'Vehicle Body Type'
                              , 'Vehicle Make'
                              , 'Violation Time'
                              , 'Violation County'
                              , 'Street Name'
                              , 'Vehicle Year'])

print(len(new), "records left after dropping null values from certain columns.")

new['I_Date']=pd.to_datetime(df['Issue Date'])

dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
new['I_Month']=pd.DatetimeIndex(new['Issue Date']).month
new['I_Year']=pd.DatetimeIndex(new['Issue Date']).year
new['I_Day']=pd.DatetimeIndex(new['Issue Date']).dayofweek.map(dayOfWeek)

new = new[['Plate ID'
          , 'Registration State'
          , 'Plate Type'
          , 'Issue Date'
          , 'I_Month'
          , 'I_Year'           
          , 'I_Day'
          , 'Violation Code'
          , 'Vehicle Body Type'
          , 'Vehicle Make'
          , 'Violation Time'
          , 'Violation County'
          , 'Street Name'
          , 'Vehicle Year']]

print(new.head())

############################ Kevin's STEP ############################ 

Mo = new.groupby(['I_Month']).count().reset_index()
Mo2 = new.groupby(['I_Month']).count()
MoTotal = len(new)

print("Here's our monthly analysis on NYC parking tickets data")
print(Mo2['Plate ID'])

print("\nWhen do you plan to visit NYC? Provide month (1 ~ 12):")
target = int(input("Enter month number: "))
Ans = Mo[(Mo.I_Month == target)]
print(Ans)

print("\nIf you plan to visit NYC in below months, you better park your car in a right place at the right time")
print(Mo.nlargest(3, 'Plate ID')) ###Top3 Ticket Issued Months

Mo2['TicketRatio'] = Mo2['Plate ID'] / MoTotal

MonthAnalysis = Mo2[['Plate ID', 'TicketRatio']]
MonthCNT = MonthAnalysis[['TicketRatio']]

print("For your information, you may refer to the chart for your plan.")
MonthCNT.plot()

############################ Vira's STEP ############################ 

new.loc[((new.I_Month >= 3) & (new.I_Month <= 5)), 'Season'] = 'Spring'
new.loc[((new.I_Month >= 6) & (new.I_Month <= 8)), 'Season'] = 'Summer'
new.loc[((new.I_Month >= 9) & (new.I_Month <= 11)), 'Season'] = 'Fall'
new.loc[((new.I_Month == 12) | (new.I_Month <= 2)), 'Season'] = 'Winter'

# Summary by season about ticket 
print("\nSummary of Automobile Violations by Season")
print("===========================================")
option = input("Would you like to see the Automobile Violations Summary by Season (y/n): ")

def get_result (answer):
        if answer == "Winter":
            s = new[new["Season"]== "Winter"]
            sp = (s.groupby("Season")["I_Month"].count())
            minim = s.groupby("I_Day")["Season"].count().nsmallest(1)
            maxim = s.groupby("I_Day")["Season"].count().nlargest(1)
            print ("\nThe total number of given tickets by", sp)
            print ("\nThe maximum number of tickets was given on ", maxim)
            print ("\nThe minimum number of tickets was given on", minim)
        elif answer == "Spring":
            s = new[new["Season"]== "Spring"]
            sp = s.groupby("Season")["I_Month"].count()
            minim = s.groupby("I_Day")["Season"].count().nsmallest(1)
            maxim = s.groupby("I_Day")["Season"].count().nlargest(1) 
            print ("The total number of given tickets by", sp)
            print ("\nThe maximum number of tickets was given on ", maxim)
            print ("\nThe minimum number of tickets was given on", minim)
        elif answer == "Fall":
            s = new[new["Season"]== "Fall"]
            sp = s.groupby("Season")["I_Month"].count()
            minim = s.groupby("I_Day")["Season"].count().nsmallest(1)
            maxim = s.groupby("I_Day")["Season"].count().nlargest(1)
            print ("The total number of given tickets by", sp)
            print ("\nThe maximum number of tickets was given on ", maxim)
            print ("\nThe minimum number of tickets was given on", minim)
        else:
            s = new[new["Season"]== "Summer"]
            sp = s.groupby("Season")["I_Month"].count()
            minim = s.groupby("I_Day")["Season"].count().nsmallest(1)
            maxim = s.groupby("I_Day")["Season"].count().nlargest(1)
            print ("The total number of given tickets by", sp)
            print ("\nThe maximum number of tickets was given on ", maxim)
            print ("\nThe minimum number of tickets was given on", minim)

if option == "y": 
    answer = input("Enter name of the season (Spring, Summer, Fall, or Winter): ")           
    print(get_result(answer))
elif option == "n":
    print("You can check that information later.")   

############################### Nadia ###################################

print("\nSummary of Code Violations by season")
print("=========================================")
print("\nThe violation codes of the tickets that were given the most by each season.")
h = new.groupby(["Season", "Violation Code"])["Season"].count().nlargest(4)
print(h)

print("\nThe violation codes of the tickets that were given the least by each season.")
d = new.groupby(["Season", "Violation Code"])["Season"].count().nsmallest(4)
print(d)

print("\nSummary of Code Violations by year")
print("=========================================")
print("\nTop five parking violation codes of the tickets that were given the most during a year.")
l = new.groupby("Violation Code")["Season"].count().nlargest(5)
print(l)

print("\nTop five violation codes of the tickets that were given the least during a year.")
k = new.groupby("Violation Code")["Season"].count().nsmallest(5)
print(k)  

############################### Caroline #################################

vehicle=new[(new["Vehicle Make"]!="") & (new["Vehicle Year"]>=1970) & (new["Vehicle Year"]<=2017)]
g_vehicle=vehicle.groupby(["Vehicle Make","Vehicle Year"]).size().sort_values(ascending=False)
print("Top Three Vehicle Make & Year That Received Tickets This Fiscal Year")
print(g_vehicle.head(3))

############################### Heather #################################


County = new['Violation County'] = new['Violation County'].replace('BRONX','Bronx')
County = new['Violation County'] = new['Violation County'].replace('BX','Bronx')
County = new['Violation County'] = new['Violation County'].replace('BK','Brooklyn')
County = new['Violation County'] = new['Violation County'].replace('K','Brooklyn') #K = brooKlyn = BK
County = new['Violation County'] = new['Violation County'].replace('KINGS','Brooklyn') #KINGS = Kings County = BK
County = new['Violation County'] = new['Violation County'].replace('NY','Manhattan') #NY = Manhattan
County = new['Violation County'] = new['Violation County'].replace('MN','Manhattan') #NY = Manhattan
County = new['Violation County'] = new['Violation County'].replace('Q','Queens')
County = new['Violation County'] = new['Violation County'].replace('QN','Queens')
County = new['Violation County'] = new['Violation County'].replace('QNS','Queens')
County = new['Violation County'] = new['Violation County'].replace('R','Bronx') #R = bRonx = BX
County = new['Violation County'] = new['Violation County'].replace('ST','Staten Island')

County = new.groupby(['Violation County']).count()
print('Manhattan has issued the most tickets in the 2017 fiscal year.')
print(County)

RegState = new.groupby(['Registration State']).size().reset_index(name='count')
sorted = RegState.sort_values(by = 'count',ascending = False)
print(sorted.head(n=5))
print("In State cars are more likely to violate rules.")


############################### German #################################

print ("There is a consistency in violate the parking rules by the same cars")
plate_id = new.groupby(['Plate ID','Violation Code']).size().reset_index(name='count')
top_plateid = plate_id.sort_values(by ='count',ascending= False)
print(top_plateid)
print(" The code 46 which is the most violated by the same people is the one we know as double parking")


print ("Here we can see the top 5 plate types that received tickets in NYC ")
plate_types = new.groupby('Plate Type').size().reset_index(name='count')
top_5 = plate_types.sort_values(by ='count',ascending= False).head(5)
print(top_5)

print ("As we can see in our graph, PAS plates are the most common to receive tickets with a big difference compared to the other plate's types" )

plt.bar('Plate Type', 'count',data=top_5)
plt.title('Top 5 Plate Types with most Parking Violations')
plt.xlabel('Plate Type')
plt.ylabel('Num of Parking Violations (10,000s)')
