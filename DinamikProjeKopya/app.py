from flask import Flask,render_template,request
from apscheduler.schedulers.background import BackgroundScheduler
import matplotlib
import random
import datetime as dt
from flask_caching import Cache

matplotlib.use("Agg")

from src.data.connection_bakim import baglan,connect_with_ipAdress,connect_with_usern_passw,connect_torq,connect_bakim_kontrol
from src.data.connection_remaining import connect_remaining,connect_class_rem,connect_kontrol
from src.models.load_model import model_loader,load_decisionTC,load_decisionTR,load_Knn
from src.models.train_model import train_again
from src.models.prediction_data import predict_data
from src.data.data_functions import *
from src.data.filter_data import *
from src.features.feature_engineering_failure import make_feature_engineering
from src.features.feature_engineering_remaining import make_feature_engineering_rem
from src.features.feature_engineering_air import make_feature_engineering_air
from src.features.feature_engineering_torque import make_feature_engineering_torque
from src.visualization.plotting import *
from src.visualization.theme import take_theme

# config = {
#     "DEBUG": True,          
#     "CACHE_TYPE": "SimpleCache",  
#     "CACHE_DEFAULT_TIMEOUT": 60  
# }

app = Flask(__name__)

# app.config.from_mapping(config)
# cache = Cache(app)

try:
    collection_bakim = baglan()
except ConnectionError as e:
    print(f"Bağlantı Kurulamadı : {e}")

try:
    collection_metro = connect_remaining()
except ConnectionError as e:
    print(f"Bağlantı Kurulamadi {e}")

try:
    collection_class = connect_class_rem()
except ConnectionError as e:
    print(f"Bağlantı Kurulamadı :{e}")

try:
    collection_kontrol = connect_kontrol()
except ConnectionError as e:
    print(f"Bağlantı Kurulamadı :{e}")

try:
    collection_torq = connect_torq()
except ConnectionError as e:
    print(f"Bağlantı Kurulamadi: {e}")

try:
    collection_bakim_kontrol = connect_bakim_kontrol()
except ConnectionError as e:
    print(f"Bağlantı Kurulamadi: {e}")

try:
    random_forest,sayac = model_loader()
except FileNotFoundError as e:
    print(f"File Bulunamadı :{e}")

try:
    DecisionTR = load_decisionTR()
except FileNotFoundError as e:
    print(f"File Bulunamadı :{e}")

try:
    DecisionTC = load_decisionTC()
except FileNotFoundError as e:
    print(f"File Bulunamadı :{e}") 

try:
    Knn = load_Knn()
except FileNotFoundError as e:
    print(f"File not found: {e}")

# @cache.cached(timeout=60,key_prefix='fetch_and_plot_data')
def fetch_and_plot_data(theme=None):
    global random_forest
    global sayac
    global DecisionTR
    global DecisionTC
    global Knn
    global collection_metro
    global collection_kontrol
    global collection_torq
    global collection_bakim_kontrol

    dataframe = convert_to_dataframe(collection_bakim)
    dataframe_torq = convert_to_dataframe(collection_bakim)
    dataframe_rem = convert_to_dataframe(collection_metro)
    dataframe_air = convert_to_dataframe(collection_metro)
    dataframe_class = convert_to_dataframe(collection_class)
    last10_air = take_last_10air(dataframe_class)
    last10_rem = take_last_10rem(dataframe_class)
    
    air_temp = no_filter_air(dataframe)

    values = no_filter_type(dataframe)

    values2 = no_filter_failure(dataframe)

    firstColor,secondColor,thirdColor = take_theme(theme)

    dataframe_copy = take_copy(dataframe)

    torque_value = take_torq_values(dataframe_torq)

    dataframe = make_feature_engineering(dataframe)
    dataframe_rem = make_feature_engineering_rem(dataframe_rem)
    dataframe_air = make_feature_engineering_air(dataframe_air)
    dataframe_torq = make_feature_engineering_torque(dataframe_torq)

    random_forest = train_again(random_forest,dataframe,sayac)

    last_data = take_last_data(dataframe)
    last_data_rem = take_last_data_rem(dataframe_rem)
    last_data_air = take_last_data_air(dataframe_air)
    last_torq =  take_last_torq(dataframe_torq)

    pred_torq = predict_data(Knn,last_torq)

    pred_air = predict_data(DecisionTC,last_data_air)

    pred_rem = predict_data(DecisionTR,last_data_rem)

    rounded_value = round(float(pred_rem[0]), 1)

    day,saat = calculate_days(rounded_value)

    class_rem_dict = {"class" : int(pred_air[0]) , "remaining_life" : rounded_value}
    torq_dict = {"Expecting Torque": round(float(pred_torq[0]),1),"Current Torque" : torque_value}

    last_data_mongo = collection_metro.find_one(sort=[('_id', -1)])
    last_data_kontrol = collection_kontrol.find_one(sort=[('_id', -1)])


    if last_data_mongo['_id'] != last_data_kontrol['_id']:
         collection_class.insert_one(class_rem_dict)
         collection_kontrol.insert_one(last_data_mongo)

    last_data_bakim =  collection_bakim.find_one(sort=[('_id',-1)])
    last_data_bakim_kontrol =  collection_bakim_kontrol.find_one(sort=[('_id',-1)])

    if last_data_bakim['_id'] != last_data_bakim_kontrol['_id']:
        collection_torq.insert_one(torq_dict)
        collection_bakim_kontrol.insert_one(last_data_bakim)

    pred = predict_data(random_forest,last_data)

    change_last_datas_target(collection_bakim,dataframe,dataframe_copy,pred)


    failure_type = take_last_10_ftype(dataframe)

    dates = take_last_10_date(dataframe)

    with app.app_context():
        return render_template('plot.html',values = values,values2 = values2,dates=dates,failure_type=failure_type,
                               firstColor = firstColor,secondColor=secondColor,thirdColor=thirdColor,last10_air=last10_air,
                               last10_rem=last10_rem,day=day,saat=saat,rounded_value=rounded_value,
                               pred_torq = round(float(pred_torq[0]),1),torque_value=torque_value,air_temp=air_temp)
    
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_and_plot_data, trigger="interval", seconds=59)
scheduler.start()

