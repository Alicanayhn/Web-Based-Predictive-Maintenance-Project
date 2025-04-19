import pandas as pd
import datetime as dt

def convert_to_dataframe(collection):
    data = list(collection.find())
    df = pd.DataFrame(data)

    return df

def take_copy(dataframe):
    dataframe_copy = dataframe.copy()

    return dataframe_copy

def take_last_data(dataframe):
    dataframe_copy = dataframe.copy()
    dataframe_copy.drop(columns=["Failure Type"],inplace=True)
    last_one = dataframe_copy.tail(1)

    return last_one

def change_last_datas_target(collection,dataframe,dataframe_copy,pred):
    last_ones_index = dataframe.index[-1]

    dataframe.at[last_ones_index,"Failure Type"] = str(pred[0])

    last_one_copy_index = dataframe_copy.index[-1]
    last_one_copy = dataframe_copy.iloc[last_one_copy_index]

    collection.update_one(
        {"_id":last_one_copy["_id"]},
        {"$set":{"Failure Type":dataframe.at[last_ones_index,"Failure Type"]}}
    )

def take_last_10_date(dataframe):
    dataframe_copy = dataframe.copy()

    baslangic_tarihi = pd.to_datetime('2024-01-01 00:00:00')

    veri_sayisi = len(dataframe)

    tarihler = [baslangic_tarihi + dt.timedelta(minutes=15*i) for i in range(veri_sayisi)]

    dataframe_copy["Date"] = tarihler

    last10 = dataframe_copy.tail(10)

    dates = last10["Date"].tolist()

    dates = [str(i) for i in dates]

    return dates

def take_last_10_ftype(dataframe):
    dataframe_copy = dataframe.copy()
    baslangic_tarihi = pd.to_datetime('2024-01-01 00:00:00')

    veri_sayisi = len(dataframe_copy)

    tarihler = [baslangic_tarihi + dt.timedelta(minutes=15*i) for i in range(veri_sayisi)]

    dataframe_copy["Date"] = tarihler

    category_mapping = {category: idx for idx, category in enumerate(sorted(dataframe_copy['Failure Type'].unique()))}
    dataframe_copy['category_num'] = dataframe_copy['Failure Type'].map(category_mapping)

    last_10 = dataframe_copy.tail(10)

    liste = last_10["category_num"].tolist()

    return liste

def take_last_data_rem(dataframe):
    dataframe_copy = dataframe.copy()
    dataframe_copy.drop(columns=["remaining_life"],inplace=True)
    last_one = dataframe_copy.tail(1)

    return last_one

def take_last_data_air(dataframe):
    dataframe_copy = dataframe.copy()
    dataframe_copy.drop(columns=["remaining_life"],inplace=True)
    last_one = dataframe_copy.tail(1)

    return last_one

def change_last_datas_target_air(collection,dataframe,dataframe_copy,pred):
    last_ones_index = dataframe.index[-1]

    dataframe.at[last_ones_index,"Air_Leak_Failure"] = str(pred[0])

    last_one_copy_index = dataframe_copy.index[-1]
    last_one_copy = dataframe_copy.iloc[last_one_copy_index]

    collection.update_one(
        {"_id":last_one_copy["_id"]},
        {"$set":{"Air_Leak_Failure":dataframe.at[last_ones_index,"Air_Leak_Failure"]}}
    )

def change_last_datas_target_rem(collection,dataframe,dataframe_copy,pred):
    last_ones_index = dataframe.index[-1]

    dataframe.at[last_ones_index,"remaining_life"] = int(pred[0])

    last_one_copy_index = dataframe_copy.index[-1]
    last_one_copy = dataframe_copy.iloc[last_one_copy_index]

    collection.update_one(
        {"_id":last_one_copy["_id"]},
        {"$set":{"remaining_life":dataframe.at[last_ones_index,"remaining_life"]}}
    )

def take_last_10air(dataframe):
    dataframe_copy = dataframe.copy()

    last_10 = dataframe_copy.tail(10)

    liste = last_10["class"].tolist()
    liste = [eleman + 1 for eleman in liste]

    return liste

def take_last_10rem(dataframe):
    dataframe_copy = dataframe.copy()

    last_10 = dataframe_copy.tail(10)

    liste = last_10["remaining_life"].tolist()
    
    return liste

def calculate_days(pred):
    day = pred * 41.4 / 100

    yuzdelik_fark = day - int(day)

    saat = yuzdelik_fark * 24

    return int(day),int(saat)

def take_last_torq(dataframe):
    dataframe_copy = dataframe.copy()
    dataframe_copy.drop(columns=["Torque [Nm]"],inplace=True)
    last_one = dataframe_copy.tail(1)

    return last_one

def take_torq_values(dataframe):
    torque_value = dataframe['Torque [Nm]'].tail(1).values[0]

    return torque_value

