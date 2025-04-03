from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from SubNode.prompts import REPORT_SECTION_QUERY_GENERATOR_PROMPT
from SubNode.states import Queries,SectionState
from SubNode.SearchandFormat import *

from dotenv import load_dotenv
load_dotenv()
import os
os.environ['GOOGLE_API_KEY']=os.getenv('GEMINI_KEY')
os.environ['TAVILY_API_KEY']=os.getenv('TAVILY_API_KEY')

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3,
    max_tokens=None,
    timeout=None,
    max_retries=2,

)



def generate_queries(state: SectionState):
    """ Generate search queries for a specific report section """

    # Get state
    section = state["section"]
    print('--- Generating Search Queries for Section: '+ section.name +' ---')
    # Get configuration
    number_of_queries = 5
    # Generate queries
    structured_llm = llm.with_structured_output(Queries)
    # Format system instructions
    system_instructions = REPORT_SECTION_QUERY_GENERATOR_PROMPT.format(section_topic=section.description,                                                                       number_of_queries=number_of_queries)
    # Generate queries
    user_instruction = "Generate search queries on the provided topic."
    search_queries = structured_llm.invoke([SystemMessage(content=system_instructions),
                                     HumanMessage(content=user_instruction)])

    print('--- Generating Search Queries for Section: '+ section.name +' Completed ---')
    return {"search_queries": search_queries.queries}


async def search_web(state: SectionState):
    """ Search the web for each query, then return a list of raw sources and a formatted string of sources."""

    # Get state
    search_queries = state["search_queries"]
    print('--- Searching Web for Queries ---')
    # Web search
    query_list = [query.search_query for query in search_queries]
    search_docs = await run_search_queries(search_queries, num_results=5, include_raw_content=True)
    # Deduplicate and format sources
    search_context = format_search_query_results(search_docs, max_tokens=2500, include_raw_content=True)

    print('--- Searching Web for Queries Completed ---')
    return {"source_str": search_context}

