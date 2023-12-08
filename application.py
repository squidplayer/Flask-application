from flask import Flask, jsonify , render_template, request
from flask_cors import CORS,cross_origin
import pandas as pd
import numpy as np;
import pickle

# For reading the data
car = pd.read_csv('aniket_car_data.csv')

regression_model = pickle.load(open('AniketLinearRegressionModel.pkl', 'rb'))



app = Flask(__name__)

@app.route('/', methods=['GET','POST'])

def index():
    brands = sorted(car['Brand'].unique())
    model = sorted(car['Model'].unique())
    location = sorted(car['Location'].unique(), reverse=True)
    Year = sorted(car['Year'].unique())
    fuel_type = car['Fuel_Type'].unique()
    tranmission = car['Transmission'].unique()
    Owner_type = car['Owner_Type'].unique()

    return render_template('index.html', brands= brands, Year=Year, car_models= model, location= location,  fuel_type= fuel_type,tranmission= tranmission,Owner_type= Owner_type)



@app.route('/predict', methods= ['POST'])
@cross_origin()

def predict():
    brand = request.form.get('brand')
    model = request.form.get('model')
    location = request.form.get('location')
    year = int(request.form.get('year'))
    kilometers = np.log(int(request.form.get('kilometer')))
    fuel = int(request.form.get('fuel'))
    transmission = int(request.form.get('transmission'))
    owner_type = int(request.form.get('owner'))
    mileage = request.form.get('mileage')
    engine = request.form.get('engine')
    power = request.form.get('power')

    print(brand, model, location, year, kilometers, fuel, transmission, owner_type, mileage, engine, power)


    

    new_data = pd.DataFrame(columns=['Brand', 'Model', 'Location', 'Year', 'Kilometers_Driven', 'Fuel_Type', 'Transmission', 'Owner_Type', 'Mileage', 'Engine', 'Power'],
                        data=[[brand, model, location, year, kilometers, fuel, transmission, owner_type, mileage, engine, power]])
    

    prediction = regression_model.predict(new_data)

    print(prediction)
    print(type(prediction))

    return jsonify({"Price in Lakhs": prediction.tolist()})
    


if __name__ == "__main__":
    app.run(debug=True  )



