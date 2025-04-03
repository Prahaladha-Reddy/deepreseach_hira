from langgraph.graph import StateGraph, START, END
from SubNode.states import SectionState,SectionOutputState

from SubNode.WriteSection import write_section
from SubNode.Search4Section import generate_queries,search_web

def build_section_graph():
    """Creates and returns the section builder subgraph."""
    section_builder = StateGraph(SectionState, output=SectionOutputState)
    
    section_builder.add_node("generate_queries", generate_queries)
    section_builder.add_node("search_web", search_web)
    section_builder.add_node("write_section", write_section)
    
    section_builder.add_edge(START, "generate_queries")
    section_builder.add_edge("generate_queries", "search_web")
    section_builder.add_edge("search_web", "write_section")
    section_builder.add_edge("write_section", END)

    return section_builder.compile()

