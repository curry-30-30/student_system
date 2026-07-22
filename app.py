from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 初始化数据库，创建学生表
def create_db():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        student_id TEXT,
        age INTEGER,
        clazz TEXT
    )
    ''')
    conn.commit()
    conn.close()

create_db()

# 登录页面
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "123456":
            return redirect("/student_list")
        return render_template("login.html", error="账号或密码错误")
    return render_template("login.html")

# 学生列表页面
@app.route("/student_list")
def student_list():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    res = cursor.execute("SELECT * FROM student").fetchall()
    conn.close()
    return render_template("list.html", data=res)

# 新增学生
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        sid = request.form["sid"]
        age = request.form["age"]
        clazz = request.form["clazz"]
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO student(name,student_id,age,clazz) VALUES (?,?,?,?)",(name,sid,age,clazz))
        conn.commit()
        conn.close()
        return redirect("/student_list")
    return render_template("add.html")

# 删除学生
@app.route("/delete/<sid>")
def delete(sid):
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE id=?", (sid,))
    conn.commit()
    conn.close()
    return redirect("/student_list")

# 程序启动入口
if __name__ == "__main__":
    app.run(debug=True)