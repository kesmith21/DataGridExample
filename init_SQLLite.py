from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pymssql
# import PyMySQL
# from flask_mysqldb import MySQL
# import mysql.connector
import os
from fnmatch import fnmatch
from pathlib import Path
import time
import requests
import sqlite3

app = Flask(__name__)
app.secret_key = 'many random bytes'

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/')
def books():
    conn = db_connection()

    cursor = conn.execute("SELECT * FROM book")
    books = cursor.fetchall()
    cursor.close()

    return render_template('BooksSQLLite.html',r=books)


@app.route('/insert', methods = ['POST'])
def insert():
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

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    conn = db_connection()
    conn.execute("DELETE FROM book WHERE id= ?", (id_data))
    conn.commit()
    conn.close()
    return redirect(url_for('books'))

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        conn = db_connection()
        conn.execute("""
               UPDATE book
               SET author=?, language=?, title=?
               WHERE id=?
            """, (author, language, title, id_data))
        # flash("Data Updated Successfully")
        conn.commit()
        return redirect(url_for('books'))


if __name__ == "__main__":
    app.run(debug=True)
