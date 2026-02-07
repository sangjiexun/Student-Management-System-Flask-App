from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from models import User, Class, Student, Grade, Attendance
from forms import LoginForm, RegistrationForm, StudentForm, ClassForm, GradeForm, AttendanceForm, SearchForm
from datetime import datetime

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # In production, use hashed passwords
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,  # In production, use hashed passwords
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

# Index route
@app.route('/index')
@login_required
def index():
    # Get statistics
    total_students = Student.query.count()
    total_classes = Class.query.count()
    total_users = User.query.count()
    
    return render_template('index.html', title='Home', 
                         total_students=total_students, 
                         total_classes=total_classes, 
                         total_users=total_users)

# Students route
@app.route('/students')
@login_required
def students():
    # Get all students
    students = Student.query.all()
    
    return render_template('students.html', title='Students', students=students)

# Student detail route
@app.route('/student/<int:student_id>')
@login_required
def student_detail(student_id):
    student = Student.query.get_or_404(student_id)
    
    # Get student's grades
    grades = Grade.query.filter_by(student_id=student_id).all()
    
    # Get student's attendance
    attendances = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.date.desc()).limit(10).all()
    
    return render_template('student_detail.html', title=f'{student.first_name} {student.last_name}', 
                         student=student, grades=grades, attendances=attendances)

