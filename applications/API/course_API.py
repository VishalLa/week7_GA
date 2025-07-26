from flask_restful import (
    Resource,
    Api,
    fields,
    marshal_with,
    reqparse
)
from ..database import db
from applications.model import Course
from .validation import NotFoundError, DuplicateError, CourseValidationError

course_field = {
    'course_id': fields.Integer,
    'course_code': fields.String,
    'course_name': fields.String,
    'course_description': fields.String
}

course_list_field = {
    'courses': fields.List(fields.Nested(course_field))
}

# Paraser for new course
create_course = reqparse.RequestParser()
create_course.add_argument('course_code', required=True, type=str)
create_course.add_argument('course_name', required=True, type=str)
create_course.add_argument('course_description', type=str)

# Paraser for update course 
update_course = reqparse.RequestParser()
update_course.add_argument('course_code', required=True, type=str)
update_course.add_argument('course_name', required=True, type=str)
update_course.add_argument('course_description', type=str)


# '/course/<int:course_id>'
class Course_API(Resource):
    @marshal_with(course_field)
    def get(self, course_id):
        course = db.session.query(Course).filter(Course.course_id==course_id).first()

        if not course:
            raise NotFoundError(status_code=404)
        
        return course, 200

    
# '/course'
class Course_GetALL_API(Resource):
    @marshal_with(course_list_field)
    def get(self):
        courses = db.session.query(Course).all()

        if not courses:
            raise NotFoundError(status_code=404)

        return {'courses': courses}, 200


# '/course/create'
class Course_Create_API(Resource):
    @marshal_with(course_field)
    def post(self):
        args = create_course.parse_args()
        course_code = args['course_code']
        course_name = args['course_name']
        course_description = args['course_description']

        if not args['course_code']:
            raise CourseValidationError(
                status_code=400,
                error_code='COURSE001',
                error_message='course code is required'
            )
        
        if not args['course_name']:
            raise CourseValidationError(
                status_code=400,
                error_code='COURSE002',
                error_message='course name is required'
            )
        
        new_course = Course(
            course_code = course_code,
            course_name = course_name,
            course_description = course_description
        )

        db.session.add(new_course)
        db.session.commit()
        return new_course, 200


# '/course/<int:course_id>/update'
class CourseUpdateAPI(Resource):
    def post(self, course_id):
        args = update_course.parse_args()
        course = db.session.query(Course).filter(Course.course_id == course_id).first()

        if not course:
            raise NotFoundError(status_code=404)
        
        if not args['course_code']:
            raise CourseValidationError(
                status_code=400,
                error_code='COURSE001',
                error_message='course code is required'
            )
        
        if not args['course_name']:
            raise CourseValidationError(
                status_code=400,
                error_code='COURSE002',
                error_message='course name is required'
            )
        
        course.course_code = args['course_code']
        course.course_name = args['course_name']
        course.course_description = args['course_description']

        db.session.commit()
        return course, 200


'/course/<int:course_id>/delete'
class CourseDeleteAPI(Resource):
    def get(self, course_id):
        course = db.session.query(Course).filter(Course.course_id == course_id).first()
        if not course:
            raise NotFoundError(status_code=404)
        db.session.delete(course)
        db.session.commit()
        return '', 200
