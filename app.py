from flask import Flask, request, redirect, render_template
from database import load_jobs_from_db, load_job_from_db, connect

app = Flask(__name__)

@app.route("/")
def show_job():
    jobs_dict = load_jobs_from_db()
    if not jobs_dict:
        return "Not Found", 404

    return render_template("home.html", jobs_dict=jobs_dict)

@app.route("/api/jobs")
def list_jobs():
    return load_jobs_from_db()

@app.route("/job/<int:job_id>")
def show_job_details(job_id):
    jobs_dict = load_job_from_db(job_id)
    if not jobs_dict:
        return "Not Found", 404

    return render_template("jobpage.html", jobs_dict=jobs_dict)

@app.route("/apply_job/<int:job_id>", methods=["POST"])
def apply_job(job_id):
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("mobile")

    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO job_application (job_id, name, email, mobile) VALUES (%s, %s, %s, %s)",
            (job_id, name, email, phone),
        )
        conn.commit()
    except Exception as err:
        print(f"Error: {err}")
        return "Failed to apply job", 500
    finally:
        if conn:
            conn.close()

    return redirect(f"/job/{job_id}")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")

@app.route("/admin_authenticate", methods=["POST"])
def admin_authenticate():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "admin":
        return redirect("/admin")
    else:
        return redirect("/admin_login")

@app.route("/admin")
def admin():
    try:
        conn = connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs_deets")
        jobs_dict = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS count, job_id FROM job_application GROUP BY job_id")
        job_counts_result = cursor.fetchall()
        
        # Convert the result into a dictionary for easier access in the template
        job_count = {item['job_id']: item['count'] for item in job_counts_result}

    except Exception as err:
        print(f"Error: {err}")
        return "Failed to fetch jobs", 500
    finally:
        if conn:
            conn.close()

    return render_template("admin.html", jobs_dict=jobs_dict, job_count=job_count)

@app.route("/edit_job/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        location = request.form.get("location")
        salary = request.form.get("salary")

        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE jobs SET title=%s, description=%s, location=%s, salary=%s WHERE id=%s",
                (title, description, location, salary, job_id),
            )
            conn.commit()
        except Exception as err:
            print(f"Error: {err}")
            return "Failed to update job", 500
        finally:
            if conn:
                conn.close()

        return redirect("/admin")

    try:
        conn = connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs_deets WHERE job_id=%s", (job_id,))
        jobs_dict = cursor.fetchone()
    except Exception as err:
        print(f"Error: {err}")
        return "Failed to fetch job", 500
    finally:
        if conn:
            conn.close()

    return render_template("edit_job.html", jobs_dict=jobs_dict)

@app.route("/delete_job/<int:job_id>")
def delete_job(job_id):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs_deets WHERE j_id=%s", (job_id,))
        conn.commit()
    except Exception as err:
        print(f"Error: {err}")
        return "Failed to delete job", 500
    finally:
        if conn:
            conn.close()

    return redirect("/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
