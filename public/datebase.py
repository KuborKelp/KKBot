import sqlite3
import os

PATH = "./database/"


def mergy_path_db(name: str, path=PATH):
    if not name.endswith(".db"):
        name += ".db"
    path_db = path + name
    return path_db


def initialize(name: str, path=PATH):
    """

    :param name: 数据库文件名 xxx.db
    :param path: 指定路径保存，默认路径:PATH = "./database/"
    :return: no return
    """
    path_db = mergy_path_db(name, path)
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path_db):
        with open(path_db, "w+"):
            pass


def create_table(name: str, table: list, path=PATH):
    """

    :param name: 数据库文件名 xxx.db
    :param path: 指定路径保存，默认路径:PATH = "./database/"
    :param table: 例:COINS(ID INT, COINS INT default 0)
    :return: no return
    """
    if table is None:
        table = []
    path_db = mergy_path_db(name, path)

    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    for t in table:
        cmd = "CREATE TABLE IF NOT EXISTS " + t
        cursor.execute(cmd)
        conn.commit()

    cursor.close()
    conn.close()


def select(name_db: str, table: str, key: dict, path=PATH):
    path_db = mergy_path_db(name_db, path)
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    cmd = f'SELECT * FROM {table}'

    if key:
        cmd += ' WHERE'
        count = 0
        for k in key.keys():
            if count > 0:
                cmd += ' AND'
            cmd += f' {k}={key[k]}'
            count = 1

    cursor.execute(cmd)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def insert(name_db: str, table: str, key: str, value: str, path=PATH):
    path_db = mergy_path_db(name_db, path)
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    cmd = f'INSERT INTO {table} {key} VALUES {value}'
    cursor.execute(cmd)
    conn.commit()

    cursor.close()
    conn.close()


def update(name_db: str, table: str, key: list, values: list, path=PATH):
    path_db = mergy_path_db(name_db, path)
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    cmd = f'UPDATE {table} SET {values[0]} = {values[1]} WHERE {key[0]}={key[1]}'
    cursor.execute(cmd)
    conn.commit()

    cursor.close()
    conn.close()


def delete(name_db: str, table: str, key: str, value: str, path=PATH):
    path_db = mergy_path_db(name_db, path)
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    cmd = f'DELETE FROM {table} WHERE {key}={value}'
    cursor.execute(cmd)
    conn.commit()

    cursor.close()
    conn.close()
