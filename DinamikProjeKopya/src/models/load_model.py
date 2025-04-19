import os
import joblib

def find_sayac():

    folder_path = "C:\\Users\\Ali Can\\Desktop\\ProjeDeneme\\DinamikProjeKopya\\models"
    
    file_names = os.listdir(folder_path)

    for file_name in file_names:
        aranan_file = file_name

    start = aranan_file.index('_') + 1
    end = aranan_file.index('.', start)
    sayac= int(aranan_file[start:end])
    
    return folder_path,sayac

def model_loader():
    folder_path,sayac = find_sayac()

    model = joblib.load(f"{folder_path}\\RandomForestModel_{sayac}.joblib")

    return model,sayac

def load_decisionTR():
    folder_path = "C:\\Users\\Ali Can\\Desktop\\ProjeDeneme\\DinamikProjeKopya\\models"

    model = joblib.load(f"{folder_path}\\DecisionTR.joblib")
    
    return model

def load_decisionTC():
    folder_path = "C:\\Users\\Ali Can\\Desktop\\ProjeDeneme\\DinamikProjeKopya\\models"

    model = joblib.load(f"{folder_path}\\DecisionTC.joblib")
    
    return model

def load_Knn():
    folder_path = "C:\\Users\\Ali Can\\Desktop\\ProjeDeneme\\DinamikProjeKopya\\models"

    model = joblib.load(f"{folder_path}\\Knn.joblib")
    
    return model
