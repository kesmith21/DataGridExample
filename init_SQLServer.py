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

app = Flask(__name__)
app.secret_key = 'many random bytes'

# mydb = pymssql.connect(host=r'(localdb)\V11.0', user=r'TestUser', password=r'1234',database=r'QE')
mydb = pymssql.connect(host=r'V01SQL01', user=r'guest', password=r'guest',database=r'InfopumpDB')

@app.route('/')
def Index():
    cur = mydb.cursor()
    # cur = mydb.cursor()
    # cur.execute("SELECT TOP (1) ITEM_ID, QUANTITY, COST  FROM [InfopumpDB].[dbo].[PARSCIT] where ITEM_ID  = '426110614000'  order by SEQUENCE desc")
    # data = cur.fetchall()
    # cur.close()


    # return render_template('index2.html', students=data)
    # print(data)
    # return render_template('PriceSearch.html', prices=data)
    return render_template('PriceSearch.html')


@app.route('/search', methods = ['POST'])
def search():

    if request.method == "POST":
        part = request.form['part']
        part = "%" + part + "%"

        cur = mydb.cursor()

        # cur = mydb.cursor()
        # print (name, email, phone)
        # print(part)
        # return (request.form['part'])
        # cur.execute("""SELECT TOP (1) ITEM_ID, QUANTITY, COST, COST/QUANTITY as Each  FROM [InfopumpDB].[dbo].[PARSCIT] where ITEM_ID  like %s
        # and QUANTITY >0 and COST > 0
        # order by SEQUENCE desc""",
        #             (part))
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

@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mydb.cursor()
        # cur = mydb.cursor()
        # print (name, email, phone)
        cur.execute("INSERT INTO students"
                    " (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        cur.connection.commit()
        return redirect(url_for('Index'))

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

if __name__ == "__main__":
    app.run(debug=True)
