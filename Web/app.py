import json
import pymysql
import model
from flask import Flask, request, render_template,jsonify
from datetime import datetime

global db, cur

app = Flask(__name__)
db = model.Database() 
app.config['JSON_AS_ASCII'] = False  

db = pymysql.connect(host="localhost", user="raspi", password="0000", db="brewants", charset="utf8")
cur = db.cursor()

@app.route('/request2', methods =['POST'])  
def request2():
    db = model.Database()
    lists =  db.select() 
    print(lists)
    return jsonify(lists) 

@app.route('/chart') 
def form():
    return render_template('chart.html')


if __name__ == '__main__':
      app.run(host='127.0.0.1', port=5000, debug=True)
