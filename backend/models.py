from pydantic import BaseModel
from typing import List

class JDRequest(BaseModel):
    jd_text: str

class JDResponse(BaseModel):
    role: str
    seniority: str
    required_skills: List[str]
    nice_to_have: List[str]
    complexity: str
