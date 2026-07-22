from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "student_system_secret"

# 初始化数据库
def create_db():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    # 学生表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        student_id TEXT,
        age INTEGER,
        clazz TEXT
    )
    ''')
    # 用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    # 插入默认管理员（如果不存在）
    cursor.execute("SELECT COUNT(*) FROM user WHERE username='admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", ("admin", "123456"))
    conn.commit()
    conn.close()

create_db()

# 登录页面
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return redirect("/student_list")
        return render_template("login.html", error="账号或密码错误")
    return render_template("login.html")

# 注册
@app.route("/register", methods=["GET", "POST"])
def register():
    errors = []
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        confirm = request.form["confirm"].strip()

        if not username or not password:
            errors.append("用户名和密码不能为空")
        if password != confirm:
            errors.append("两次密码输入不一致")
        if len(password) < 6:
            errors.append("密码长度不能少于6位")

        if not errors:
            conn = sqlite3.connect("student.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                flash("注册成功，请登录")
                return redirect("/")
            except sqlite3.IntegrityError:
                errors.append("用户名已存在")
            finally:
                conn.close()

        return render_template("register.html", errors=errors, username=username)

    return render_template("register.html")

# 修改密码
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    errors = []
    success = None
    if request.method == "POST":
        username = request.form["username"].strip()
        old_pw = request.form["old_password"].strip()
        new_pw = request.form["new_password"].strip()
        confirm = request.form["confirm"].strip()

        if not username or not old_pw or not new_pw:
            errors.append("请填写完整信息")
        elif new_pw != confirm:
            errors.append("两次新密码输入不一致")
        elif len(new_pw) < 6:
            errors.append("新密码长度不能少于6位")
        else:
            conn = sqlite3.connect("student.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, old_pw))
            if cursor.fetchone():
                cursor.execute("UPDATE user SET password=? WHERE username=?", (new_pw, username))
                conn.commit()
                success = "密码修改成功，请重新登录"
            else:
                errors.append("用户名或原密码错误")
            conn.close()

        if success:
            return render_template("change_password.html", success=success, username=username)
        return render_template("change_password.html", errors=errors, username=username)

    return render_template("change_password.html")

# 用户列表
@app.route("/user_list")
def user_list():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    users = cursor.execute("SELECT id, username, password FROM user").fetchall()
    conn.close()
    return render_template("user_list.html", users=users)

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
            flash("保存成功！")
            return redirect("/student_list")

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
    flash("删除成功！")
    return redirect("/student_list")

# 删除全部学生
@app.route("/delete_all")
def delete_all():
    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student")
    conn.commit()
    conn.close()
    flash("已删除全部学生！")
    return redirect("/student_list")

if __name__ == "__main__":
    app.run(debug=True)
