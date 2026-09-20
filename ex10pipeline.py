import re
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier

MONGO_URI = "mongodb://localhost:27017"
LOG_PATH = "auth.log"

LINE_RE = re.compile(
    r"^(?P<timestamp>\S+ \S+) (?P<tipo>\w+) usuario=(?P<usuario>\S+) ip=(?P<ip>\S+)$"
)


def parse_log(path):
    documentos = []
    with open(path, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            m = LINE_RE.match(linha)
            if not m:
                continue
            documentos.append(m.groupdict())
    return documentos


def main():
    documentos = parse_log(LOG_PATH)

    client = MongoClient(MONGO_URI)
    db = client["cp1_seguranca"]
    col = db["auth_events"]
    col.delete_many({})
    if documentos:
        col.insert_many(documentos)
    print(f"Eventos inseridos no MongoDB: {len(documentos)}")

    pipeline = [
        {"$match": {"tipo": "FAIL"}},
        {"$group": {"_id": "$ip", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
    ]
    contagem_por_ip = list(col.aggregate(pipeline))

    X = [[doc["total"]] for doc in contagem_por_ip]
    y = [1 if doc["total"] >= 5 else 0 for doc in contagem_por_ip]

    print("Dataset de treino:", X, "rótulos", y)
    for doc in contagem_por_ip:
        suspeito = 1 if doc["total"] >= 5 else 0
        print(f"  {doc['_id']} -> {doc['total']} FAILs (suspeito={suspeito})")

    clf = RandomForestClassifier(random_state=42)
    clf.fit(X, y)

    pred = clf.predict([[8]])[0]
    rotulo = "Suspeito (1)" if pred == 1 else "Normal (0)"
    print(f"\nPrevisão para IP com 8 falhas -> {rotulo}")

    client.close()


if __name__ == "__main__":
    main()