from typing import List

from fastapi import APIRouter, Path
from pydantic import BaseModel

section_router = APIRouter(
    tags=["Section Routes"],
)

sections = []


class Section(BaseModel):
    name: str
    strength: bool


@section_router.get("/sections", response_model=List[Section])
def get_all_sections():
    return sections


@section_router.get("/section/{name}", response_model=List[Section])
def get_section_by_name(section_id: int = Path(description="The name of the section to fetch", gt=0)):
    return sections[section_id]


@section_router.post("/sections")
def add_section(section: Section):
    return sections.append(section)
