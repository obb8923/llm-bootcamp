from flask import Flask, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Juniverse325!",
        database="imageDetact"
    )

@app.route('/show_member', methods=['GET'])
def show_member():
    name = request.args.get('name')
    
    if not name:
        return "이름을 입력해주세요.", 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM member WHERE name = %s"
        cursor.execute(query, (name,))
        
        member = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if member:
            return f"멤버 정보: {member}", 200
        else:
            return f"'{name}' 이름의 멤버를 찾을 수 없습니다.", 40
        
    except mysql.connector.Error as err:
        return f"데이터베이스 오류: {err}", 500