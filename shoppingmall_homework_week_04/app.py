from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('localhost', 27017);
db = client.dbsparta;


# 1. 기본 홈페이지
@app.route('/')
def home():
    return render_template('index.html')


# 2. API: POST(브라우저에서 온 데이터를 받기, jsonify)
@app.route('/order', methods=['POST'])
def write_order():

    name = request.form['name']
    count = request.form['count']
    address = request.form['address']
    phone = request.form['phone']

    orders = {
        'name': name,
        'count': count,
        'address': address,
        'phone': phone
    }

    db.orderList.insert_one(orders)

    return jsonify({'result': 'success'})

# 3. API: GET(브라우저에 DB 저장 데이터를 주기, jsonify)
@app.route('/order', methods=['GET'])
def read_order():
    ordersList = list(db.orderList.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'ordersList': ordersList})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True);
