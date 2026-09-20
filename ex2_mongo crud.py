from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"

vulns = [
    {"cve_id": "CVE-2024-001", "tipo": "SQL Injection", "severidade": "Alta", "corrigida": False},
    {"cve_id": "CVE-2024-002", "tipo": "XSS", "severidade": "Media", "corrigida": True},
    {"cve_id": "CVE-2024-003", "tipo": "Path Traversal", "severidade": "Critica", "corrigida": False},
]


def main():
    client = MongoClient(MONGO_URI)
    db = client["cp1_seguranca"]
    col = db["vulnerabilidades"]

    col.delete_many({})

    # CREATE
    col.insert_many(vulns)

    print("Buscar severidade='Alta':")
    for doc in col.find({"severidade": "Alta"}):
        print(f"  {doc['cve_id']}: {doc['tipo']}")

    resultado = col.update_one({"cve_id": "CVE-2024-001"}, {"$set": {"corrigida": True}})
    print(f"\nupdate corrigida=True em 001 -> \"{resultado.modified_count} documento modificado\"")

    abertas = col.count_documents({"corrigida": False})
    print(f"count corrigida=False -> {abertas} (só a CVE-2024-003 restou aberta)")

    col.delete_one({"cve_id": "CVE-2024-002"})
    print("\nCVE-2024-002 removida.")

    client.close()


if __name__ == "__main__":
    main()