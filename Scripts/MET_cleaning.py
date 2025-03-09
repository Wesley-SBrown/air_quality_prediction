import pandas as pd

df = pd.read_csv("data/Raw_MET_CA(2013_2024).csv")

# qc_data = []
# for items in df.columns:
#     if items[-2:] == "Qc":
#         qc_data.append(items)

df = df.dropna()
df = df.loc[:, ~df.columns.str.endswith("Qc")] #deletes all columns that end in Qc
df = df.loc[:, ~df.columns.str.endswith("Unit")] #deletes all columns that end in Unit
del df["Standard"] #deletes the column with "english"
del df["Julian"] #deletes the day of the year
del df["Scope"] #deletes the column with "daily"
del df["DaySoilTmpAvg.Value"]
del df["DayAsceEto.Value"]


def checker(col_name:str, unit:str) -> bool: #checks to see if all nodes are the same in a column
    print((df[col_name] == unit).all())

# checker("Standard", "english") #True
# checker("DayAirTmpAvg.Unit", "(F)") #True
# checker("DayAirTmpMax.Unit", "(F)") #True
# checker("DayAirTmpMin.Unit", "(F)") #True
# checker("DayDewPnt.Unit", "(F)") #True
# checker("DayPrecip.Unit", "(in)") #True
# checker("DayRelHumAvg.Unit", "(%)") #True
# checker("DayRelHumMax.Unit", "(%)") #True
# checker("DayRelHumMin.Unit", "(%)") #True
# checker("DaySolRadAvg.Unit", "(Ly/day)") #True
# checker("DayVapPresAvg.Unit", "(mBars)") #True
# checker("DayWindRun.Unit", "(MPH)") #True
# checker("DayWindSpdAvg.Unit", "(MPH)") #True

df = df.rename(columns={ #adding units to column names
    "DayAirTmpAvg.Value" : "DayAirTmpAvg (F)",
    "DayAirTmpMax.Value" : "DayAirTmpMax (F)",
    "DayAirTmpMin.Value" : "DayAirTmpMin (F)",
    "DayDewPnt.Value" : "DayDewPnt (F)",
    "DayPrecip.Value" : "DayPrecip (in)",
    "DayRelHumAvg.Value" : "DayRelHumAvg (%)",
    "DayRelHumMax.Value" : "DayRelHumMax (%)",
    "DayRelHumMin.Value" : "DayRelHumMin (%)",
    "DaySolRadAvg.Value" : "DaySolRadAvg (Ly/day)",
    "DayVapPresAvg.Value" : "DayVapPresAvg (mBars)",
    "DayWindRun.Value" : "DayWindRun (MPH)",
    "DayWindSpdAvg.Value" : "DayWindSpdAvg (MPH)"
})

#Decided to only use five stations worth of Data
df= df[df["Station"].isin([6, 43, 88, 211, 233])]

#6: Davis, Upper Mid
#43 Glenburn, Upper Top
#211 Gilroy, Mid
#88 Cuyama, Bottom Mid
#233 Joshua Tree, Bottom

df.to_csv("data/initial_clean_MET.csv", index = False)
#15202 rows