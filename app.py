from flask import Flask, request, redirect, render_template,url_for,session
from database import load_jobs_from_db, load_job_from_db, connect

app = Flask(__name__)
app.secret_key = "secret_key"

error_message = ""
allowed_urls = ["/"]

def query_db(query, args=(), one=False):
    conn = connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/", methods=["GET", "POST"])
def index():
    global error_message
    if request.method == "POST":
        login_type = request.form.get("login_type")
        if login_type == "user":
            return redirect(url_for("user_login"))
        elif login_type == "admin":
            return redirect(url_for("admin_login_form"))
        else:
            return "Invalid login choice"
    else:
        return render_template("index.html", error_message=error_message)


@app.route("/user_login", methods=["POST", "GET"])   
def user_login():
    global username, allowed_urls
    allowed_urls.append("/user_login")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = query_db("SELECT * FROM users WHERE username=%s AND password=%s;", (username, password), one=True)
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            allowed_urls.append("/home")
            return redirect(url_for("show_job"))
        else:
            error_message = "Invalid credentials"
            return render_template("index.html", error_message=error_message)
    return render_template("index.html")


@app.route("/admin_authenticate", methods=["POST"])
def admin_authenticate():
    allowed_urls.append("/admin_authenticate")
    admin_username = request.form.get("admin_username")
    admin_password = request.form.get("admin_password")
    if admin_username == 'admin' and admin_password == 'admin':
        allowed_urls.append("/admin")
        return redirect(url_for("admin"))

    return "Invalid Credentials"

@app.route("/home")
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
            "INSERT INTO job_application (job_id, name, email, mobile,user_id) VALUES (%s, %s, %s, %s,%s)",
            (job_id, name, email, phone, session['user_id']),
        )
        conn.commit()
    except Exception as err:
        print(f"Error: {err}")
        return "Failed to apply job", 500
    finally:
        if conn:
            conn.close()

    return redirect("/home")

@app.route("/applications")
def applications():
    try:
        conn = connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM job_application where user_id = %s", (session['user_id'],))
        applications = cursor.fetchall()
    except Exception as err:
        print(f"Error: {err}")
        return "Failed to fetch applications", 500
    finally:
        if conn:
            conn.close()

    return render_template("applications.html", applications=applications)

# @app.route("/admin_login")
# def admin_login():
#     return render_template("admin_login.html")

# @app.route("/admin_authenticate", methods=["POST"])
# def admin_authenticate():
#     username = request.form.get("username")
#     password = request.form.get("password")

#     if username == "admin" and password == "admin":
#         return redirect("/admin")
#     else:
#         return redirect("/admin_login")

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

# @app.route("/edit_job/<int:job_id>", methods=["GET", "POST"])
# def edit_job(job_id):
#     if request.method == "POST":
#         title = request.form.get("title")
#         description = request.form.get("description")
#         location = request.form.get("location")
#         salary = request.form.get("salary")

#         try:
#             conn = connect()
#             cursor = conn.cursor()
#             cursor.execute(
#                 "UPDATE jobs SET title=%s, description=%s, location=%s, salary=%s WHERE id=%s",
#                 (title, description, location, salary, job_id),
#             )
#             conn.commit()
#         except Exception as err:
#             print(f"Error: {err}")
#             return "Failed to update job", 500
#         finally:
#             if conn:
#                 conn.close()

#         return redirect("/admin")

#     try:
#         conn = connect()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM jobs_deets WHERE job_id=%s", (job_id,))
#         jobs_dict = cursor.fetchone()
#     except Exception as err:
#         print(f"Error: {err}")
#         return "Failed to fetch job", 500
#     finally:
#         if conn:
#             conn.close()

#     return render_template("edit_job.html", jobs_dict=jobs_dict)

@app.route("/delete_job/<int:job_id>")
def delete_job(job_id):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs_deets WHERE job_id=%s", (job_id,))
        conn.commit()
    except Exception as err:
        print(f"Error: {err}")
        return "Failed to delete job", 500
    finally:
        if conn:
            conn.close()

    return redirect("/admin")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
        except Exception as err:
            print(f"Error: {err}")
            return "Failed to register", 500
        finally:
            if conn:
                conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            conn = connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
        except Exception as err:
            print(f"Error: {err}")
            return "Failed to login", 500
        finally:
            if conn:
                conn.close()

        if user and user['password'] == password:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return redirect(url_for("show_job"))
        else:
            return "Invalid credentials", 401

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/my_applications")
def my_applications():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    user_id = session['user_id']
    try:
        conn = connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM job_application WHERE user_id = %s", (user_id,))
        applications = cursor.fetchall()
    except Exception as err:
        print(f"Error: {err}")
        return "Failed to fetch applications", 500
    finally:
        if conn:
            conn.close()

    return render_template("my_applications.html", applications=applications)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
