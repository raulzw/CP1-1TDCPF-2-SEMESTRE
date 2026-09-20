# CP1 — Coding for Security (2º Semestre)

Soluções dos 10 exercícios do checkpoint. Cada exercício é um script
independente e roda separadamente.

## 1. Ambiente (Docker)

Suba o MySQL e o MongoDB localmente:

```bash
docker run -d --name mysql-cp1 -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=cp1_seguranca -p 3306:3306 mysql:8

docker run -d --name mongo-cp1 -p 27017:27017 mongo:7
```

Espere alguns segundos até o MySQL terminar de inicializar antes de rodar
os scripts (`docker logs -f mysql-cp1` até ver "ready for connections").

## 2. Dependências Python

```bash
pip install -r requirements.txt
```

## 3. Rodar cada exercício

```bash
python ex1_mysql.py            # CRUD SQL
python ex2_mongo_crud.py       # CRUD MongoDB
python ex3_mongo_agg.py        # Aggregation - Top IPs
python ex4_sql_injection.py    # Query insegura vs parametrizada
python ex5_transaction.py      # Transação com rollback
python ex6_mongo_index.py      # Índice e desempenho
python ex7_ml_classifier.py    # RandomForestClassifier
python ex8_anomaly.py          # IsolationForest
python ex9_metrics.py          # Métricas honestas
python ex10_pipeline.py        # Mini-pipeline SIEM completo
```
