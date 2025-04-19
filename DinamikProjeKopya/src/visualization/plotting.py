import pandas as pd
import datetime as dt
import numpy as np
import io
from matplotlib import pyplot as plt
import seaborn as sns
import base64

def plot_histplot(dataframe,col):
    img = io.BytesIO()
    plt.figure(figsize=(20,8))
    sns.histplot(data=dataframe,x=col,kde=True)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url

def plot_lineplot(dataframe,col):

    baslangic_tarihi = pd.to_datetime('2024-01-01 00:00:00')

    veri_sayisi = len(dataframe)

    tarihler = [baslangic_tarihi + dt.timedelta(minutes=15*i) for i in range(veri_sayisi)]

    dataframe["Date"] = tarihler

    img = io.BytesIO()
    plt.figure(figsize=(12,6))
    sns.lineplot(data=dataframe,x="Date",y=col)
    plt.title(f"Son Makinenin Processin sıcaklığı:{dataframe.iloc[-1][col]}")
    plt.ylabel("Işlem Sıcaklığı")
    plt.grid()
    plt.savefig(img,format="png")
    img.seek(0)

    dataframe.drop(["Date"],axis=1,inplace=True)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url
    
def pasta_grafiginin_ozellikleri(dataframe,target):
    sayilar = []
    degiskenler = list(dataframe[target].unique())

    for col in degiskenler:
        sayi = len(dataframe[dataframe[target] == col])
        sayilar.append(sayi)
    
    degiskenler = np.array(degiskenler)

    return degiskenler,sayilar

def plot_pie(dataframe,target = "Failure Type"):
    degiskenler,sayilar = pasta_grafiginin_ozellikleri(dataframe,target)

    img = io.BytesIO()
    plt.figure(figsize=(12,6))
    plt.pie(sayilar,labels=degiskenler,explode=[0.1, 0.6, 0.6, 0.6,0.6,0.6],autopct="%3.1f%%")
    # plt.legend()
    plt.title("Veri Setinin Hata Oranları")
    plt.savefig(img,format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

def plot_countplot(dataframe,col):
    img = io.BytesIO()
    plt.figure(figsize=(12,6))
    sns.countplot(data=dataframe,x=col,)
    plt.title("Makine Tür Dağılımı")
    plt.savefig(img,format="png")
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

def lineplot_for_targets(dataframe):
    baslangic_tarihi = pd.to_datetime('2024-01-01 00:00:00')

    veri_sayisi = len(dataframe)

    tarihler = [baslangic_tarihi + dt.timedelta(minutes=15*i) for i in range(veri_sayisi)]

    dataframe["Date"] = tarihler

    category_mapping = {category: idx for idx, category in enumerate(sorted(dataframe['Failure Type'].unique()))}
    dataframe['category_num'] = dataframe['Failure Type'].map(category_mapping)

    last_10 = dataframe.tail(10)

    img = io.BytesIO()

    plt.figure(figsize=(12, 6))
    plt.plot(last_10['Date'], last_10['category_num'], marker='o')

    plt.title('Son 10 Verinin Kategorik Değişimi')
    plt.xlabel('Tarih')
    plt.ylabel('Kategori')
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.yticks(ticks=list(category_mapping.values()), labels=list(category_mapping.keys()))

    plt.savefig(img,format="png")
    img.seek(0)

    dataframe.drop(["category_num","Date"],axis=1,inplace=True)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url
