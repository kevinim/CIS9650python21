print("############################################################")
print("################## STEP 0 - DATA LOADING ###################")
print("############################################################")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

f = open("Parking_Violations_Issued_-_Fiscal_Year_2017.csv")
df = pd.read_csv(f)
print(len(df), "records were read from file.")
print("\n############################################################")
print("################## STEP 1 - DATA CLEANING ##################")
print("############################################################")

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

############################ Kevin's Part ############################ 


print("\n############################################################")
print("################### STEP 2 - DATA ANALYSIS #################")
print("############################################################")

print("\n# How many tickets were issued during FY'17?#")
print(len(new), "tickets were issued during FY'17.")

print("\n# How many tickets were issued during each month in FY'17?#")
print("### Here's monthly analysis on NYC parking tickets data      ####")

Mo = new.groupby(['I_Month']).count().reset_index()
Mo = Mo[['I_Month','Plate ID']]
print(Mo)

print("This is a line graph and Distribution of Monthly Tickets in NYC")
sns.lineplot(data=Mo, x="I_Month", y="Plate ID").set_title('Monthly Tickets (in Millions)')

sns.set_style("white") 
plt.figure(figsize = (6, 4))
plt.hist(
         Mo["Plate ID"], # the variable on which to create the histogram
         bins = 6, 
         color = "#000090"
         )

plt.title("Distribution of Parking Tickets(Month)", fontsize = 14, weight = "bold")
plt.xlabel("Month")
plt.ylabel("Number of Tickets")

sns.despine()
plt.show()

print("It shows NYC Parking tickets peaked in June")

print("\nThis is a list of top 3 months that parking tickets were issued.")
print(Mo.nlargest(3, 'Plate ID')) ###Top3 Ticket Issued Months


DA = new.groupby(['I_Day']).count().reset_index()
DA = DA[['I_Day','Plate ID']]
DA = DA.reindex([1,5,6,4,0,2,3])

print("This is a line graph with Days data of NYC Parking Tickets")

sns.lineplot(data=DA, x="I_Day", y="Plate ID").set_title('Tickets per Day (in Millions)')
plt.show()
print("\nFor your information, you may refer to the chart for your plan.")

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
County = new['Violation County'] = new['Violation County'].replace('R','Staten Island') 
County = new['Violation County'] = new['Violation County'].replace('ST','Staten Island')

County = new.groupby(['Violation County']).size().reset_index(name='count')
sorted = County.sort_values(by = 'count',ascending = False)
print(sorted.head(n=5))
print('Manhattan has issued the most tickets in the 2017 fiscal year.')



############################### Nadia ###################################


new.loc[((new.I_Month >= 3) & (new.I_Month <= 5)), 'Season'] = 'Spring'
new.loc[((new.I_Month >= 6) & (new.I_Month <= 8)), 'Season'] = 'Summer'
new.loc[((new.I_Month >= 9) & (new.I_Month <= 11)), 'Season'] = 'Fall'
new.loc[((new.I_Month == 12) | (new.I_Month <= 2)), 'Season'] = 'Winter'


print("\nSummary of Code Violations by year")
print("=========================================")

print("\n{len(new)} tickets were issued during 2017 fiscal year in NYC")

print("\nTop five parking violation codes of the tickets that were given the most during a year.")
l = new.groupby("Violation Code")["I_Year"].count().nlargest(5)
print(l)

print("\nTop five violation codes of the tickets that were given the least during a year.")
k = new.groupby("Violation Code")["I_Year"].count().nsmallest(5)
print(k)  

max_violation_codes = new['Violation Code'].value_counts().nlargest(10)

sns.set(style="ticks")

#Graph 1
plt.figure(figsize=(10,6))
f = sns.barplot(y=max_violation_codes.values, x=max_violation_codes.index, alpha=0.9, palette=("magma"))
plt.tick_params(labelbottom='on')
plt.ylabel('Number of tickets', fontsize=16);
plt.xlabel('Violation Code', fontsize=16);
plt.title('Ten most common parking violation codes in NYC', fontsize=18);
    
min_violation_codes = new['Violation Code'].value_counts().nsmallest(10)

#Graph 2
plt.figure(figsize=(10,6))
f = sns.barplot(y=min_violation_codes.values, x=min_violation_codes.index, alpha=0.9, palette=("BuGn_d"))
plt.tick_params(labelbottom='on')
plt.ylabel('Number of tickets', fontsize=16);
plt.xlabel('Violation Code', fontsize=16);
plt.title('Ten least common parking violation codes in NYC', fontsize=18)

############################### Caroline #################################

