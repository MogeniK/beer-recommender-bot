from tensorflow import keras

def load_model(model_path):
    return keras.models.load_model(model_path)

def predict_beer(model, features):
    prediction = model.predict([features])
    return prediction
    