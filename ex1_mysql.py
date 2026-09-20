
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "cp1_seguranca",
}

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS ativos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ip VARCHAR(45) NOT NULL UNIQUE,
    tipo VARCHAR(50) NOT NULL,
    criticidade ENUM('baixa', 'media', 'alta') NOT NULL,
    status VARCHAR(20) NOT NULL
);
"""

ativos_iniciais = [
    ("SRV-WEB01", "192.168.1.10", "servidor", "alta", "ativo"),
    ("PC-RH03", "192.168.1.45", "estacao", "baixa", "ativo"),
    ("SW-CORE01", "192.168.1.1", "switch", "media", "inativo"),
]


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def criar_tabela(cursor):
    cursor.execute(CREATE_TABLE_SQL)


def inserir_ativos(conn, cursor, ativos):
    sql = "INSERT INTO ativos (nome, ip, tipo, criticidade, status) VALUES (%s, %s, %s, %s, %s)"
    for ativo in ativos:
        try:
            cursor.execute(sql, ativo)
            conn.commit()
        except Error as e:
            conn.rollback()
            print(f"  [ERRO] Não inseriu {ativo[0]} ({ativo[1]}): {e}")


def listar_por_tipo(cursor, tipo):
    cursor.execute("SELECT nome, ip, criticidade, status FROM ativos WHERE tipo = %s", (tipo,))
    return cursor.fetchall()


def atualizar_status(conn, cursor, nome, novo_status):
    cursor.execute("UPDATE ativos SET status = %s WHERE nome = %s", (novo_status, nome))
    conn.commit()
    return cursor.rowcount


def remover_ativo(conn, cursor, nome):
    cursor.execute("DELETE FROM ativos WHERE nome = %s", (nome,))
    conn.commit()
    return cursor.rowcount


def main():
    conn = get_connection()
    cursor = conn.cursor()

    print("Criando tabela...")
    criar_tabela(cursor)

    print("Inserindo dados iniciais...")
    inserir_ativos(conn, cursor, ativos_iniciais)

    print("\nListar tipo='servidor':")
    for row in listar_por_tipo(cursor, "servidor"):
        print(" ", " | ".join(str(c) for c in row))

    print("\nAtualizando status de SW-CORE01 para 'ativo'...")
    linhas = atualizar_status(conn, cursor, "SW-CORE01", "ativo")
    print(f"  {linhas} registro(s) atualizado(s)")

    print("\nTentando inserir IP duplicado (192.168.1.10)...")
    inserir_ativos(conn, cursor, [("SRV-WEB02", "192.168.1.10", "servidor", "alta", "ativo")])

    print("\nRemovendo PC-RH03...")
    linhas = remover_ativo(conn, cursor, "PC-RH03")
    print(f"  {linhas} registro(s) removido(s)")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()