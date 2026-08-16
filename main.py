from fastapi import FastAPI, Request,status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from exceptions.custom_exceptions import (
    CourseSelectionException,
    ProfessorAlreadyAsignedException,
    CourseAlreadySelectedException,
    CourseNotFoundException,
    CourseDoesNotExistInSelectedCourses,
    StudentAlreadyExist,
    StudentDoesNotExist,
    InvalidDataException,
    StudentNotFoundException,
    ProfessorNotFoundException)
from routers.students import router as student_router
from routers.professors import router as professor_router
from routers.courses import router as course_router
from data.storage import _save_all,load_all,students,professors,courses

app=FastAPI(title="Simple course selection site",
            description="به سایت انتخاب واحد من خوش آمدید.",
            version="1.0.0")

app.include_router(student_router)
app.include_router(professor_router)
app.include_router(course_router)

# Frontend assets 
FRONTEND_DIR = Path(__file__).parent / "frontend"
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

@app.on_event("startup")
def startup_load_data():
    load_all()
@app.on_event("shutdown")
def shutdown_save_data():
    _save_all()
    
@app.get("/", tags=["Welcome message"])
def welcome_message():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/debug/storage",tags=["Debug"])
def debug_storage_summary():
    return {
        "student_count": len(students),
        "professor_count": len(professors),
        "course_count": len(courses)
    }
    
@app.get("/debug/storage/all",tags=["Debug"])
def debug_storage_all():
    return {"students":[student.to_dict()for student in students.values() ],
            "professors": [professor.to_dict() for professor in professors.values()],
            "courses": [course.to_dict() for course in courses.values()]}
    
@app.exception_handler(ProfessorAlreadyAsignedException)
async def professor_already_asigned(request:Request,exc: ProfessorAlreadyAsignedException):
    return JSONResponse(
        status_code = status.HTTP_409_CONFLICT,
        content={"Error":"قبلا انجام شده.","message":str(exc)},
    )
    
@app.exception_handler(CourseAlreadySelectedException)
async def course_already_selected(request:Request,exc: CourseAlreadySelectedException):
    return JSONResponse(
        status_code = status.HTTP_409_CONFLICT,
        content={"Error":"قبلا انتخاب شده.","message":str(exc)},
    )
    
@app.exception_handler(CourseNotFoundException)
async def course_not_found(request: Request, exc: CourseNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"Error": "درس پیدا نشد","message": str(exc)}
    )
    
@app.exception_handler(CourseDoesNotExistInSelectedCourses)
async def course_does_not_exist_in_selected_courses(request:Request,exc: CourseDoesNotExistInSelectedCourses):
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content={"Error":"درس پیدا نشد !","message":str(exc)},
    )

@app.exception_handler(StudentAlreadyExist)
async def student_already_exist(request:Request,exc: StudentAlreadyExist):
    return JSONResponse(
        status_code = status.HTTP_409_CONFLICT,
        content={"Error":"دانشجو از قبل وجود دارد !","message":str(exc)},
    )
    
@app.exception_handler(StudentDoesNotExist)
async def student_does_not_exist(request:Request,exc: StudentDoesNotExist):
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content={"Error":"دانشجو وجود ندارد !","message":str(exc)},
    )
    
@app.exception_handler(InvalidDataException)
async def invalid_data(request:Request,exc: InvalidDataException):
    return JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content={"Error":"ورودی نامعتبر ","message":str(exc)},
    )
    
@app.exception_handler(StudentNotFoundException)
async def invalid_data(request:Request,exc: StudentNotFoundException):
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content={"Error":"دانشجو پیدا نشد","message":str(exc)},
    )
    
@app.exception_handler(ProfessorNotFoundException)
async def invalid_data(request:Request,exc: ProfessorNotFoundException):
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content={"Error":"استاد پیدا نشد","message":str(exc)},
    )
    
@app.exception_handler(CourseSelectionException)
async def invalid_data(request:Request,exc: CourseSelectionException):
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content={"Error":"CourseSelectionException","message":str(exc)},
    )
    