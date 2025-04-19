from pymongo.mongo_client import MongoClient

def baglan():
    client = MongoClient("localhost",27017)
    db = client["IletisimYazilim"]
    collection = db["Bakim"]

    return collection

def connect_with_usern_passw():
    username = "alican"
    password = "123456"
    host = "localhost"
    port = 27017
    database = "IletisimYazilim"

    uri = f"mongodb://{username}:{password}@{host}:{port}/{database}"
    client = MongoClient(uri)

    db = client[database]

    collection = db["Bakim"]

    return collection

def connect_with_ipAdress():
    client = MongoClient("mongodb://192.168.0.115:27017")
    db = client["IletisimYazilim"]
    collection = db["Bakim"]

    return collection

def connect_torq():
    client = MongoClient("localhost",27017)
    db = client["IletisimYazilim"]
    collection = db["BakimTorque"]

    return collection

def connect_bakim_kontrol():
    client = MongoClient("localhost",27017)
    db = client["IletisimYazilim"]
    collection = db["BakimKontrol"]

    return collection