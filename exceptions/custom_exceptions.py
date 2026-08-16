class CourseSelectionException(Exception):
    "Base Exception for course selection system"

class ProfessorAlreadyAsignedException(CourseSelectionException):
    pass

class CourseAlreadySelectedException(CourseSelectionException):
    pass

class CourseDoesNotExistInSelectedCourses(CourseSelectionException):
    pass

class StudentAlreadyExist(CourseSelectionException):
    pass

class StudentDoesNotExist(CourseSelectionException):
    pass

class InvalidDataException(CourseSelectionException):
    pass

class StudentNotFoundException(CourseSelectionException):
    pass

class ProfessorNotFoundException(CourseSelectionException):
    pass

class CourseNotFoundException(CourseSelectionException):
    pass