from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from SubNode.states import SectionState
from SubNode.prompts import SECTION_WRITER_PROMPT
from SubNode.SearchandFormat import *

from dotenv import load_dotenv
load_dotenv()
import os
os.environ['GOOGLE_API_KEY']=os.getenv('API_KEY')
os.environ['TAVILY_API_KEY']=os.getenv('TAVILY_API_KEY')

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,

)


def write_section(state: SectionState):
    """ Write a section of the report """

    # Get state
    section = state["section"]
    source_str = state["source_str"]
    print('--- Writing Section : '+ section.name +' ---')
    # Format system instructions
    system_instructions = SECTION_WRITER_PROMPT.format(section_title=section.name,                                                     section_topic=section.description,                                                       context=source_str)
    # Generate section
    user_instruction = "Generate a report section based on the provided sources."
    section_content = llm.invoke([SystemMessage(content=system_instructions),
                                  HumanMessage(content=user_instruction)])
    # Write content to the section object
    section.content = section_content.content

    print('--- Writing Section : '+ section.name +' Completed ---')
    # Write the updated section to completed sections
    return {"completed_sections": [section]}