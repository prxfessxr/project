from fastapi import APIRouter, status
from schemas.professor_schema import ProfessorCreate, ProfessorUpdate
from services.professor_service import create_professor, get_professor_by_id, get_all_professors, update_professor, delete_professor

router = APIRouter(prefix="/professors", tags=["Professors"])

@router.post("/", status_code=status.HTTP_201_CREATED) 
def creat_professor(professor: ProfessorCreate):
    new_professor = create_professor(professor)
    return new_professor.to_dict()

@router.get("/")
def list_professors():
    return [professor.to_dict() for professor in get_all_professors()]

@router.get("/{professor_id}")
def show_professor_by_id(professor_id: int):
    professor = get_professor_by_id(professor_id)
    return professor.to_dict()

@router.put("/{professor_id}")
def edit_professor(professor_id: int, professor: ProfessorUpdate):
    updated_professor = update_professor(professor_id, professor)
    return updated_professor.to_dict()

@router.delete("/{professor_id}", status_code=status.HTTP_200_OK)
def remove_professor(professor_id: int):
    delete_professor(professor_id)
    return {"message": "استاد با موفقیت حذف شد"}