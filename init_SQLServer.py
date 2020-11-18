from flask import Flask, render_template, request, redirect, url_for, flash
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

mydb = pymssql.connect(host=r'(localdb)\V11.0', user=r'TestUser', password=r'1234',database=r'QE')

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route('/')
def Index():

    return render_template('PriceSearch.html')


@app.route('/search', methods = ['POST'])
def search():

    if request.method == "POST":
        part = request.form['part']
        part = "%" + part + "%"

        cur = mydb.cursor()

        cur.execute("""SELECT  dbo.PARSCIT.ITEM_ID, dbo.PARSCIT.QUANTITY, dbo.PARSCIT.COST
,format(cast(case when COST>0 and QUANTITY >0 then COST/QUANTITY else 0 end as decimal(10,2)),'C', 'en-US' )  AS Each
--,cast(COST/QUANTITY as decimal(10,2))*1  AS Each
FROM            dbo.PARSCIT INNER JOIN
                             (SELECT        MAX(SEQUENCE) AS Expr1, ITEM_ID
                               FROM            dbo.PARSCIT AS PARSCIT_1
                               WHERE        (ITEM_ID like  %s)
                               and QUANTITY >0 and COST > 0
                               GROUP BY ITEM_ID) AS dtLastRecord ON dbo.PARSCIT.SEQUENCE = dtLastRecord.Expr1 AND dbo.PARSCIT.ITEM_ID = dtLastRecord.ITEM_ID
                               where QUANTITY >0 and COST > 0""",(part))
        data = cur.fetchall()
        cur.close()
        return render_template('PriceSearch.html', prices=data)

@app.route('/insertBook', methods = ['POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    # if request.method == "GET":
    #     cursor = conn.execute("SELECT * FROM book")
    #     books = [
    #         dict(id=row[0], author=row[1], language=row[2], title=row[3])
    #         for row in cursor.fetchall()
    #     ]
    #     if books is not None:
    #         return jsonify(books)

    if request.method == "POST":
        new_author = request.form["author"]
        new_lang = request.form["language"]
        new_title = request.form["title"]
        sql = """INSERT INTO book (author, language, title)
                 VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        return f"Book with the id: 0 created successfully", 201

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mydb.cursor()
    # cur = mydb.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    cur.connection.commit()
    return redirect(url_for('Index'))

@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mydb.cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        # flash("Data Updated Successfully")
        cur.connection.commit()
        return redirect(url_for('Index'))

@app.route('/File')
def FileList():
    root = "C:\Kent Smith"
    pattern = "*.jpg"
    keylist=[]
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                # print(os.path.join(path, name))
                # keylist.append(Path(os.path.join(path, name)).absolute().as_uri())
                # keylist.append(time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(os.path.getmtime(os.path.join(path, name)))))

                keylist.append(dict(FileName=Path(os.path.join(path, name)).absolute().as_uri(),
                                    LastMod=time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(os.path.getmtime(os.path.join(path, name))))))
    # print(keylist)
    return render_template('FileList.html', data=keylist)

@app.route('/insertBook', methods = ['POST'])
def insert():
    def books():
        conn = db_connection()
        cursor = conn.cursor()

        if request.method == "GET":
            cursor = conn.execute("SELECT * FROM book")
            books = [
                dict(id=row[0], author=row[1], language=row[2], title=row[3])
                for row in cursor.fetchall()
            ]
            if books is not None:
                return jsonify(books)

        if request.method == "POST":
            new_author = request.form["author"]
            new_lang = request.form["language"]
            new_title = request.form["title"]
            sql = """INSERT INTO book (author, language, title)
                     VALUES (?, ?, ?)"""
            cursor = cursor.execute(sql, (new_author, new_lang, new_title))
            conn.commit()
            return f"Book with the id: 0 created successfully", 201

if __name__ == "__main__":
    app.run(debug=True)
