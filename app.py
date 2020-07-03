  
from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from datetime import date

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])

        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif (Fuel_Type_Petrol == 'Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        elif (Fuel_Type_Petrol == 'CNG'):
        	Fuel_Type_Petrol = 0
        	Fuel_Type_Diesel = 0

        Year=int(date.today().year) - Year

        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        elif (Seller_Type_Individual == 'Dealer'):
            Seller_Type_Individual=0

        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        elif (Transmission_Mannual == 'Automatic'):
            Transmission_Mannual=0
        try:
            if Present_Price < 1.5:
                raise Exception
            prediction=model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
            output=round(prediction[0],2)
        except:
        	output = -1
        if output<0:
            return render_template('result.html', output = output)
        else:
            return render_template('result.html', output = output)

    else:
        return render_template('result.html')

if __name__=="__main__":
    app.run(debug=True)
