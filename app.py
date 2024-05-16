from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np

app = Flask(__name__,template_folder='templates')

model = pickle.load(open('models/LogR_model.pkl','rb'))

@app.route('/')
def home():
    return render_template('Diabetes_Prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    glucose = request.form['Glucose']
    bp = request.form['BP']
    insulin = request.form['insulin']
    bmi = request.form['bmi']
    age = request.form['age']



    int_features = []
    for value in request.form.values():
        try:
            int_value = int(value)
            int_features.append(int_value)
        except ValueError:
            pass

    if not int_features:
        return render_template('Diabetes_Prediction.html', pred="Please provide valid input data.")

    print(int_features)
    input_data = np.array(int_features).reshape(1, -1)


    prediction = model.predict(input_data)


    if prediction == 1:
        result = "You are Diabetic"
    else:
        result = "You are Non-Diabetic"

    return render_template('Diabetes_Prediction.html', pred=result,glucose=glucose, bp=bp, insulin=insulin, bmi=bmi, age=age)

if __name__ == '__main__':
    app.run(debug=True)