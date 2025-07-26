import requests
from flask import Flask
from flask import render_template
from flask_restful import Api

from applications.API.student_API import (
    Student_API,
    Student_Create_API,
    Student_GetALL_API,
    StudentDeleteAPI,
    StudentUpdateAPI
)
from applications.API.enrollment_API import (
    Enrollment_GET_course_enrollment,
    Enrollment_GET_student_enrollment,
    WithdrawStudent
)
from applications.API.course_API import (
    Course_API,
    Course_Create_API,
    Course_GetALL_API,
    CourseDeleteAPI,
    CourseUpdateAPI
)

from applications.controllers.studentcontrollers import student_controller
from applications.controllers.coursecontrollers import course_controller

from applications.config import Config
from applications.database import db


Api_Base = Config.API_BASE
app = None
api = None 

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api = Api(app)
    app.app_context().push()

    # register endpoints
    api.add_resource(Student_Create_API, '/student/create')
    api.add_resource(Student_GetALL_API, '/student')
    api.add_resource(Student_API, '/student/<int:student_id>')
    api.add_resource(StudentUpdateAPI, '/student/<int:student_id>/update')
    api.add_resource(StudentDeleteAPI, '/student/<int:student_id>/delete')

    api.add_resource(Enrollment_GET_student_enrollment, '/student/enrollment/<int:student_id>')
    api.add_resource(WithdrawStudent, '/student/<int:student_id>/withdraw/<int:course_id>')
    api.add_resource(Enrollment_GET_course_enrollment, '/course/enrollment/<int:course_id>')

    api.add_resource(Course_API, '/course/<int:course_id>')
    api.add_resource(Course_GetALL_API, '/course')
    api.add_resource(Course_Create_API, '/course/create')
    api.add_resource(CourseUpdateAPI, '/course/<int:course_id>/update')
    api.add_resource(CourseDeleteAPI, '/course/<int:course_id>/delete')

    # register controller
    app.register_blueprint(student_controller)
    app.register_blueprint(course_controller)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
