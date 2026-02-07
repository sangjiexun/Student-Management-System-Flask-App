# 学生管理系统

## 项目概述
学生管理系统是一个基于Flask框架开发的学校学生管理系统，支持用户管理、学生管理、班级管理、成绩管理、考勤管理等功能。

## 技术架构

### 后端技术
- **Flask**: Python Web框架
- **Flask-SQLAlchemy**: ORM数据库工具
- **Flask-Migrate**: 数据库迁移工具
- **Flask-Login**: 用户认证管理
- **Flask-WTF**: 表单处理和验证
- **SQLite**: 轻量级数据库系统

### 前端技术
- **Jinja2**: 模板引擎
- **HTML5/CSS3**: 页面结构和样式
- **Bootstrap**: 响应式UI框架

## 项目结构

```
Student-Management-System-Flask-App/
├── static/
│   └── styles.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── students.html
│   ├── student_detail.html
│   ├── add_student.html
│   ├── classes.html
│   ├── class_detail.html
│   ├── add_class.html
│   ├── grades.html
│   ├── add_grade.html
│   ├── attendance.html
│   ├── add_attendance.html
│   ├── users.html
│   └── search.html
├── app.py
├── config.py
├── models.py
├── forms.py
├── routes.py
├── data.sqlite
└── README.md
```

## 核心功能

### 1. 用户管理
- 用户注册和登录
- 用户信息管理
- 管理员权限管理

### 2. 学生管理
- 学生添加、编辑、删除
- 学生信息查询
- 学生详情查看

### 3. 班级管理
- 班级添加、编辑、删除
- 班级信息查询
- 班级学生列表

### 4. 成绩管理
- 成绩添加、编辑、删除
- 成绩查询
- 学生成绩记录

### 5. 考勤管理
- 考勤记录添加、编辑、删除
- 考勤查询
- 学生考勤记录

### 6. 统计功能
- 学生总数统计
- 班级总数统计
- 用户总数统计

## 数据库设计

### 主要数据表
- **user**: 用户信息
- **class**: 班级信息
- **student**: 学生信息
- **grade**: 成绩信息
- **attendance**: 考勤信息

## 快速开始

### 环境要求
- Python 3.6+
- pip

### 安装步骤
1. 克隆仓库
   ```bash
   git clone https://github.com/sangjiexun/Student-Management-System-Flask-App.git
   cd Student-Management-System-Flask-App
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 初始化数据库
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. 运行应用
   ```bash
   python app.py
   ```

## 部署说明

### 生产环境部署
- 使用Gunicorn作为WSGI服务器
- 使用Nginx作为反向代理
- 配置HTTPS
- 启用生产模式

### 环境变量配置
- `SECRET_KEY`: 应用密钥
- `DATABASE_URL`: 数据库连接URL
- `DEBUG`: 调试模式

## 许可证

MIT License

---

# Student Management System

## Project Overview
Student Management System is a Flask-based school student management system, supporting user management, student management, class management, grade management, attendance management, and other functions.

## Technical Architecture

### Backend Technologies
- **Flask**: Python Web framework
- **Flask-SQLAlchemy**: ORM database tool
- **Flask-Migrate**: Database migration tool
- **Flask-Login**: User authentication management
- **Flask-WTF**: Form handling and validation
- **SQLite**: Lightweight database system

### Frontend Technologies
- **Jinja2**: Template engine
- **HTML5/CSS3**: Page structure and styling
- **Bootstrap**: Responsive UI framework

## Project Structure

```
Student-Management-System-Flask-App/
├── static/
│   └── styles.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── students.html
│   ├── student_detail.html
│   ├── add_student.html
│   ├── classes.html
│   ├── class_detail.html
│   ├── add_class.html
│   ├── grades.html
│   ├── add_grade.html
│   ├── attendance.html
│   ├── add_attendance.html
│   ├── users.html
│   └── search.html
├── app.py
├── config.py
├── models.py
├── forms.py
├── routes.py
├── data.sqlite
└── README.md
```

## Core Features

### 1. User Management
- User registration and login
- User information management
- Admin privilege management

### 2. Student Management
- Student addition, editing, and deletion
- Student information query
- Student detail viewing

### 3. Class Management
- Class addition, editing, and deletion
- Class information query
- Class student list

### 4. Grade Management
- Grade addition, editing, and deletion
- Grade query
- Student grade records

### 5. Attendance Management
- Attendance record addition, editing, and deletion
- Attendance query
- Student attendance records

### 6. Statistics Functions
- Total student count statistics
- Total class count statistics
- Total user count statistics

## Database Design

### Main Data Tables
- **user**: User information
- **class**: Class information
- **student**: Student information
- **grade**: Grade information
- **attendance**: Attendance information

## Quick Start

### Environment Requirements
- Python 3.6+
- pip

### Installation Steps
1. Clone the repository
   ```bash
   git clone https://github.com/sangjiexun/Student-Management-System-Flask-App.git
   cd Student-Management-System-Flask-App
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize database
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. Run the application
   ```bash
   python app.py
   ```

## Deployment Instructions

### Production Environment Deployment
- Use Gunicorn as WSGI server
- Use Nginx as reverse proxy
- Configure HTTPS
- Enable production mode

### Environment Variables Configuration
- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: Database connection URL
- `DEBUG`: Debug mode

## License

MIT License