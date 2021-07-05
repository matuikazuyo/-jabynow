import MySQLdb
import hashlib
import random as rd
import string

def insert(mail,pw,name,bir,depa,tclass):
    salt = create_salt()
    b_pw = bytes(pw, "utf-8")
    b_salt = bytes(salt, "utf-8")

    hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 2560).hex()

    conn = get_connection()
    cur = conn.cursor()

    insert_sql = "INSERT INTO account2 VALUES(%s,%s,%s,%s,%s,%s,%s)"

    try:
        cur.execute(insert_sql, (mail,hashed_pw,name,bir,depa,tclass,salt))
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
    return MySQLdb.connect(user='root',passwd='gogototaiga1',host='localhost',db='gakusyuukanri',charset="utf8")

def login(id,pw):
    salt = search_salt(pw)

    if salt == None:
        return None 

    # PWハッシュ
    b_pw = bytes(pw, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 2560).hex()

    result = search_account(id, hashed_pw)

    return result

def search_salt(pw):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT salt FROM syain WHERE pw = %s"

    try:
        cur.execute(sql, (pw,))
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
    sql = "SELECT id, name FROM syain_date WHERE id = %s AND pw = %s"
    try:
        cur.execute(sql, (id, pw))
    except Exception as e:
        print("SQL実行に失敗：" , e)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def yakusyoku(id):
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT yakusyoku FROM syain WHERE id = %s"
    try:
        cur.execute(sql, (id,))
    except Exception as e:
        print("SQL実行に失敗：" , e)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return yakusyoku