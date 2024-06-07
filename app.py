from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",
        database="Flutter"
    )
    cursor = db.cursor(dictionary=True)
except mysql.connector.Error as err:
    db = None
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

@app.route('/users', methods=['GET'])
def get_users():
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor.execute("SELECT * FROM employee_details")
    users = cursor.fetchall()
    return jsonify(users)

@app.route('/add_user', methods=['POST'])
def add_user():
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    try:
        cursor.execute("INSERT INTO employee_details (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()
        return jsonify({"message": "User added successfully!"}), 201
    except mysql.connector.Error as err:
        print("Failed to insert user:", err)
        return jsonify({"error": "Failed to insert user"}), 500

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    try:
        cursor.execute("DELETE FROM employee_details WHERE email = %s", (email,))
        db.commit()
        return jsonify({"message": "User deleted successfully!"}), 200
    except mysql.connector.Error as err:
        print("Failed to delete user:", err)
        return jsonify({"error": "Failed to delete user"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
