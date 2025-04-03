import asyncio
from typing import Any, Dict, List, Union
from dataclasses import asdict, dataclass
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
import tiktoken
from dotenv import load_dotenv
load_dotenv()
import os
os.environ['GOOGLE_API_KEY']=os.getenv('GOOGLE_API_KEY')
os.environ['TAVILY_API_KEY']=os.getenv('TAVILY_API_KEY')
# Define a class to handle structured search queries
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
import asyncio
from dataclasses import asdict, dataclass
from typing import List, Dict, Union, Any
import tiktoken

@dataclass
class SearchQuery:
    search_query: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

tavily_search = TavilySearchAPIWrapper()

async def run_search_queries(
    search_queries: List[Union[str, SearchQuery]],
    num_results: int = 5,
    include_raw_content: bool = False
) -> List[Dict]:
    search_tasks = []
    
    for query in search_queries:
        query_str = query.search_query if isinstance(query, SearchQuery) else str(query)
        try:
            search_tasks.append(
                tavily_search.raw_results_async(
                    query=query_str,
                    max_results=num_results,
                    search_depth='advanced',
                    include_answer=False,
                    include_raw_content=include_raw_content
                )
            )
        except Exception as e:
            print(f"Error creating search task for query '{query_str}': {e}")
            continue
    
    if not search_tasks:
        return []
    
    try:
        search_docs = await asyncio.gather(*search_tasks, return_exceptions=True)
        return [doc for doc in search_docs if not isinstance(doc, Exception)]
    except Exception as e:
        print(f"Error during search queries: {e}")
        return []

def format_search_query_results(
    search_response: Union[Dict[str, Any], List[Any]],
    max_tokens: int = 2000,
    include_raw_content: bool = False
) -> str:
    encoding = tiktoken.encoding_for_model("gpt-4")
    sources_list = []

    if isinstance(search_response, dict):
        sources_list.extend(search_response.get('results', [search_response]))
    elif isinstance(search_response, list):
        for response in search_response:
            if isinstance(response, dict):
                sources_list.extend(response.get('results', [response]))
            elif isinstance(response, list):
                sources_list.extend(response)

    if not sources_list:
        return "No search results found."

    unique_sources = {source['url']: source for source in sources_list if isinstance(source, dict) and 'url' in source}
    formatted_text = "Content from web search:\n\n"

    for source in unique_sources.values():
        formatted_text += f"Source {source.get('title', 'Untitled')}:\n===\n"
        formatted_text += f"URL: {source['url']}\n===\n"
        formatted_text += f"Most relevant content from source: {source.get('content', 'No content available')}\n===\n"

        if include_raw_content:
            raw_content = source.get("raw_content", "")
            if raw_content:
                tokens = encoding.encode(raw_content)
                truncated_content = encoding.decode(tokens[:max_tokens])
                formatted_text += f"Raw Content: {truncated_content}\n\n"

    return formatted_text.strip()