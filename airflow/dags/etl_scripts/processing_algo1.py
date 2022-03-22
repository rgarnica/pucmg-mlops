import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn

import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputPath", help="arquivo input clean Iris", type=str)
args = parser.parse_args()

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_squared_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

warnings.filterwarnings("ignore")
np.random.seed(40)

try:
    data = pd.read_csv(args.inputPath, sep=",")
except Exception as e:
    logger.exception("erro abrindo csv: %s", e)

train, test = train_test_split(data)
train_x = train.drop(["classEncoder"], axis=1)
test_x = test.drop(["classEncoder"], axis=1)
train_y = train[["classEncoder"]]
test_y = test[["classEncoder"]]

try:
    idExperiment = mlflow.create_experiment('Iris1')
except:
    idExperiment = mlflow.get_experiment_by_name('Iris1').experiment_id

alpha = 0.5
l1_ratio = 0.5
with mlflow.start_run(experiment_id=idExperiment):
    mlflow.log_param("alpha", alpha)
    mlflow.log_param("l1_ratio", l1_ratio)

    regressor = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
    regressor.fit(train_x, train_y)

    predicted_qualities = regressor.predict(test_x)

    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)

    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
    if tracking_url_type_store != "file":
        mlflow.sklearn.log_model(regressor, "model", registered_model_name="IrisModel")
    else:
        mlflow.sklearn.log_model(regressor, "model")








