from flask import *
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
host_name = os.getenv("HOST_NAME")
user_name = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
db_name = os.getenv("DB_NAME")


def connect():
    connection = mysql.connector.connect(
        host=host_name, user=user_name, password=password, database=db_name
    )
    return connection


def load_jobs_from_db():
    jobs_dict = {}
    try:
        conn = connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs_deets")
        jobs_db = cursor.fetchall()

        for job in jobs_db:
            jobs_dict[job["j_id"]] = dict(job)

        return jobs_dict
    finally:
        if conn:
            conn.close()


def load_job_from_db(job_id):
    try:
        conn = connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs_deets WHERE j_id = %s", (job_id,))
        job = cursor.fetchone()
        return job
    finally:
        if conn:
            conn.close()
