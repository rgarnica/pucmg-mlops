# Criando a imagem do docker

```
docker build -t mlops-api .
```

# Executando a imagem

```
docker run --name="mlops-api" -p 5001:5001 mlops-api
```

# Fazendo uma requisição na API

```
curl -X POST -d sepal_length=4.9 -d sepal_width=3.0 -d petal_length=1.4 -d petal_width=0.2 http://localhost:5001/predict
```