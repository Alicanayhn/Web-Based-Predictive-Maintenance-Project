import joblib

def len_control(dataframe,sayac):
    if len(dataframe) == (sayac + 1) * 10000:
        return True
    else:
        return False
    
def train_again(model,dataframe,sayac):
    if len_control(dataframe,sayac):
       dataframe_copy = dataframe

       X = dataframe_copy.drop(["Failure Type"],axis = 1)
       y = dataframe_copy["Failure Type"]

       model = model.fit(X,y)

       joblib.dump(model,f"C:\\Users\\Ali Can\\Desktop\\Proje\\DinamikProje\\models\\RandomForestModel_{sayac + 1}.joblib")

       return model
    
    else:
        
        return model