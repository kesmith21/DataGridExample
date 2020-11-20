import sqlite3

from flask import Flask, render_template, jsonify, redirect, url_for, flash, request
import pymssql
# import PyMySQL
# from flask_mysqldb import MySQL
# import mysql.connector
import os
from fnmatch import fnmatch
from pathlib import Path
import time
import requests

app = Flask(__name__)
app.secret_key = 'many random bytes'
# https://www.youtube.com/watch?v=qriL9Qe8pJc

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/')
def getbooks():
    r = requests.get("http://localhost:8084/books","GET")

    return render_template('BooksRestAPI.html',r=r.json())

@app.route('/GetUser')
def getbooks():
    r = requests.get("http://tmmk-wwebp26/UserManagementSvc/UserManagementService.svc?wsdl","GET")

    return r.json()


#

@app.route('/insert', methods = ['POST'])
def insert():

    payload = {"author":request.form["author"], "title":request.form["title"], "language":request.form["language"]}
    r = requests.post("http://localhost:8084/books", data=payload)
    return redirect(url_for('getbooks'))

@app.route('/deleteBook/<string:id_data>')
def deleteBook(id_data):

    r = requests.delete("http://localhost:8084/book/"+ id_data)
    return redirect(url_for('getbooks'))


@app.route('/insertBookSQL', methods = ['POST'])
def insertBook():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        new_author = request.form["author"]
        new_lang = request.form["language"]
        new_title = request.form["title"]
        sql = """INSERT INTO book (author, language, title)
                 VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        # return f"Book with the id: 0 created successfully", 201
        flash("Data Updated Successfully")
        return redirect(url_for('books'))


@app.route('/update',methods=['POST','GET'])
def update():
    i = request.form['id']
    payload = {"title": request.form["title"],  "language": request.form["language"], "author": request.form["author"]}
    r = requests.put("http://localhost:8084/book/"+i,data=payload)
    flash("Data Updated Successfully")
    return redirect(url_for('getbooks'))

if __name__ == "__main__":
    app.run(debug=True)
