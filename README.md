# 🎓 学生管理系统

一个基于 **Flask + SQLite** 的轻量级学生信息管理 Web 应用。

## ✨ 功能

- **登录验证** — 管理员账号密码登录
- **学生列表** — 展示所有学生信息，序号自动排序
- **新增学生** — 添加学生（姓名、学号、年龄、班级）
- **删除学生** — 一键删除学生记录
- **表单校验** — 姓名不能含数字，学号和年龄只能输入数字（错误提示红色展示）
- **操作反馈** — 保存/删除成功后弹出自动淡出的提示

## 🚀 快速开始

### 环境要求

- Python 3.7+

### 安装与运行

```bash
# 克隆仓库
git clone https://github.com/curry-30-30/student_system.git
cd student_system

# （推荐）创建虚拟环境
python -m venv .venv

# Windows 激活虚拟环境
.venv\Scripts\Activate.ps1
# macOS / Linux 激活虚拟环境
# source .venv/bin/activate

# 安装依赖
pip install flask

# 启动服务
python app.py
```

打开浏览器访问 **http://127.0.0.1:5000**

### 默认登录账号

| 用户名 | 密码 |
|-------|------|
| admin | 123456 |

## 📁 项目结构

```
student_system/
├── app.py              # Flask 主程序（路由 + 数据库操作）
├── templates/
│   ├── login.html      # 登录页面
│   ├── list.html       # 学生列表页面
│   └── add.html        # 新增学生页面
├── .gitignore
└── README.md
```

## 🛠️ 技术栈

- **后端**: Python / Flask
- **数据库**: SQLite
- **前端**: HTML / CSS (Flexbox 居中布局)

## 📄 许可证

MIT
