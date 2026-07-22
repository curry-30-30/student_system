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
    errors = []
    if request.method == "POST":
        name = request.form["name"].strip()
        sid = request.form["sid"].strip()
        age = request.form["age"].strip()
        clazz = request.form["clazz"].strip()

        # 验证（收集所有错误，而非只报一个）
        if any(c.isdigit() for c in name):
            errors.append("姓名不能包含数字")
        if not sid.isdigit():
            errors.append("学号只能输入数字")
        if not age.isdigit():
            errors.append("年龄只能输入数字")

        if not errors:
            conn = sqlite3.connect("student.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO student(name,student_id,age,clazz) VALUES (?,?,?,?)", (name, sid, age, clazz))
            conn.commit()
            conn.close()
            return redirect("/student_list")

        # 验证失败时返回表单，保留已填内容
        return render_template("add.html", errors=errors, name=name, sid=sid, age=age, clazz=clazz)

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