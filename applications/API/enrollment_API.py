from flask_restful import (
    Resource,
    Api,
    fields,
    marshal_with,
    reqparse
)
from ..database import db
from applications.model import Enrollment, Student, Course
courses = {
    'course_id': fields.Integer,
    'course_code': fields.String,
    'course_name': fields.String,
    'course_description': fields.String
}

student_enrollment_list = {
    'estudent_id': fields.List(fields.Nested(courses))
}

students = {
    'student_id': fields.Integer,
    'roll_number': fields.String,
    'first_name': fields.String,
    'last_name': fields.String 
}

course_enrollment_list = {
    'ecourse_id': fields.List(fields.Nested(students))
}


# '/student/enrollment/<int:student_id>'
class Enrollment_GET_student_enrollment(Resource):
    @marshal_with(student_enrollment_list)
    def get(self, student_id):
        enrollment = db.session.query(Enrollment).filter(Enrollment.estudent_id == student_id).all()
        course_ids = [course.ecourse_id for course in enrollment]
        courses = []
        for course_id in course_ids:
            course = db.session.query(Course).filter(Course.course_id == course_id).first()
            if course:
                courses.append(course)
        return {'estudent_id': courses}, 200
    

# '/course/enrollment/<int:course_id>'
class Enrollment_GET_course_enrollment(Resource):
    @marshal_with(course_enrollment_list)
    def get(self, course_id):
        enrollment = db.session.query(Enrollment).filter(Enrollment.ecourse_id == course_id).all()
        student_ids = [student.estudent_id for student in enrollment]
        students = []
        for student_id in student_ids:
            student = db.session.query(Student).filter(Student.student_id == student_id).first()
            if student:
                students.append(student)
        return {'ecourse_id': students}, 200
    

'/student/<int:student_id>/withdraw/<int:course_id>'
class WithdrawStudent(Resource):
    def get(self, student_id, course_id):
        enrollment = db.session.query(Enrollment).filter(
            Enrollment.estudent_id == student_id,
            Enrollment.ecourse_id == course_id
        ).first()
        if enrollment:
            db.session.delete(enrollment)
            db.session.commit()
            return {'message': 'Enrollment deleted successfully'}, 200
        else:
            return {'message': 'Enrollment not found'}, 404