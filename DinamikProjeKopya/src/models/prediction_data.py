def predict_data(model,last_data):
    pred = model.predict(last_data.values.reshape(1,-1))

    return pred