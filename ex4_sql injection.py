import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "cp1_seguranca",
}

usuarios = [
    ("admin", "admin@x.com"),
    ("ana", "ana@x.com"),
    ("bruno", "bruno@x.com"),
]


def preparar_tabela(cursor, conn):
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    cursor.execute(
        """
        CREATE TABLE usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            email VARCHAR(100)
        )
        """
    )
    cursor.executemany("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", usuarios)
    conn.commit()


def busca_insegura(cursor, nome_digitado):
    query = f"SELECT * FROM usuarios WHERE nome = '{nome_digitado}'"
    cursor.execute(query)
    return cursor.fetchall()


def busca_segura(cursor, nome_digitado):
    query = "SELECT * FROM usuarios WHERE nome = %s"
    cursor.execute(query, (nome_digitado,))
    return cursor.fetchall()


def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    preparar_tabela(cursor, conn)

    entrada = "' OR '1'='1"

    resultado_inseguro = busca_insegura(cursor, entrada)
    print(f"[INSEGURO] entrada={entrada}  -> {len(resultado_inseguro)} usuários (VAZAMENTO)" )

    resultado_seguro = busca_segura(cursor, entrada)
    print(f"[SEGURO]   entrada={entrada}  -> {len(resultado_seguro)} usuários (defesa OK)")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()