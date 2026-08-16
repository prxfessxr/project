from models.person import Person
from exceptions.custom_exceptions import ProfessorAlreadyAsignedException
class Professor(Person):
    def __init__(self, id, first_name, last_name,personnel_code,department):
        super().__init__(id, first_name, last_name)
        self.personnel_code = personnel_code
        self.department = department
        self.courses = []
    
    def assign_course(self,course):
        if course in self.courses:
            raise ProfessorAlreadyAsignedException("این درس قبلا به استاد اختصاص داده شده!")
        else :
            self.courses.append(course)
    def get_courses(self) -> list:
        return self.courses
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["personnel"] = self.personnel_code
        data["department"] = self.department
        data["courses"] = [{
            "id":course.id,
            "title":course.title,
            "code":course.code,
            "unit":course.unit,
            }for course in self.courses]
        return data
    