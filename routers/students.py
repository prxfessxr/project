from fastapi import APIRouter, status
from schemas.student_schema import StudentCreate,StudentUpdate
from services.student_service import create_student , get_student_by_id, get_all_students,update_student,delete_student
from services.selection_services import select_course_for_student,drop_course_for_student,get_student_courses

router = APIRouter(prefix= "/students",tags=["students"])

@router.post("/",status_code=status.HTTP_201_CREATED)  
def creat_student(student:StudentCreate):
    new_student = create_student(student)
    return new_student.to_dict()

@router.get("/") 
def list_students():
    return[student.to_dict() for student in get_all_students()]

@router.get("/{student_id}") 
def show_student_by_id(student_id:int):
    student = get_student_by_id(student_id)
    return student.to_dict()

@router.put("/{student_id}")
def edit_student(student_id:int, student: StudentUpdate):
    updated_student = update_student(student_id,student)
    return updated_student.to_dict()

@router.delete("/{student_id}", status_code=status.HTTP_200_OK)
def remove_student(student_id: int):
    delete_student(student_id)
    return {"message": "دانشجو با موفقیت حذف شد"}

@router.get("/{student_id}/courses")
def check_student_courses(student_id:int):
    courses = get_student_courses(student_id)
    return [a_course.to_dict() for a_course in courses]

@router.post("/{student_id}/courses/{course_id}")
def select_course(student_id:int,course_id:int):
    student= select_course_for_student(student_id,course_id)
    return {"message":"درس با موفقیت برای دانشجو انتخاب شد ","student":student.to_dict()}


@router.delete("/{student_id}/courses/{course_id}")
def delete_course(student_id:int,course_id:int):
    student= drop_course_for_student(student_id,course_id)
    return {"message":"درس با موفقیت حذف شد ","student":student.to_dict()}