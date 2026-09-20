"""
Exercício 5 — Transação com rollback (MySQL)
"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "cp1_seguranca",
}

contas_iniciais = [(1, "Alice", 1000), (2, "Bob", 500)]


def preparar_tabela(cursor, conn):
    cursor.execute("DROP TABLE IF EXISTS contas")
    cursor.execute(
        """
        CREATE TABLE contas (
            id INT PRIMARY KEY,
            titular VARCHAR(100),
            saldo INT
        )
        """
    )
    cursor.executemany("INSERT INTO contas (id, titular, saldo) VALUES (%s, %s, %s)", contas_iniciais)
    conn.commit()


def get_saldo(cursor, conta_id):
    cursor.execute("SELECT saldo FROM contas WHERE id = %s", (conta_id,))
    row = cursor.fetchone()
    return row[0] if row else None


def transferir(conn, cursor, origem_id, destino_id, valor):
    try:
        # debita da origem
        cursor.execute("UPDATE contas SET saldo = saldo - %s WHERE id = %s", (valor, origem_id))

        # verifica se a conta destino existe antes de creditar
        cursor.execute("SELECT id FROM contas WHERE id = %s", (destino_id,))
        if cursor.fetchone() is None:
            raise ValueError(f"conta destino {destino_id} inexistente")

        # credita no destino
        cursor.execute("UPDATE contas SET saldo = saldo + %s WHERE id = %s", (valor, destino_id))

        conn.commit()
        return True, None
    except (Error, ValueError) as e:
        conn.rollback()
        return False, str(e)


def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    conn.autocommit = False
    cursor = conn.cursor()

    preparar_tabela(cursor, conn)

    ok, erro = transferir(conn, cursor, 1, 2, 200)
    alice = get_saldo(cursor, 1)
    bob = get_saldo(cursor, 2)
    print(f"Transferência 1 {'OK' if ok else 'FALHOU'}. Alice={alice}, Bob={bob}")

    ok, erro = transferir(conn, cursor, 1, 99, 100)
    alice = get_saldo(cursor, 1)
    status = "OK" if ok else f"FALHOU ({erro}). Rollback."
    print(f"Transferência 2 {status} Alice={alice}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()