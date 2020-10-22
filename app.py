import json
import pandas as pd
import numpy as np
import tensorflow
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)

# Available routes
@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")

# @app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about.html")

# @app.route("/model")
# @app.route("/our-model")
@app.route("/our-model.html")
def model():
    return render_template("our-model.html")

@app.route("/model/<zipInput>/<employmentInput>/<amountInput>")
def election_predict(zipInput, employmentInput, amountInput):

    # print(amountInput)

    #Load model. 
    model = load_model("election_model.h5")

    #Dictionary to store the inputs. 
    input_dict = {"Zip": zipInput, "Occupation":  employmentInput, "Amount": amountInput}
    # print(input_dict)

    #Since we will only pass 1 prediction at a time, index = [0] (only 1 row)
    input_df = pd.DataFrame(data = input_dict, index = [0])

    #Empty df to create the encoded values. -----------
    encoded_df = pd.DataFrame()

    for column in input_df[["Zip","Occupation","Amount"]]:
        
        #Creates the encoder object.
        encoder = LabelEncoder()
        #Imports the encoded attributes from our original model.
        encoder.classes_ = np.load(f'model_encoders/encoder{column}.npy', allow_pickle=True)
        print(encoder.classes_)
        #Creates a colmn with the encoded values.
        encoded_df[column] = encoder.transform(input_df[column])

    #Scaler improrts the scaler parameters from our original model.
    X_scaler_USER = MinMaxScaler().fit(pd.read_pickle('https://election-data-2020-red-raiders.s3.us-east-2.amazonaws.com/X_scaler.pkl'))
    #Scales the user input parameters.
    X_USER_scaled = X_scaler_USER.transform(encoded_df)
   
    #model prediction.
    encoded_predictions = model.predict_classes(X_USER_scaled)

    #original encoder of campaign.
    encoder_campaign = LabelEncoder()
    encoder_campaign.classes_ = np.load(f'model_encoders/encoderCampaign.npy', allow_pickle=True)
    # print(encoder_campaign.classes_)

    #Decodes the prediction labels.
    prediction_labels = encoder_campaign.inverse_transform(encoded_predictions)

    #Inserts prediction labels into dictionary in preparation for jsonification
    prediction_labels_dict = [{"Campaign": str(prediction_labels[0])}]
    
    # Test dictionary
    # prediction_labels = [{"Campaign": "Democrat"}]

    #Returns the prediction.
    return jsonify(prediction_labels_dict)



if __name__ == "__main__":
    app.run(debug=False)