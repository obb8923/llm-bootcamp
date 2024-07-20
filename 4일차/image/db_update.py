from flask import Flask, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Juniverse325!",
        database="board"
    )

@app.route('/add_member', methods=['POST'])
def add_member():
    data = request.get_json()
    company = data.get('company')
    owner_name = data.get('owner_name')
    mail = data.get('mail')
    job = data.get('job')
    address = data.get('address')

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO member (company,owner_name,mail,job,address) VALUES (%s, %s, %s, %s, %s)"
    val = (company,owner_name,mail,job,address)

    cursor.execute(sql, val)
    conn.commit()

    cursor.close()
    conn.close()

    return "명함 등록 완료"

if __name__ == "__main__":
    app.run()