vehicle=new[(new["Vehicle Make"]!="") & (new["Vehicle Year"]>=1970) & (new["Vehicle Year"]<=2017)]
g_vehicle=vehicle.groupby(["Vehicle Make","Vehicle Year"]).size().sort_values(ascending=False)
print("Top Three Vehicle Make & Year That Received Tickets This Fiscal Year")
print(g_vehicle.head(3))


############################### Heather #################################


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
plt.show()

print("\n############################################################")
print("################ STEP 3 - INTERACTIVE ANALYSIS #############")
print("############################################################")

############################ Vira's Part ############################ 

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
    
############################ Kevin's Part ############################ 


print("\nWhen do you plan to visit NYC? Provide month (1 ~ 12):")
target = int(input("Enter month number: "))
Ans = Mo[(Mo.I_Month == target)]
print(Ans,"tickets were issued in the month in 2017 fiscal year")

############################ Caroline's Part ############################ 

most="y"

while most=='y':
    print("NYC Boroughs: Brooklyn, Bronx, Staten Island, Queens, Manhattan")    
    cty=input("Insert Borough Name:")

    if cty=="Bronx":
        ct=new[(new["Violation County"]=="Bronx")]
        tt=ct.groupby(["Violation County","I_Month"]).size()
        maximum=tt.sort_values(ascending=False)
        print("Month with the Most Amount of Tickets in the Bronx:")
        print(maximum.head(1))
        print()
        minimum=tt.sort_values()
        print("Month with the Least Amount of Tickets in the Bronx:")
        print(minimum.head(1))
        print()
        cty_avg=tt.mean()
        print("Average Number of Tickets Per Month in the Bronx:")
        print(cty_avg)
    elif cty=="Queens":
        ct=new[(new["Violation County"]=="Queens")]
        tt=ct.groupby(["Violation County","I_Month"]).size()
        maximum=tt.sort_values(ascending=False)
        print("Month with the Most Amount of Tickets in Queens:")
        print(maximum.head(1))
        print()
        minimum=tt.sort_values()
        print("Month with the Least Amount of Tickets in Queens:")
        print(minimum.head(1))
        print()
        cty_avg=tt.mean()
        print("Average Number of Tickets Per Month in Queens:")
        print(cty_avg)
    elif cty=="Brooklyn":
        ct=new[(new["Violation County"]=="Brooklyn")]
        tt=ct.groupby(["Violation County","I_Month"]).size()
        maximum=tt.sort_values(ascending=False)
        print("Month with the Most Amount of Tickets in Brooklyn:")
        print(maximum.head(1))
        print()
        minimum=tt.sort_values()
        print("Month with the Least Amount of Tickets in Brooklyn:")
        print(minimum.head(1))
        print()
        cty_avg=tt.mean()
        print("Average Number of Tickets Per Month in Brooklyn:")
        print(cty_avg)
    elif cty=="Manhattan":
        ct=new[(new["Violation County"]=="Manhattan")]
        tt=ct.groupby(["Violation County","I_Month"]).size()
        maximum=tt.sort_values(ascending=False)
        print("Month with the Most Amount of Tickets in Manhattan:")
        print(maximum.head(1))
        print()
        minimum=tt.sort_values()
        print("Month with the Least Amount of Tickets in Manhattan:")
        print(minimum.head(1))
        print()
        cty_avg=tt.mean()
        print("Average Number of Tickets Per Month in Manhattan:")
        print(cty_avg)
    elif cty=="Staten Island":
        ct=new[(new["Violation County"]=="Staten Island")]
        tt=ct.groupby(["Violation County","I_Month"]).size()
        maximum=tt.sort_values(ascending=False)
        print("Month with the Most Amount of Tickets in Staten Island:")
        print(maximum.head(1))
        print()
        minimum=tt.sort_values()
        print("Month with the Least Amount of Tickets in Staten Island:")
        print(minimum.head(1))
        print()
        cty_avg=tt.mean()
        print("Average Number of Tickets Per Month in Staten Island:")
        print(cty_avg)
    
    more=input("Would you like to look at another borough? (y/n):")
    if more !='y':
        break

############################ Vira's Part ############################ 
    

print("\nParking situation in the city")
print("===============================")
question = input("Enter a date in d/m/yy format: ")
holiday = (new[new['Issue Date'] == question]).shape[0]
print("On this day,", holiday, "tickets were distributed.")
if holiday > 1000:
    print("Due to parking ticket distribution on this day, parking can be an issue.")
else:
    print("Due to parking ticket distribution on this day, parking should not be an issue.")  
