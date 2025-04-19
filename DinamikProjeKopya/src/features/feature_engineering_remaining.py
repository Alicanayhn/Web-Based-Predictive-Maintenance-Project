import pandas as pd 
import numpy as np
from sklearn.preprocessing import StandardScaler
import warnings

def set_options():
    pd.set_option("display.max_columns",None)
    pd.set_option("display.float_format",lambda x:"%.2f" %x)
    warnings.filterwarnings("ignore")

def label_target(dataframe):
    dataframe['Air_Leak_Failure'] = 0

    down_periods = [
        ('2020-04-18 00:00:00', '2020-04-18 23:59:00'),
        ('2020-05-29 23:30:00', '2020-05-30 06:00:00'),
        ('2020-06-05 10:00:00', '2020-06-07 14:30:00'),
        ('2020-07-15 14:30:00', '2020-07-15 19:00:00')
    ]

    for start, end in down_periods:
        dataframe.loc[(dataframe['timestamp'] >= start) & (dataframe['timestamp'] <= end), 'Air_Leak_Failure'] = 1
    
    return dataframe

def drop_useless(dataframe):
    dataframe.drop(['_id'],axis=1,inplace=True)
    dataframe.drop('Unnamed: 0',axis=1,inplace=True)
    dataframe.drop(index=dataframe[dataframe["timestamp"] > "2020-07-15 19:00:00"].index,inplace=True)
    dataframe.drop(index=dataframe[(dataframe["timestamp"] >= "2020-02-01 00:00:00") & ((dataframe["timestamp"] < "2020-04-18 00:00:00"))].index,inplace=True)

    return dataframe

def change_times_type(dataframe):
    dataframe["timestamp"] =  pd.to_datetime(dataframe["timestamp"],format='%Y-%m-%d %H:%M:%S')

    return dataframe

def drop_high_korelation(dataframe):
    dataframe.drop(["TP3","COMP","DV_eletric","Oil_level"],axis=1,inplace=True)
    
    return dataframe

def fill_ratio(dataframe,liste):
    boyut = len(liste)
    kalan_omur_degerleri = [(boyut - i - 1) / (boyut - 1) * 100 for i in range(boyut)]
    sayac = 0
    for index in liste:
        dataframe.at[index,"remaining_life"] = kalan_omur_degerleri[sayac]
        sayac += 1

def create_remaining_life(dataframe):
    dataframe["remaining_life"] = np.nan

    liste = list(dataframe[dataframe["Air_Leak_Failure"] == 1].index)

    for index in liste:
        dataframe.at[index,"remaining_life"] = 0 
    
    second_period = list(dataframe[(dataframe["timestamp"] >= '2020-04-18 23:59:01') & ((dataframe["timestamp"] < '2020-05-29 23:30:00'))].index)
    third_period = list(dataframe[(dataframe["timestamp"] >= '2020-05-30 06:00:01') & ((dataframe["timestamp"] < '2020-06-05 10:00:00'))].index)
    fourth_period = list(dataframe[(dataframe["timestamp"] >= '2020-06-07 14:30:01') & ((dataframe["timestamp"] < '2020-07-15 14:30:00'))].index)

    listeler = [second_period,third_period,fourth_period]

    for liste in listeler:
        fill_ratio(dataframe,liste)

    return dataframe

def create_oil_category(dataframe):
    bins = [20, 55, 70, 90]
    labels = ['Low', 'Medium', 'High']

    dataframe['Oil_temperature_category'] = pd.cut(dataframe['Oil_temperature'], bins=bins, labels=labels)

    return dataframe

def create_motor_category(dataframe):
    bins = [0,2,5,7.5,9.5]
    labels = ['turns_off', 'offloaded', 'under_load','working']

    dataframe['Motor_current_category'] = pd.cut(dataframe['Motor_current'], bins=bins, labels=labels)

    return dataframe

def create_new_variable(dataframe):
    dataframe["Oil_Res_Ratio"] = dataframe["Oil_temperature"] / dataframe["Reservoirs"]
    dataframe["H1_times_Res"] = dataframe["H1"] * dataframe["Reservoirs"]
    dataframe["Motor_times_Oil"] = dataframe["Motor_current"] * dataframe["Oil_temperature"] 

    return dataframe

def drop_timestamp(dataframe):
    dataframe.drop("timestamp",axis=1,inplace=True)

    return dataframe

def degisken_turlerini_ayır(dataframe,cat_th=10,car_th=20):
    
    kategorik_degiskenler = [col for col in dataframe.columns if dataframe[col].dtype == 'O']
    sayisal_degiskenler = [col for col in dataframe.columns if dataframe[col].dtype != 'O']
    
    kat_ama_car = [col for col in dataframe.columns if dataframe[col].dtype == 'O' and dataframe[col].nunique() > car_th]
    say_ama_cat = [col for col in dataframe.columns if dataframe[col].dtype != 'O' and dataframe[col].nunique() < cat_th]
    
    kategorik_degiskenler = kategorik_degiskenler + say_ama_cat
    
    kategorik_degiskenler = [col for col in kategorik_degiskenler if col not in kat_ama_car]
    
    sayisal_degiskenler = [col for col in sayisal_degiskenler if col not in say_ama_cat]
    
    return kategorik_degiskenler,sayisal_degiskenler,kat_ama_car

def scaler(dataframe):
    kategorik_degiskenler,sayisal_degiskenler,kat_ama_car = degisken_turlerini_ayır(dataframe)

    sayisal_degiskenler = [col for col in sayisal_degiskenler if col not in ["remaining_life","timestamp"]]

    ss = StandardScaler()
    dataframe[sayisal_degiskenler] = ss.fit_transform(dataframe[sayisal_degiskenler])

    dataframe = pd.get_dummies(data=dataframe,columns=kategorik_degiskenler,drop_first=True)

    return dataframe

def make_feature_engineering_rem(dataframe):
    set_options()
    dataframe = label_target(dataframe)
    dataframe = drop_useless(dataframe)
    dataframe = change_times_type(dataframe)
    dataframe = drop_high_korelation(dataframe)
    dataframe = create_remaining_life(dataframe)
    dataframe = create_oil_category(dataframe)
    dataframe = create_motor_category(dataframe)
    dataframe = create_new_variable(dataframe)
    dataframe = drop_timestamp(dataframe)
    dataframe = scaler(dataframe)

    return dataframe