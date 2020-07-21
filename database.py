import mysql.connector
from hashlib import md5
from Crypto.Cipher import AES
import os
from binascii import unhexlify

def password_hash(password):
    return md5(password.encode()).hexdigest()

key = password_hash('IAMBATMAN')
cypher_tool = AES.new(key, AES.MODE_ECB)

db_user, db_password = 'root', '12345678@aA'

mydb = mysql.connector.connect(
  host="localhost",
  user=db_user,
  password=db_password,
)

def createDatabase():
    cursor = mydb.cursor()
    sql = "CREATE TABLE users (uid INT NOT NULL AUTO_INCREMENT, user VARCHAR(128), password CHAR(32), PRIMARY KEY(uid), UNIQUE(user))"
    cursor.execute(sql)

    cursor = mydb.cursor()
    sql = 'CREATE TABLE passwords (user_id INT, username VARCHAR(128), password VARCHAR(512), website VARCHAR(128), FOREIGN KEY (user_id) REFERENCES users(uid))'
    cursor.execute(sql)

"""cursor = mydb.cursor()
cursor.execute("SHOW DATABASES")
new_db = False

print(list(cursor))
print(('PM',) in list(cursor))"""

try:
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE PM")

    mydb = mysql.connector.connect(
        host="localhost",
        user=db_user,
        password=db_password,
        database="PM"
    )
    print("Creating DB")
    createDatabase()

except:
    mydb = mysql.connector.connect(
        host="localhost",
        user=db_user,
        password=db_password,
        database="PM"
    )

# createDatabase()


def login(user, password):
    sql = "SELECT uid, user, password FROM users WHERE user='{}'".format(user)
    # print(sql)
    try:
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

        # print(result)
        if result[-1] == password_hash(password):
            return result[0]
    except Exception as e:
        print(e)
        pass

    return None
        

def register(user, password):
    pass_hash = password_hash(password)

    sql = "INSERT INTO users(user, password) VALUES ('{}', '{}')".format(user, pass_hash)
    # print(sql)
    try:
        cursor = mydb.cursor()
        cursor.execute(sql)
        mydb.commit()
        return True
    except:
        return False

def encryptPass(password):
    return cypher_tool.encrypt(password.rjust(32)).hex()

def storePassword(uid, website, user, password):
    password = encryptPass(password)

    sql = "INSERT INTO passwords VALUES({}, '{}', '{}', '{}')".format(uid, user, password, website)
    # print(sql)
    try:
        cursor = mydb.cursor()
        cursor.execute(sql)
        mydb.commit()
        return True
    except:
        return False

def decryptPass(password):
    return (cypher_tool.decrypt(unhexlify(password))).decode().strip()

def getPasswords(uid):
    sql = "SELECT username, password, website FROM passwords WHERE user_id={}".format(uid)
    # print(sql)
    pass_list = []
    try:
        cursor = mydb.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        for row in result:
            pass_list.append((row[0], decryptPass(row[1]), row[2]))
    except Exception as e:
        print(e)
        pass

    return pass_list

if __name__ == '__main__':
    enc = encryptPass('pass')
    print(enc)
    dec = decryptPass(enc)
    print(dec)

    print(register('amul', 'pass'))
    print(register('test', '1234'))

    print(login('amul', 'pass'))
    print(login('test', '1243'))

    print(storePassword(1, 'www.google.com', 'amul', 'pass'))
    print(storePassword(1, 'www.facebook.com', 'amul1', 'pass1'))

    print(getPasswords(1))