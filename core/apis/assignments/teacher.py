from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_submitted_assignments(p):
    """Returns list of assignments submitted to teacher"""
    teacher_assignments = Assignment.get_assignments_by_submitted_student(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Grades an submitted assignment"""
    assignment_grade_payload = AssignmentGradeSchema().load(incoming_payload)

    assignment_grade = Assignment.grade_assignment(
        _id=assignment_grade_payload.id,
        grade=assignment_grade_payload.grade,
        principal=p
    )
    db.session.commit()
    assignment_grade_dump = AssignmentSchema().dump(assignment_grade)
    return APIResponse.respond(data=assignment_grade_dump)