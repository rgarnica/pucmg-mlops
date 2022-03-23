from flask import Flask, request
import joblib
import sys

app = Flask(__name__)

MODEL_LABELS = ['setosa', 'versicolor', 'virginica']


@app.route("/predict",methods=['POST'])
def hello_world():

    sepal_length = request.args.get('sepal_length', default=5.8, type=float)
    sepal_width = request.args.get('sepal_width', default=3.0, type=float)
    petal_length = request.args.get('petal_length', default=3.9, type=float)
    petal_width = request.args.get('petal_width', default=1.2, type=float)

    model = joblib.load('model.pkl')
    features = [[sepal_length, sepal_width, petal_length, petal_width]]

    label_index = model.predict(features)
    label = MODEL_LABELS[label_index[0]]

    return label

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)