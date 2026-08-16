from fastapi import APIRouter, status
from schemas.course_schema import CourseCreate, CourseUpdate
from services.course_service import create_course, get_course_by_id, get_all_courses, update_course, delete_course
from services.selection_services import assign_professor_to_course

router = APIRouter(prefix= "/courses", tags=["Courses"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def creat_course(course: CourseCreate):
    new_course = create_course(course)
    return new_course.to_dict()

@router.get("/") 
def list_courses():
    return [course.to_dict() for course in get_all_courses()]

@router.get("/{course_id}")
def show_course_by_id(course_id: int):
    course = get_course_by_id(course_id)
    return course.to_dict()

@router.put("/{course_id}")
def edit_course(course_id: int, course: CourseUpdate):
    updated_course = update_course(course_id, course)
    return updated_course.to_dict()

@router.delete("/{course_id}", status_code=status.HTTP_200_OK)
def remove_course(course_id: int):
    delete_course(course_id)
    return {"message": "درس با موفقیت حذف شد" }

@router.post("/{course_id}/professors/{professor_id}")
def assign_professor(course_id:int,professor_id:int):
    course = assign_professor_to_course(course_id,professor_id)
    return{"message":"درس با موفقیت برای استاد انتخاب شد","course":course.to_dict()}