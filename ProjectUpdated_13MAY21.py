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

#print(new.head())

############################ Kevin's Part ############################ 


print("\n############################################################")
print("################### STEP 2 - DATA ANALYSIS #################")
print("############################################################")


print(f"\nThere were issued {len(new)} tickets during 2017 fiscal year in NYC.")

print("\nHere's monthly analysis on NYC parking tickets data:")

Month = new.groupby(['I_Month']).count().reset_index()
Mo = Month[['I_Month','Plate ID']]

Mo.columns = ['Month', 'Number of Tickets']

Mo2 = Month[['I_Month','Plate ID']]

print(Mo)

print("This is a line chart showing Distribution of Monthly Tickets in NYC")
sns.lineplot(data=Mo, x="Month", y="Number of Tickets").set_title('Monthly Tickets (in Millions)')

sns.despine()
plt.show()

print("It shows NYC Parking tickets peaked in June")

print("\nTop 3 months that parking tickets were issued the most:")
print("=========================================================")
print(Mo2.nlargest(3, 'Plate ID').reset_index()) ###Top3 Ticket Issued Months

############################ Vira's Part ############################ 

#Pie chart
textprops = {"frotsize": 10}
a = new.groupby("I_Day")["Violation Code"].count()
sizes = a.values 
mylabels = a.index

plt.pie(sizes, labels = mylabels, autopct = "%1.2f%%")
plt.title("Distribution of Daily Parking Tickets: \nFiscal Year 2017", bbox ={"facecolor": "0.8", "pad":5})
plt.show() 

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
print("\nRanking of ticket distribution by Counties:")
print("=========================================================")
print(sorted.head(n=5).reset_index())
print('\nManhattan has issued the most tickets in the 2017 fiscal year.')


############################### Nadia ###################################

counties = new.groupby(['Violation County', 'I_Month']).size().reset_index(name='count')
counties = counties.sort_values(by = 'count',ascending = False)
print("This line graph is displaying monthly tickets distrubition by county in NYC")

#Multiple line plots displaying monthly tickets distrubition by county
sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
sns.lineplot(data = counties, x='I_Month',y='count' ,hue='Violation County')
plt.ylabel('Number of tickets (whole numbers)', fontsize=16)
plt.xlabel('Month', fontsize=16)
plt.title("Distribution of Monthly Parking Tickets by County: \nFiscal Year 2017", fontsize=18)
plt.show()

print("\nSummary of Code Violations by year")
print("=========================================================")

print("Top five parking violation codes of the tickets that were given the most during a year.")
l = new.groupby("Violation Code")["I_Year"].count().nlargest(5)
print(l)

print("\nTop five violation codes of the tickets that were given the least during a year.")
k = new.groupby("Violation Code")["I_Year"].count().nsmallest(5)
print(k)  

max_violation_codes = new['Violation Code'].value_counts().nlargest(10)

#Bar chart displaying 10 most common ticket violation codes 
print("This bar chart is displaying ten most common parking violation codes in NYC")
sns.set(style="ticks")
plt.figure(figsize=(10,6))
sns.barplot(y=max_violation_codes.values, x=max_violation_codes.index, alpha=0.9, palette=("magma"))
plt.tick_params(labelbottom='on')
plt.ylabel('Number of tickets (100,000s)', fontsize=16)
plt.xlabel('Violation Code', fontsize=16)
plt.title('Ten most common parking violation codes in NYC', fontsize=18)
plt.show()
    
min_violation_codes = new['Violation Code'].value_counts().nsmallest(10)

#Bar chart displaying 10 least common ticket violation codes 
print("This bar chart is displaying ten least common parking violation codes in NYC")
sns.set(style="ticks")
plt.figure(figsize=(10,6))
sns.barplot(y=min_violation_codes.values, x=min_violation_codes.index, alpha=0.9, palette=("BuGn_d"))
plt.tick_params(labelbottom='on')
plt.ylabel('Number of tickets (whole numbers)', fontsize=16)
plt.xlabel('Violation Code', fontsize=16)
plt.title('Ten least common parking violation codes in NYC', fontsize=18)
plt.show() 

############################### Caroline #################################

vehicle=new[(new["Vehicle Make"]!="") & (new["Vehicle Year"]>=1970) & (new["Vehicle Year"]<=2017)]
g_vehicle=vehicle.groupby(["Vehicle Make","Vehicle Year"]).size().sort_values(ascending=False)
print("\nTop Three Vehicle Make & Year That Received Tickets This Fiscal Year")
print("=========================================================")
print(g_vehicle.head(3))

############################### Heather #################################

print("Are In State cars or Out of State cars more likely to violate the rules?")
print("========================================================================")
print("In State cars are more likely to violate rules.")
RegState = new.groupby(['Registration State']).size().reset_index(name='count')
sorted = RegState.sort_values(by = 'count',ascending = False)
print(sorted.head(n=10))

############################### German #################################

print ("\nConsistency in violating the parking rules by the same cars")
print("=========================================================")
plate_id = new.groupby(['Plate ID','Violation Code']).size().reset_index(name='count')
top_plateid = plate_id.sort_values(by ='count',ascending= False)
print(top_plateid)
print("\nThe code 46 which is the most violated by the same people is the one we know as double parking")


print ("\nThe top 5 plate types that received tickets in NYC ")
print("=========================================================")
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
print("=========================================================")
option = input("\n Would you like to see the Automobile Violations Summary by Season (y/n): ")

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
    print("\nYou can check that information later.")
    
############################ Kevin's Part ############################
print("\nSummary of Automobile Violations by Month")
print("=========================================================") 

print("\nWhen do you plan to visit NYC? Provide month (1 ~ 12): ")
target = int(input("Enter month number: "))
Ans = Mo2[(Mo2.I_Month == target)]
print(Ans,"tickets were issued in the month in 2017 fiscal year")

############################ Caroline's Part ############################ 
print("\nSummary of Automobile Violations by Borough")
print("=========================================================") 

most="y"

while most=='y':
    print("\nNYC Boroughs: Brooklyn, Bronx, Staten Island, Queens, Manhattan")    
    cty=input("Insert Borough Name: ")

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
    
    more=input("\nWould you like to look at another borough? (y/n): ")
    if more !='y':
        break

    
############################ Heather's Part ############################ 

print("\nNumber of Tickets for any Registration State")
print("=================================================")

another = "y"

while another == "y":
    state = input("\nPlease enter state abbreviation: ")
    chosen = (new[new['Registration State'] == state]).shape[0]
    print("\nIn the state of", state, chosen, "tickets were distributed.")
    a=input("\nWould you like to look at another state? (y/n):")
    if a !='y':
        break

