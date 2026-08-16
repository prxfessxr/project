from pydantic import BaseModel , Field
 
class StudentCreate(BaseModel):
    first_name : str = Field(...,min_length=2,max_length=50,examples=["Ali"])
    last_name : str = Field(...,min_length=2,max_length=50,examples=["Ahmadi"])
    student_number : str = Field(...,min_length=7,max_length=11,examples=["4041423"])
    major : str = Field(...,min_length=2,max_length=80,examples=["Computer Engineering"])
    
class StudentUpdate(BaseModel):
    first_name : str| None = Field(default=None,min_length=2,max_length=50)
    last_name : str | None= Field(default=None,min_length=2,max_length=50)
    student_number : str| None = Field(default=None,min_length=7,max_length=11)
    major : str | None= Field(default=None,min_length=2,max_length=80)