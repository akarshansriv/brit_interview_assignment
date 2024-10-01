# brit_interview_assignment
This repository contains a simple web application using Javascript and python fastapi where users can add some specific items and later see the total cost once he is done adding items.

""" Steps To Run the application in local """:
""Create a virtual env using venv cammand
    python -m venv <envname>
    and run 
    pip install -r requirements.txt.""
"""Create Database
    run create_db.py to create database and tables
    run populate_db.by to add items to db."""
""Rename dotenv file to .env and add database URL of your local db_name, Secret key, etc to it.""
"""
""Run the following command from root dir""
"""uvicorn main:app --reload" or "uvicorn main:app" if you wish to run without reload"""