# Add student route
@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = StudentForm()
    
    # Populate class choices
    form.class_id.choices = [(class_.id, class_.name) for class_ in Class.query.all()]
    
    if form.validate_on_submit():
        # Check if student ID already exists
        existing_student = Student.query.filter_by(student_id=form.student_id.data).first()
        if existing_student:
            flash('Student ID already exists', 'danger')
            return redirect(url_for('add_student'))
        
        student = Student(
            student_id=form.student_id.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data,
            class_id=form.class_id.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Student has been added', 'success')
        return redirect(url_for('students'))
    
    return render_template('add_student.html', title='Add Student', form=form)

# Edit student route
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    
    # Populate class choices
    form.class_id.choices = [(class_.id, class_.name) for class_ in Class.query.all()]
    
    if form.validate_on_submit():
        # Check if student ID already exists (excluding current student)
        existing_student = Student.query.filter(
            Student.student_id == form.student_id.data,
            Student.id != student_id
        ).first()
        if existing_student:
            flash('Student ID already exists', 'danger')
            return redirect(url_for('edit_student', student_id=student_id))
        
        student.student_id = form.student_id.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.gender = form.gender.data
        student.date_of_birth = form.date_of_birth.data
        student.address = form.address.data
        student.phone = form.phone.data
        student.email = form.email.data
        student.class_id = form.class_id.data
        
        db.session.commit()
        flash('Student has been updated', 'success')
        return redirect(url_for('student_detail', student_id=student_id))
    
    return render_template('add_student.html', title='Edit Student', form=form)

# Delete student route
@app.route('/delete_student/<int:student_id>')
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    # Check if student has grades or attendance records
    if student.grades or student.attendances:
        flash('Cannot delete student with grades or attendance records', 'danger')
        return redirect(url_for('student_detail', student_id=student_id))
    
    db.session.delete(student)
    db.session.commit()
    flash('Student has been deleted', 'success')
    return redirect(url_for('students'))

# Classes route
@app.route('/classes')
@login_required
def classes():
    # Get all classes
    classes = Class.query.all()
    
    return render_template('classes.html', title='Classes', classes=classes)

# Class detail route
@app.route('/class/<int:class_id>')
@login_required
def class_detail(class_id):
    class_ = Class.query.get_or_404(class_id)
    
    # Get students in this class
    students = Student.query.filter_by(class_id=class_id).all()
    
    return render_template('class_detail.html', title=class_.name, class_=class_, students=students)

# Add class route
@app.route('/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    form = ClassForm()
    
    if form.validate_on_submit():
        # Check if class name already exists
        existing_class = Class.query.filter_by(name=form.name.data).first()
        if existing_class:
            flash('Class name already exists', 'danger')
            return redirect(url_for('add_class'))
        
        class_ = Class(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(class_)
        db.session.commit()
        flash('Class has been added', 'success')
        return redirect(url_for('classes'))
    
    return render_template('add_class.html', title='Add Class', form=form)

# Edit class route
@app.route('/edit_class/<int:class_id>', methods=['GET', 'POST'])
@login_required
def edit_class(class_id):
    class_ = Class.query.get_or_404(class_id)
    form = ClassForm(obj=class_)
    
    if form.validate_on_submit():
        # Check if class name already exists (excluding current class)
        existing_class = Class.query.filter(
            Class.name == form.name.data,
            Class.id != class_id
        ).first()
        if existing_class:
            flash('Class name already exists', 'danger')
            return redirect(url_for('edit_class', class_id=class_id))
        
        class_.name = form.name.data
        class_.description = form.description.data
        
        db.session.commit()
        flash('Class has been updated', 'success')
        return redirect(url_for('class_detail', class_id=class_id))
    
    return render_template('add_class.html', title='Edit Class', form=form)

# Delete class route
@app.route('/delete_class/<int:class_id>')
@login_required
def delete_class(class_id):
    class_ = Class.query.get_or_404(class_id)
    
    # Check if class has students
    if class_.students:
        flash('Cannot delete class with students', 'danger')
        return redirect(url_for('class_detail', class_id=class_id))
    
    db.session.delete(class_)
    db.session.commit()
    flash('Class has been deleted', 'success')
    return redirect(url_for('classes'))

# Grades route
@app.route('/grades')
@login_required
def grades():
    # Get all grades
    grades = Grade.query.all()
    
    return render_template('grades.html', title='Grades', grades=grades)

# Add grade route
@app.route('/add_grade', methods=['GET', 'POST'])
@login_required
def add_grade():
    form = GradeForm()
    
    # Populate student choices
    form.student_id.choices = [(student.id, f'{student.first_name} {student.last_name} ({student.student_id})') for student in Student.query.all()]
    
    if form.validate_on_submit():
        grade = Grade(
            student_id=form.student_id.data,
            subject=form.subject.data,
            score=form.score.data,
            grade=form.grade.data,
            semester=form.semester.data,
            academic_year=form.academic_year.data
        )
        db.session.add(grade)
        db.session.commit()
        flash('Grade has been added', 'success')
        return redirect(url_for('grades'))
    
    return render_template('add_grade.html', title='Add Grade', form=form)

# Edit grade route
@app.route('/edit_grade/<int:grade_id>', methods=['GET', 'POST'])
@login_required
def edit_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    form = GradeForm(obj=grade)
    
    # Populate student choices
    form.student_id.choices = [(student.id, f'{student.first_name} {student.last_name} ({student.student_id})') for student in Student.query.all()]
    
    if form.validate_on_submit():
        grade.student_id = form.student_id.data
        grade.subject = form.subject.data
        grade.score = form.score.data
        grade.grade = form.grade.data
        grade.semester = form.semester.data
        grade.academic_year = form.academic_year.data
        
        db.session.commit()
        flash('Grade has been updated', 'success')
        return redirect(url_for('grades'))
    
    return render_template('add_grade.html', title='Edit Grade', form=form)

# Delete grade route
@app.route('/delete_grade/<int:grade_id>')
@login_required
def delete_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    db.session.delete(grade)
    db.session.commit()
    flash('Grade has been deleted', 'success')
    return redirect(url_for('grades'))

# Attendance route
@app.route('/attendance')
@login_required
def attendance():
    # Get all attendance records
    attendances = Attendance.query.order_by(Attendance.date.desc()).all()
    
    return render_template('attendance.html', title='Attendance', attendances=attendances)

# Add attendance route
@app.route('/add_attendance', methods=['GET', 'POST'])
@login_required
def add_attendance():
    form = AttendanceForm()
    
    # Populate student choices
    form.student_id.choices = [(student.id, f'{student.first_name} {student.last_name} ({student.student_id})') for student in Student.query.all()]
    
    if form.validate_on_submit():
        # Check if attendance record already exists for this student on this date
        existing_attendance = Attendance.query.filter_by(
            student_id=form.student_id.data,
            date=form.date.data
        ).first()
        if existing_attendance:
            flash('Attendance record already exists for this student on this date', 'danger')
            return redirect(url_for('add_attendance'))
        
        attendance = Attendance(
            student_id=form.student_id.data,
            date=form.date.data,
            status=form.status.data,
            notes=form.notes.data
        )
        db.session.add(attendance)
        db.session.commit()
        flash('Attendance has been added', 'success')
        return redirect(url_for('attendance'))
    
    # Set default date to today
    form.date.data = datetime.utcnow().date()
    
    return render_template('add_attendance.html', title='Add Attendance', form=form)

# Edit attendance route
@app.route('/edit_attendance/<int:attendance_id>', methods=['GET', 'POST'])
@login_required
def edit_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    form = AttendanceForm(obj=attendance)
    
    # Populate student choices
    form.student_id.choices = [(student.id, f'{student.first_name} {student.last_name} ({student.student_id})') for student in Student.query.all()]
    
    if form.validate_on_submit():
        # Check if attendance record already exists for this student on this date (excluding current record)
        existing_attendance = Attendance.query.filter(
            Attendance.student_id == form.student_id.data,
            Attendance.date == form.date.data,
            Attendance.id != attendance_id
        ).first()
        if existing_attendance:
            flash('Attendance record already exists for this student on this date', 'danger')
            return redirect(url_for('edit_attendance', attendance_id=attendance_id))
        
        attendance.student_id = form.student_id.data
        attendance.date = form.date.data
        attendance.status = form.status.data
        attendance.notes = form.notes.data
        
        db.session.commit()
        flash('Attendance has been updated', 'success')
        return redirect(url_for('attendance'))
    
    return render_template('add_attendance.html', title='Edit Attendance', form=form)

# Delete attendance route
@app.route('/delete_attendance/<int:attendance_id>')
@login_required
def delete_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    db.session.delete(attendance)
    db.session.commit()
    flash('Attendance has been deleted', 'success')
    return redirect(url_for('attendance'))

# Search route
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    students = []
    
    if form.validate_on_submit():
        search_term = form.search.data
        
        # Search in student names, IDs, and classes
        students = Student.query.filter(
            db.or_(
                Student.first_name.ilike(f'%{search_term}%'),
                Student.last_name.ilike(f'%{search_term}%'),
                Student.student_id.ilike(f'%{search_term}%'),
                Student.class_id.in_(
                    db.session.query(Class.id).filter(Class.name.ilike(f'%{search_term}%'))
                )
            )
        ).all()
    
    return render_template('search.html', title='Search', form=form, students=students)

# Users route
@app.route('/users')
@login_required
def users():
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    # Get all users
    users = User.query.all()
    
    return render_template('users.html', title='Users', users=users)

# Add user route
@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,  # In production, use hashed passwords
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User has been created', 'success')
        return redirect(url_for('users'))
    
    return render_template('register.html', title='Add User', form=form)

# Delete user route
@app.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    # Check if user is the current user
    if user.id == current_user.id:
        flash('Cannot delete your own account', 'danger')
        return redirect(url_for('users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted', 'success')
    return redirect(url_for('users'))