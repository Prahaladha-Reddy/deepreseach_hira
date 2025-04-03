from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import operator
from typing import Annotated, List, Optional, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import operator
from typing import Annotated, List

class Section(BaseModel):
    name: str = Field(description="Name for a particular section of the report.")
    description: str = Field(description="Brief overview of the main topics and concepts to be covered in this section.")
    research: bool = Field(description="Whether to perform web search for this section of the report.")
    content: str = Field(description="The content for this section.")

class Sections(BaseModel):
    sections: List[Section] = Field(description="All the Sections of the overall report.")

class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query for web search.")

class Queries(BaseModel):
    queries: List[SearchQuery] = Field(description="List of web search queries.")

class ReportStateInput(TypedDict):
    topic: str

class ReportStateOutput(TypedDict):
    final_report: str

class ReportState(TypedDict):
    topic: str
    sections: list[Section]
    completed_sections: Annotated[list, operator.add]
    report_sections_from_research: str
    final_report: str

class SectionState(TypedDict):
    section: Section
    search_queries: list[SearchQuery]
    source_str: str
    report_sections_from_research: str
    completed_sections: list[Section]

class SectionOutputState(TypedDict):
    completed_sections: list[Section]