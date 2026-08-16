from pydantic import BaseModel , Field
 
class CourseCreate(BaseModel):
    title : str = Field(...,min_length=2,max_length=100,examples=["Advanced python programming"])
    code : str = Field(...,min_length=2,max_length=20,examples=["CS301"])
    capacity : int = Field(...,ge=1,le=200,examples=["30"])
    unit : int = Field(...,ge=1,le=5,examples=["3"])
    
class CourseUpdate(BaseModel):
    title : str | None= Field(default=None,min_length=2,max_length=50)
    code : str | None= Field(default=None,min_length=2,max_length=20)
    capacity: int | None = Field(default=None, ge=1, le=200)
    unit: int | None = Field(default=None, ge=1, le=5)