@app.route('/')
def home():

    return render_template("index.html")

# Tarih ile filtrelenmis grafikleri görselleştiren kisim
def filter_date(theme = 'blue',start_date_type=None,end_date_type=None,start_date_fail=None,end_date_fail=None,start_date_air=None,end_date_air=None):

    global random_forest
    global sayac
    global DecisionTR
    global DecisionTC
    global Knn
    global collection_metro
    global collection_kontrol
    global collection_torq
    global collection_bakim_kontrol
    
    dataframe = convert_to_dataframe(collection_bakim)
    dataframe_torq = convert_to_dataframe(collection_bakim)
    dataframe_rem = convert_to_dataframe(collection_metro)
    dataframe_air = convert_to_dataframe(collection_metro)
    dataframe_class = convert_to_dataframe(collection_class)

    values = filter_type(start_date_type,end_date_type,dataframe)

    values2 = filter_fail(start_date_fail,end_date_fail,dataframe)

    last10_air = take_last_10air(dataframe_class)
    last10_rem = take_last_10rem(dataframe_class)

    air_temp = filter_air(start_date_air,end_date_air,dataframe)

    firstColor,secondColor,thirdColor = take_theme(theme)

    dataframe_copy = take_copy(dataframe)
    torque_value = dataframe_torq['Torque [Nm]'].tail(1).values[0]

    dataframe = make_feature_engineering(dataframe)
    dataframe_rem = make_feature_engineering_rem(dataframe_rem)
    dataframe_air = make_feature_engineering_air(dataframe_air)
    dataframe_torq = make_feature_engineering_torque(dataframe_torq)

    random_forest = train_again(random_forest,dataframe,sayac)

    last_data = take_last_data(dataframe)
    last_data_rem = take_last_data_rem(dataframe_rem)
    last_data_air = take_last_data_air(dataframe_air)
    last_torq =  take_last_torq(dataframe_torq)

    pred_torq = predict_data(Knn,last_torq)

    pred_air = predict_data(DecisionTC,last_data_air)

    pred_rem = predict_data(DecisionTR,last_data_rem)

    rounded_value = round(float(pred_rem[0]), 1)

    day,saat = calculate_days(rounded_value)

    class_rem_dict = {"class" : int(pred_air[0]) , "remaining_life" : rounded_value}
    torq_dict = {"Expecting Torque": round(float(pred_torq[0]),1),"Current Torque" : torque_value}

    last_data_mongo = collection_metro.find_one(sort=[('_id', -1)])
    last_data_kontrol = collection_kontrol.find_one(sort=[('_id', -1)])


    if last_data_mongo['_id'] != last_data_kontrol['_id']:
         collection_class.insert_one(class_rem_dict)
         collection_kontrol.insert_one(last_data_mongo)

    last_data_bakim =  collection_bakim.find_one(sort=[('_id',-1)])
    last_data_bakim_kontrol =  collection_bakim_kontrol.find_one(sort=[('_id',-1)])

    if last_data_bakim['_id'] != last_data_bakim_kontrol['_id']:
        collection_torq.insert_one(torq_dict)
        collection_bakim_kontrol.insert_one(last_data_bakim)

    pred = predict_data(random_forest,last_data)

    change_last_datas_target(collection_bakim,dataframe,dataframe_copy,pred)


    failure_type = take_last_10_ftype(dataframe)

    dates = take_last_10_date(dataframe)


    return render_template('plot.html',values = values,values2 = values2,dates=dates,failure_type=failure_type,
                               firstColor = firstColor,secondColor=secondColor,thirdColor=thirdColor,last10_air=last10_air,
                               last10_rem=last10_rem,day=day,saat=saat,rounded_value=rounded_value,
                               pred_torq = round(float(pred_torq[0]),1),torque_value=torque_value,air_temp=air_temp)

@app.route('/plot',methods = ["POST"])
def plot():
    theme = request.form.get('theme')
    return fetch_and_plot_data(theme) 

@app.route('/get-data',methods = ['POST'])
def get_data(theme = 'blue'):
    start_date_type = request.form.get('date-start-type')
    end_date_type = request.form.get('date-end-type')

    start_date_fail = request.form.get('date-start-failure')
    end_date_fail = request.form.get('date-end-failure')

    start_date_air = request.form.get('date-start-air')
    end_date_air = request.form.get('date-end-air')

    return filter_date(theme,start_date_type,end_date_type,start_date_fail,end_date_fail,start_date_air,end_date_air)

if __name__ == '__main__':
    app.run(debug=True)