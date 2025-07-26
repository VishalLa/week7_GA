from flask_restful import (
    Resource,
    Api,
    fields,
    marshal_with,
    reqparse
)
from ..database import db
from applications.model import Student
from .validation import NotFoundError, DuplicateError, StudentValidationError


student_fields = {
    'student_id': fields.Integer,
    'roll_number': fields.String,
    'first_name': fields.String,
    'last_name': fields.String
}

student_list_fields = {
    'students': fields.List(fields.Nested(student_fields))
}

# Paraser for new student
create_parse = reqparse.RequestParser()
create_parse.add_argument('roll_number', required=True, type=str)
create_parse.add_argument('first_name', required=True, type=str)
create_parse.add_argument('last_name', type=str)

# Paraser for update student
update_parse = reqparse.RequestParser()
update_parse.add_argument('roll_number', required=True, type=str)
update_parse.add_argument('first_name', required=True, type=str)
update_parse.add_argument('last_name', type=str)


# '/student/<int:student_id>'
class Student_API(Resource):
    @marshal_with(student_fields)
    def get(self, student_id):
        student = db.session.query(Student).filter_by(student_id = student_id).first()
        
        if not student:
            raise NotFoundError(status_code=404)
        
        return student, 200


# '/student'
class Student_GetALL_API(Resource):
    @marshal_with(student_list_fields)
    def get(self):
        students = db.session.query(Student).all()

        if not students:
            raise NotFoundError(status_code=404)

        return {'students': students}, 200 
    

# '/student/create'
class Student_Create_API(Resource):
    @marshal_with(student_fields)
    def post(self):
        args = create_parse.parse_args()
        roll_number = args['roll_number']
        first_name = args['first_name']
        last_name = args['last_name']

        existing = db.session.query(Student).filter_by(roll_number=roll_number).first()
        if existing:
            raise DuplicateError(status_code=409)

        if not roll_number:
            raise StudentValidationError(
                status_code=400,
                error_code='STUDENT001',
                error_message='roll number is required'
            )
        
        if not first_name:
            raise StudentValidationError(
                status_code=400,
                error_code='STUDENT002',
                error_message='first name is required'
            )
        
        new_student = Student(
            roll_number = roll_number,
            first_name = first_name,
            last_name = last_name
        )

        db.session.add(new_student)
        db.session.commit()
        return new_student, 200


# '/student/<int:student_id>/update'
class StudentUpdateAPI(Resource):
    def post(self, student_id):
        args = update_parse.parse_args()
        student = db.session.query(Student).filter_by(student_id = student_id).first()

        if not student:
            raise NotFoundError(status_code=404)

        if not args['first_name']:
            raise  StudentValidationError(
                status_code=400,
                error_code='STUDENT02',
                error_message='first name is required'
            )
        
        student.roll_number = args['roll_number']
        student.first_name = args['first_name']
        student.last_name = args['last_name']

        db.session.commit()
        return student, 200


# '/student/<int:student_id>/delete'
class StudentDeleteAPI(Resource):
    def get(self, student_id):
        student = db.session.query(Student).filter_by(student_id=student_id).first()
        if not student:
            raise NotFoundError(status_code=404)
        db.session.delete(student)
        db.session.commit()
        return '', 200
