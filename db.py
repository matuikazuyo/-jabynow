import MySQLdb
import hashlib
import random as rd
import string

def insert(id,pw,mail,name,department,jyousi_id,jyousi_name,yakusyoku):
    salt = create_salt()
    b_pw = bytes(pw, "utf-8")
    b_salt = bytes(salt, "utf-8")

    hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 2560).hex()

    conn = get_connection()
    cur = conn.cursor()

    insert_sql = "INSERT INTO syain VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    try:
        cur.execute(insert_sql, (id,hashed_pw,mail,name,department,jyousi_id,jyousi_name,yakusyoku,salt))
    except Exception as e:
        print("SQL実行に失敗：" , e)
    
    cur.close()
    conn.commit()
    conn.close()

def create_salt():
    SALT_LEN = 20
    CHARACTER = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    salt = "".join(rd.choices(CHARACTER, k=SALT_LEN))
    return salt


def get_connection():
    return MySQLdb.connect(user='root',passwd='gogototaiga1',host='localhost',db='ringisyosystem',charset="utf8")

def login(id,pw):
    salt = search_salt(id)

    if salt == None:
        return None 

    # PWハッシュ
    b_pw = bytes(pw, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 2560).hex()

    result = search_account(id, hashed_pw)

    return result

def search_salt(id):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT salt FROM kanrisya WHERE id = %s"

    try:
        cur.execute(sql, (id,))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return result[0]

    return None

def search_account(id,pw):
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT pw id FROM kanrisya WHERE id = %s "
    try:
        cur.execute(sql, (id,))
    except Exception as e:
        print("SQL実行に失敗：" , e)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

# def yakusyoku(id):
#     conn = get_connection()
#     cur = conn.cursor()
#     sql = "SELECT yakusyoku FROM syain WHERE id = %s"
#     try:
#         cur.execute(sql, (id,))
#     except Exception as e:
#         print("SQL実行に失敗：" , e)
#     result = cur.fetchone()
#     cur.close()
#     conn.close()
#     return yakusyoku
