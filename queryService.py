from flask import Flask, render_template, jsonify, redirect, url_for, flash
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
@app.route('/', methods = ['GET'])
def getbooks():
    r = requests.get("http://localhost:8084/books")
    # payload = {"firstName":"John", "lastName":"Smith"}
    # r = requests.get("https://httpbin.org/get",params=payload)

    return render_template('Books.html',r=r.json())

if __name__ == "__main__":
    app.run(debug=True)
