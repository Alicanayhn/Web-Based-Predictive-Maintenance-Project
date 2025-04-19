import pandas as pd
import datetime as dt
import warnings
from sklearn.preprocessing import StandardScaler

def set_options():
    pd.set_option("display.max_columns",None)
    pd.set_option("display.float_format",lambda x:"%.2f" %x)
    warnings.filterwarnings("ignore")

def add_Date(dataframe):
    baslangic_tarihi = pd.to_datetime('2024-01-01 00:00:00')

    veri_sayisi = len(dataframe)

    tarihler = [baslangic_tarihi + dt.timedelta(minutes=15*i) for i in range(veri_sayisi)]

    dataframe["Date"] = tarihler

    return dataframe

def drop_useless_columns(datframe):
    datframe.drop(["_id"],axis=1,inplace=True)
    datframe.drop(["UDI"],axis=1,inplace=True)
    datframe.drop(["Product ID"],axis=1,inplace=True)
    datframe.drop(["Target"],axis=1,inplace=True)

    return datframe

def take_YMD_from_date(dataframe):
    dataframe["Year"] = dataframe["Date"].dt.year
    dataframe["Month"] = dataframe["Date"].dt.month
    dataframe["Day"] = dataframe["Date"].dt.day

    return dataframe

def take_weekdays(dataframe):
    dataframe["Weekday"] = dataframe["Date"].dt.weekday

    dataframe.loc[dataframe["Weekday"] == 0,"Weekday"] = "Monday"
    dataframe.loc[dataframe["Weekday"] == 1,"Weekday"] = "Tuesday"
    dataframe.loc[dataframe["Weekday"] == 2,"Weekday"] = "Wednesday"
    dataframe.loc[dataframe["Weekday"] == 3,"Weekday"] = "Thursday"
    dataframe.loc[dataframe["Weekday"] == 4,"Weekday"] = "Friday"
    dataframe.loc[dataframe["Weekday"] == 5,"Weekday"] = "Saturday"
    dataframe.loc[dataframe["Weekday"] == 6,"Weekday"] = "Sunday"

    return dataframe

def temp_difference(dataframe):
    dataframe['Temperature Difference'] = dataframe['Process temperature [K]'] - dataframe['Air temperature [K]']
    
    return dataframe

def take_power(dataframe):
    dataframe['Power [W]'] = (dataframe['Torque [Nm]'] * dataframe['Rotational speed [rpm]']) / 9.5488

    return dataframe

def make_categorize_tool(dataframe):
    bins = [0, 50, 100, 150, 200, 244]
    labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    dataframe['Wear Category'] = pd.cut(dataframe['Tool wear [min]'], bins=bins, labels=labels, include_lowest=True)

    return dataframe

def rpm_trq_ratio(dataframe):
    dataframe['RPM_Torque_Ratio'] = dataframe['Rotational speed [rpm]'] / dataframe['Torque [Nm]'] 

    return dataframe

def air_process_interaction(dataframe):
    dataframe["Air_Process_Interaction"] = dataframe["Air temperature [K]"] * dataframe["Process temperature [K]"]

    return dataframe

def temp_wear_interaction(dataframe):
    dataframe['Temperature_Wear_Interaction'] = dataframe['Process temperature [K]'] * dataframe['Tool wear [min]']

    return dataframe

def tool_roll_mean(dataframe):
    dataframe["ToolWear_roll_mean_1_hours"] = dataframe["Tool wear [min]"].shift(1).rolling(window=4).mean()
    dataframe["ToolWear_roll_mean_6_hours"] = dataframe["Tool wear [min]"].shift(1).rolling(window=24).mean()
    dataframe["ToolWear_roll_mean_12_hours"] = dataframe["Tool wear [min]"].shift(1).rolling(window=48).mean()    
    dataframe["ToolWear_roll_mean_24_hours"] = dataframe["Tool wear [min]"].shift(1).rolling(window=96).mean()

    dataframe.drop(index=dataframe.iloc[0:96].index,axis=0,inplace=True)

    return dataframe

def drop_date(dataframe):
    dataframe.drop(["Date"],axis=1,inplace=True)
    
    return dataframe

def drop_year(dataframe):
    dataframe.drop(["Year_2024"],axis=1,inplace=True)

    return dataframe

def degisken_turlerini_ayir(dataframe,cat_th=10,car_th=20):
    
    kategorik_degiskenler = [col for col in dataframe.columns if dataframe[col].dtype == 'O']
    sayisal_degiskenler = [col for col in dataframe.columns if dataframe[col].dtype != 'O']
    
    kat_ama_car = [col for col in dataframe.columns if dataframe[col].dtype == 'O' and dataframe[col].nunique() > car_th]
    say_ama_cat = [col for col in dataframe.columns if dataframe[col].dtype != 'O' and dataframe[col].nunique() < cat_th]
    
    kategorik_degiskenler = kategorik_degiskenler + say_ama_cat
    
    kategorik_degiskenler = [col for col in kategorik_degiskenler if col not in kat_ama_car]
    
    sayisal_degiskenler = [col for col in sayisal_degiskenler if col not in say_ama_cat]
    
    return kategorik_degiskenler,sayisal_degiskenler,kat_ama_car


def scaler(dataframe):
    kategorik_degiskenler,sayisal_degiskenler,kat_ama_car = degisken_turlerini_ayir(dataframe)
    kategorik_degiskenler = [col for col in kategorik_degiskenler if col != "Failure Type"]

    ss = StandardScaler()

    dataframe[sayisal_degiskenler] = ss.fit_transform(dataframe[sayisal_degiskenler])

    dataframe = pd.get_dummies(data=dataframe,columns=kategorik_degiskenler)

    return dataframe



def make_feature_engineering(dataframe):
    set_options()
    dataframe = add_Date(dataframe)
    dataframe = drop_useless_columns(dataframe)
    dataframe = take_YMD_from_date(dataframe)
    dataframe = take_weekdays(dataframe)
    dataframe = temp_difference(dataframe)
    dataframe = take_power(dataframe)
    dataframe = make_categorize_tool(dataframe)
    dataframe = rpm_trq_ratio(dataframe)
    dataframe = air_process_interaction(dataframe)
    dataframe = temp_wear_interaction(dataframe)
    dataframe = tool_roll_mean(dataframe)
    dataframe = drop_date(dataframe)
    dataframe = scaler(dataframe)
    dataframe = drop_year(dataframe)

    return dataframe