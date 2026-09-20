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
python ex1_mysql_crud.py       # CRUD SQL
python ex2_mongo_crud.py       # CRUD MongoDB
python ex3_mongo_agg.py        # Aggregation - Top IPs
python ex4_sql_injection.py    # Query insegura vs parametrizada
python ex5_transaction.py      # Transação com rollback
python ex6_mongo_index.py      # Índice e desempenho
python ex7_ml_classifier.py    # RandomForestClassifier
python ex8_anomaly_detection.py # IsolationForest
python ex9_metrics.py          # Métricas honestas
python ex10_pipeline.py        # Mini-pipeline SIEM completo
```

## Notas

- **Exercício 4**: é um exercício puramente defensivo/didático
  (comparar concatenação insegura vs. query parametrizada). Rode só
  no banco local do laboratório.
- **Exercício 10**: usa `auth.log`, incluído nesta pasta com o mesmo
  formato e as mesmas contagens do enunciado (10 FAILs de
  185.220.101.1, 5 de 91.240.118.172, 3 de 45.33.32.156). Se você já
  tem o `auth.log` da GS do 1º semestre, é só substituir o arquivo —
  o parser (`LINE_RE`) espera o formato:
  `TIMESTAMP TIPO usuario=NOME ip=IP`.
- Os scripts 7, 8 e 9 não dependem de banco de dados — rodam direto.
- `random_state=42` é usado em todos os pontos de aleatoriedade
  (split de treino/teste, modelos) para reprodutibilidade, como pedido
  nos critérios de correção.
