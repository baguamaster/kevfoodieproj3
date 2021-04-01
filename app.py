from flask import Flask, render_template, request, redirect, url_for
import random
import pymongo
from bson.objectid import ObjectId
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask('app')

# link to mongoDB
MONGO_DB="mongodb+srv://admin-ang:a1b2c3d4@cluster0.hocdb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
DATABASE_NAME="profile"
COLLECTION_NAME="personal-details"

#  Setup to Connect to MongoDB
conn = pymongo.MongoClient(MONGO_DB)
data = conn[DATABASE_NAME][COLLECTION_NAME]

# read
@app.route('/')
def index():
  users = data.find({})
  
  return render_template('index.html', data=users)


# create
@app.route("/create")
def create():
  return render_template('create.html')
@app.route("/create", methods=["POST"])
def insert():
#   # text input
  new_user = request.form.get("username")
  # radio input
  new_gender = request.form.get('gender')
  # checkbox input
  date_input = request.form.get('date_input')
  print(date_input)

  data.insert({
    'username':new_user,
    'gender' : new_gender,

  })

  return redirect(url_for('index'))


# Edit
@app.route("/edit/<edit_id>")
def edit(edit_id):
  user_to_edit = data.find_one({
      "_id":ObjectId(edit_id)
  })
  print(user_to_edit)
  return render_template('edit.html', user=user_to_edit)

@app.route("/edit/<edit_id>", methods=["POST"])
def update(edit_id):
  # get info from html
  new_user = request.form.get("username")
  new_gender = request.form.get("gender")

  # update MONGO database 
  data.update({
    "_id" : ObjectId(edit_id)
  },{
    '$set': {
      'username': new_user,
      'gender': new_gender
    }
  })    
  return redirect(url_for('index'))

@app.route("/confirm_delete/<edit_id>")
def confirm_delete(edit_id):
  return render_template('confirm_delete.html', user_id=edit_id)

@app.route("/delete/<edit_id>")
def delete(edit_id):
  data.delete_one({
    '_id':ObjectId(edit_id)
  })
  return redirect(url_for('index'))

app.run(host='0.0.0.0', port=8080)
