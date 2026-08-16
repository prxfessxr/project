from models.person import Person
from exceptions.custom_exceptions import CourseAlreadySelectedException
from exceptions.custom_exceptions import CourseDoesNotExistInSelectedCourses,CourseSelectionException

class Student(Person):
    def __init__(self, id, first_name, last_name,student_number,major,selected_courses = None):
        super().__init__(id, first_name, last_name)
        self.student_number = student_number
        self.major = major
        self.selected_courses = selected_courses if selected_courses is not None else []
        
    def select_course(self, course):
        if course in self.selected_courses:
            raise CourseAlreadySelectedException("درس قبلا توسط دانشجو انتخاب شده!")
        if course.full_capacity():
            raise CourseSelectionException("ظرفیت این درس تکمیل است.")
        self.selected_courses.append(course)
        if self not in course.students:
            course.students.append(self)
    
    def drop_course(self, course):
        if course not in self.selected_courses:
            raise CourseDoesNotExistInSelectedCourses("این مورد در لیست دروس انتخابی وجود ندارد!")
        self.selected_courses.remove(course)
        if self in course.students:
            course.students.remove(self)
            
    def get_courses(self) -> list :
        return self.selected_courses
    
    def to_dict(self):
        data = super().to_dict()
        data["student_number"] = self.student_number
        data["major"] = self.major
        data["selected_courses"] = [{
            "id":course.id,
            "title":course.title,
            "code":course.code,
            "unit":course.unit,
            }for course in self.selected_courses]
        return data