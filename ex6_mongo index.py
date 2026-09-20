import random
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"

IPS_POOL = [
    "185.220.101.1", "91.240.118.172", "45.33.32.156",
    "192.168.1.10", "10.0.0.5", "200.150.30.4",
]


def gerar_eventos(qtd=1000, ip_alvo="185.220.101.1", qtd_alvo=250):
    eventos = []
    # garante exatamente qtd_alvo eventos do IP alvo
    for _ in range(qtd_alvo):
        eventos.append({"ip": ip_alvo, "tipo": random.choice(["FAIL", "OK"])})
    outros_ips = [ip for ip in IPS_POOL if ip != ip_alvo]
    for _ in range(qtd - qtd_alvo):
        eventos.append({"ip": random.choice(outros_ips), "tipo": random.choice(["FAIL", "OK"])})
    random.shuffle(eventos)
    return eventos


def main():
    client = MongoClient(MONGO_URI)
    db = client["cp1_seguranca"]
    col = db["eventos_perf"]

    col.delete_many({})
    eventos = gerar_eventos()
    col.insert_many(eventos)
    print(f"{len(eventos)} eventos inseridos.")

    col.create_index("ip")
    print("Índice criado em 'ip'.")

    ip_alvo = "185.220.101.1"
    total = col.count_documents({"ip": ip_alvo})
    print(f"Eventos do IP {ip_alvo}: {total}")

    client.close()


if __name__ == "__main__":
    main()