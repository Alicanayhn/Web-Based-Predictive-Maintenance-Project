import datetime as dt
import pandas as pd

def no_filter_type(dataframe):
    BarM = len(dataframe[dataframe["Type"] == 'M'])
    BarL = len(dataframe[dataframe["Type"] == 'L'])
    BarH = len(dataframe[dataframe["Type"] == 'H'])

    values = [BarM,BarL,BarH]

    return values

def no_filter_air(dataframe):
    air_temp = dataframe["Air temperature [K]"].tolist()

    return air_temp

def no_filter_failure(dataframe):
    lenNo = len(dataframe[dataframe["Failure Type"] == "No Failure"])
    lenRandom = len(dataframe[dataframe["Failure Type"] == "Random Failures"])
    lenTool = len(dataframe[dataframe["Failure Type"] == "Tool Wear Failure"])
    lenOv = len(dataframe[dataframe["Failure Type"] == "Overstrain Failure"])
    lenHD = len(dataframe[dataframe["Failure Type"] == "Heat Dissipation Failure"])
    lenPow = len(dataframe[dataframe["Failure Type"] == "Power Failure"])

    values2 = [lenNo,lenRandom,lenTool,lenOv,lenHD,lenPow]

    return values2

def filter_type(start_date_type,end_date_type,dataframe):
    if (start_date_type != '2024-02-15' or end_date_type != '2024-02-15') and (start_date_type != None and end_date_type != None):
        dataframe_for_date = dataframe.copy()

        baslangic_tarihi = pd.to_datetime('2024-01-01 00:00:00')

        veri_sayisi = len(dataframe_for_date)

        tarihler = [baslangic_tarihi + dt.timedelta(minutes=15*i) for i in range(veri_sayisi)]

        dataframe_for_date["Date"] = tarihler
        
        dataframe_for_date = dataframe_for_date[(dataframe_for_date["Date"] < end_date_type) & (dataframe_for_date["Date"] > start_date_type)]

        BarM = len(dataframe_for_date[dataframe_for_date["Type"] == 'M'])
        BarL = len(dataframe_for_date[dataframe_for_date["Type"] == 'L'])
        BarH = len(dataframe_for_date[dataframe_for_date["Type"] == 'H'])

    else:
        BarM = len(dataframe[dataframe["Type"] == 'M'])
        BarL = len(dataframe[dataframe["Type"] == 'L'])
        BarH = len(dataframe[dataframe["Type"] == 'H'])
    
    values = [BarM,BarL,BarH]

    return values

def filter_fail(start_date_fail,end_date_fail,dataframe):
    if (start_date_fail != '2024-02-15' or end_date_fail != '2024-02-15') and (start_date_fail != None and end_date_fail != None):
        dataframe_for_fail = dataframe.copy()

        baslangic_tarihi = pd.to_datetime('2024-01-01 00:00:00')

        veri_sayisi = len(dataframe_for_fail)

        tarihler = [baslangic_tarihi + dt.timedelta(minutes=15*i) for i in range(veri_sayisi)]

        dataframe_for_fail["Date"] = tarihler
        
        dataframe_for_fail = dataframe_for_fail[(dataframe_for_fail["Date"] < end_date_fail) & (dataframe_for_fail["Date"] > start_date_fail)]

        lenNo = len(dataframe_for_fail[dataframe_for_fail["Failure Type"] == "No Failure"])
        lenRandom = len(dataframe_for_fail[dataframe_for_fail["Failure Type"] == "Random Failures"])
        lenTool = len(dataframe_for_fail[dataframe_for_fail["Failure Type"] == "Tool Wear Failure"])
        lenOv = len(dataframe_for_fail[dataframe_for_fail["Failure Type"] == "Overstrain Failure"])
        lenHD = len(dataframe_for_fail[dataframe_for_fail["Failure Type"] == "Heat Dissipation Failure"])
        lenPow = len(dataframe_for_fail[dataframe_for_fail["Failure Type"] == "Power Failure"])

    else:
        lenNo = len(dataframe[dataframe["Failure Type"] == "No Failure"])
        lenRandom = len(dataframe[dataframe["Failure Type"] == "Random Failures"])
        lenTool = len(dataframe[dataframe["Failure Type"] == "Tool Wear Failure"])
        lenOv = len(dataframe[dataframe["Failure Type"] == "Overstrain Failure"])
        lenHD = len(dataframe[dataframe["Failure Type"] == "Heat Dissipation Failure"])
        lenPow = len(dataframe[dataframe["Failure Type"] == "Power Failure"])

    values2 = [lenNo,lenRandom,lenTool,lenOv,lenHD,lenPow]

    return values2

def filter_air(start_date_air,end_date_air,dataframe):
    if (start_date_air != '2024-02-15' or end_date_air != '2024-02-15') and (start_date_air != None and end_date_air != None):
        dataframe_for_air = dataframe.copy()

        baslangic_tarihi = pd.to_datetime('2024-01-01 00:00:00')

        veri_sayisi = len(dataframe_for_air)

        tarihler = [baslangic_tarihi + dt.timedelta(minutes=15*i) for i in range(veri_sayisi)]

        dataframe_for_air["Date"] = tarihler
        
        dataframe_for_air = dataframe_for_air[(dataframe_for_air["Date"] < end_date_air) & (dataframe_for_air["Date"] > start_date_air)]

        air_temp = dataframe_for_air["Air temperature [K]"].tolist()

    else:

        air_temp = dataframe["Air temperature [K]"].tolist()

    return air_temp