from pydantic import BaseModel , Field
 
class ProfessorCreate(BaseModel):
    first_name : str = Field(...,min_length=2,max_length=50,examples=["Reza"])
    last_name : str = Field(...,min_length=2,max_length=50,examples=["Karimi"])
    personnel_code : str = Field(...,min_length=3,max_length=20,examples=["140158"])
    department : str = Field(...,min_length=2,max_length=80,examples=["Computer"])
    
class ProfessorUpdate(BaseModel):
    first_name : str| None = Field(default=None,min_length=2,max_length=50)
    last_name : str| None = Field(default=None,min_length=2,max_length=80)
    personnel_code : str| None = Field(default=None,min_length=3,max_length=20)
    department : str| None = Field(default=None,min_length=2,max_length=80)