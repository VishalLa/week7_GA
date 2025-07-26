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

course_controller = Blueprint('course_controller', __name__)


@course_controller.route('/courses')
def course_index():
    response = requests.get(f'{Api_Base}/course')

    if response.status_code == 200:
        courses = response.json().get('courses', [])
    else:
        courses = []

    return render_template('course_index.html', course_list = courses)


@course_controller.route('/course/create', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        data = {
            'course_code': request.form['code'],
            'course_name': request.form['c_name'],
            'course_description': request.form['desc']
        }

        response = requests.post(f'{Api_Base}/course/create', json=data)

        if response.status_code == 200:
            return redirect(url_for('course_index'))
        
        elif response.status_code == 409:
            return render_template('course_exists.html')
        
        elif response.status_code == 400:
            return redirect(url_for('create_course'))
        
        return redirect(url_for('create_course'))
    
    return render_template('create_course.html')


@course_controller.route('/course/<int:course_id>/delete', methods=['GET'])
def delete_course(course_id):
    requests.get(f'{Api_Base}/course/{course_id}/delete')
    return redirect(url_for('course_index'))


@course_controller.route('/course/<int:course_id>/update', methods=['GET', 'POST'])
def update_course(course_id):
    course = requests.get(f'{Api_Base}/course/{course_id}/update')

    if request.method == 'POST':
        data = {
            'course_code': request.form['code'],
            'course_name': request.form['c_name'],
            'course_description': request.form['desc']
        }

        response = requests.post(f'{Api_Base}/course/{course_id}/update', json=data)

        if response.status_code == 400:
            return redirect(url_for('update_course'))
        
        return redirect(url_for('course_index'))
    
    return render_template('update_course.html', course=course.json())


@course_controller.route('/course/<int:course_id>', methods=['GET'])
def course_detail(course_id):
    course = requests.get(f'{Api_Base}/course/{course_id}')
    enrollments = requests.get(f'{Api_Base}/course/enrollment/{course_id}')

    return render_template('course_enrollment.html', enrollments=enrollments.json().get('ecourse_id', []), course=course.json())

