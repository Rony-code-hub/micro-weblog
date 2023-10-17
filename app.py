import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def create_app():
    app = Flask(__name__)

    password = os.environ.get("MONGODB_PWD")
    connection_string = f"mongodb+srv://rony:{password}@cluster2.ht42g97.mongodb.net/"
    client = MongoClient(connection_string)

    app.dbs = client.microvlog_service

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method=="POST":
            entry_content = request.form.get("content")
            date_formatted = datetime.datetime.today().strftime("%Y-%m-%d")
            app.dbs.my_data.insert_one({"content": entry_content, "date": date_formatted})

        entries_with_date = [
            (
                entry["content"], 
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.dbs.my_data.find({})
        ]
        return render_template("index.html", entries=entries_with_date)
    return app