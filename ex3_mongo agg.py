from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"

eventos = [
    {"tipo": "FAIL", "ip": "185.220.101.1"}, {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK", "ip": "192.168.1.10"}, {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "185.220.101.1"}, {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "45.33.32.156"}, {"tipo": "FAIL", "ip": "185.220.101.1"},
]


def main():
    client = MongoClient(MONGO_URI)
    db = client["cp1_seguranca"]
    col = db["eventos"]

    col.delete_many({})
    col.insert_many(eventos)

    pipeline = [
        {"$match": {"tipo": "FAIL"}},
        {"$group": {"_id": "$ip", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$limit": 3},
    ]

    print("Top 3 IPs com mais FAILs:")
    for doc in col.aggregate(pipeline):
        print(f"  {doc['_id']} -> {doc['total']}")

    client.close()


if __name__ == "__main__":
    main()