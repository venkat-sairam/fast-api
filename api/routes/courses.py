from typing import List

from fastapi import APIRouter, Path
from pydantic import BaseModel

course_router = APIRouter(
    tags=["course Routes"],
)

courses = []


class Course(BaseModel):
    name: str
    strength: bool


@course_router.get("/courses", response_model=List[Course])
def get_all_courses():
    return courses


@course_router.get("/course/{name}", response_model=List[Course])
def get_course_by_name(course_id: int = Path(description="The name of the course to fetch", gt=0)):
    return courses[course_id]


@course_router.post("/courses", response_model=dict)
def add_course(course: Course):
    courses.append(course)
    return {"message": "Course added successfully!"}
