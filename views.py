# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 17:23:46 2020

@author: NotBlue
"""

from flask import Flask, render_template, request
import sqlite3
import re

app = Flask(__name__)

def createConnection(name):
        try:
            db = sqlite3.connect(name)
            return db
        except:
            print('error while creating conenciton')

def createTable(cursor, db):
    try:
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS datas(
                        name TEXT,
                        number PRIMARY KEY)
                    ''')
        db.commit()
    except:
        print('error while creating table')

@app.route('/', methods=['GET', 'POST'])
def index():
    db = createConnection("data.db")
    cursor = db.cursor()
    createTable(cursor, db)
    cursor.execute("SELECT number FROM datas")
    db.commit()
    lenght = len(cursor.fetchall())
    if request.method == "POST":
        result=request.form
        n = result['search']
        if bool(re.match("^[A-Za-z-]", n)) == False:
            return render_template("index.html", error='Invalid Character in your research', total=lenght)
        else:
            cursor.execute("SELECT * FROM datas WHERE name=?", (n,))
            db.commit()
            data = cursor.fetchall()
            if len(data) == 0:
                return render_template("index.html", error='This number is not in the database',total=lenght)
            return render_template("index.html", data=data,total=lenght)
    return render_template("index.html", total=lenght)
    
@app.route('/adding',methods = ['POST', 'GET'])
def adding():
    db = createConnection("data.db")
    cursor = db.cursor()
    createTable(cursor, db)
    cursor.execute("SELECT number FROM datas")
    db.commit()
    lenght = len(cursor.fetchall())
    if request.method == "POST":
        result=request.form
        n = result['nom']
        p = result['numéro']
        if (bool(re.match("^[A-Za-z]", n)) == False or bool(re.match("^[0-9]", p)) == False) or (len(p) != 10):
            return render_template("adding.html",error = 'Invalid Character in your input', total=lenght)
        try:
            cursor.execute('''INSERT INTO datas(name, number) VALUES (?, ?)''', (n, p))
            db.commit()
            cursor.execute("SELECT number FROM datas")
            db.commit()
            lenght = len(cursor.fetchall())
        except db.IntegrityError as e:
            print(f"error with insertion: {e}")
            return render_template("adding.html",error = 'This number has already been added', total=lenght)
        return render_template("adding.html",nom=n, numéro=p, total=lenght)
    return render_template("adding.html", total=lenght)
    
app.run(debug=True)