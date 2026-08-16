from exceptions.custom_exceptions import StudentAlreadyExist
from exceptions.custom_exceptions import StudentDoesNotExist
from exceptions.custom_exceptions import ProfessorAlreadyAsignedException
class Courses:
    def __init__(self,id,code,unit,title,capacity):
        self.id = id
        self.code = code
        self.title = title
        self.capacity = capacity
        self.unit = unit
        self.professor = None
        self.students = []
        
    def full_capacity(self):
        return len(self.students) >= self.capacity
    
    def add_student(self,student):
        if student in self.students:
            raise StudentAlreadyExist("این دانشجو قبلا اضافه شده.")
        else :
            self.students.append(student)
            
    def remove_student(self,student):
        if student not in self.students:
            raise StudentDoesNotExist("دانشجو قبلا حذف شده.")
        else :
            self.students.remove(student)
    
    def assign_professor(self, professor):
        if self.professor is not None:
            if self.professor.id == professor.id:
                raise ProfessorAlreadyAsignedException(
                    "این استاد قبلا به این درس اختصاص داده شده."
                )
            raise ProfessorAlreadyAsignedException(
                "این درس قبلا یک استاد دارد."
            )

        self.professor = professor
        professor.assign_course(self)
        
    def to_dict(self) ->dict:
        return{
           "id": self.id,
            "title": self.title,
            "code": self.code,
            "unit": self.unit,
            "capacity": self.capacity,
            "remaining capacity": self.capacity-len(self.students),
            "professor":None if self.professor is None else {
                "id": self.professor.id,
                "first_name": self.professor.first_name,
                "last_name": self.professor.last_name,
                "personnel_code": self.professor.personnel_code
            },
            "students":[
                {
                    "id": student.id,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "student_number": student.student_number,
                }
                for student in self.students
            ],
        }