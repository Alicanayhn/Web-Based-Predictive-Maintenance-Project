from pymongo import MongoClient

def connect_remaining():
    client = MongoClient("localhost",27017)
    db = client["IletisimYazilim"]
    collection = db["MetroPT3"]

    return collection

def connect_class_rem():
    client = MongoClient("localhost",27017)
    db = client["IletisimYazilim"]
    collection = db["MetroPT3-class-rem"]

    return collection

def connect_kontrol():
    client = MongoClient("localhost",27017)
    db = client["IletisimYazilim"]
    collection = db["MetroKontrol"]

    return collection
 