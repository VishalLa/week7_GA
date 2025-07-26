import requests
from flask import (
    render_template,
    url_for,
    redirect,
    Blueprint,
    request,
    flash
)
from applications.config import Config

# API Base
Api_Base = Config.API_BASE

student_controller = Blueprint('student_controller', __name__)

@student_controller.route('/')
def index():
    response = requests.get(f'{Api_Base}/student')

    if response.status_code == 200:
        students = response.json().get('students', [])
    else:
         students = []

    return render_template('index.html', student_list=students)


@student_controller.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        data = {
            'roll_number': request.form['roll'],
            'first_name': request.form['f_name'],
            'last_name': request.form['l_name']
        }

        response = requests.post(f'{Api_Base}/student/create', json=data)

        if response.status_code == 200:
            return redirect(url_for('index'))
        
        elif response.status_code == 409:
            return render_template('student_exists.html')

        elif response.status_code == 400:
            return redirect(url_for('create_student'))
        
        return redirect(url_for('create_student'))
        
    return render_template('create_student.html')


@student_controller.route('/student/<int:student_id>/delete', methods=['GET'])
def delete_student(student_id):
    requests.delete(f'{Api_Base}/student/{student_id}/delete')
    return redirect(url_for('index'))


@student_controller.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = requests.get(f'{Api_Base}/student/{student_id}/update')
    enrollments = requests.get(f'{Api_Base}/student/enrollment/{student_id}')
    
    student_course_enrollment = enrollments.json()
    courses = student_course_enrollment['estudent_id']

    if request.method == 'POST':
        data = {
            'roll_number': request.form['roll'],
            'first_name': request.form['f_name'],
            'last_name': request.form['l_name']
        }
        
        response = requests.post(f'{Api_Base}/student/{student_id}/update', json=data)
        
        if response.status_code == 400:
            return redirect(url_for('update_student'))
        
        return redirect(url_for('index'))

    return render_template('update_student.html', student=student.json(), course_list=courses)


@student_controller.route('/student/<int:student_id>', methods=['GET'])
def student_detail(student_id):
    student = requests.get(f'{Api_Base}/student/{student_id}')
    student_enrollment = requests.get(f'{Api_Base}/student/enrollment/{student_id}')

    return render_template('student_enrollment.html', student=student.json(), enrollments=student_enrollment.json().get('estudent_id', []))


@student_controller.route('/student/<int:student_id>/withdraw/<int:course_id>', methods=['GET'])
def withdraw_student(student_id, course_id):
    requests.get(f'{Api_Base}/student/{student_id}/withdraw/{course_id}')
    return redirect(url_for('index'))
