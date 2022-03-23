from flask import Flask, request, jsonify
import joblib
import sys

app = Flask(__name__)

MODEL_LABELS = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']

@app.route("/predict",methods=['POST'])
def predict():

    sepal_length = request.form.get('sepal_length', default=None, type=float)
    sepal_width = request.form.get('sepal_width', default=None, type=float)
    petal_length = request.form.get('petal_length', default=None, type=float)
    petal_width = request.form.get('petal_width', default=None, type=float)

    if (sepal_length is None or sepal_width is None or petal_length is None or petal_width is None):
        response = jsonify(status='error', message='Os parametros sepal_length, sepal_width, petal_length, petal_width sao obrigatorios e precisam ser numericos.')
        response.status_code = 400
        return response

    model = joblib.load('model.pkl')
    features = [[sepal_length, sepal_width, petal_length, petal_width]]

    try:
        label_index = model.predict(features)
    except Exception as err:
        response = jsonify(status='error', message='Falha na previsao do modelo. Erro: {}'.format(err))
        response.status_code = 400
        return response

    label = MODEL_LABELS[label_index[0]]
    return jsonify(status='complete', label=label)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)