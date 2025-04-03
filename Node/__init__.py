from SubNode.states import ReportState , ReportStateInput,ReportStateOutput 
from langgraph.graph import StateGraph , START,END
from SubNode import build_section_graph
from Node.parallelizeFinalSectionWriting import parallelize_final_section_writing , compile_final_report
from Node.ParallelSectionWriting import parallelize_section_writing
from Node.SectionFormating import format_completed_sections
from Node.SectionWriting import write_final_sections
from SubNode.SectionPlanning import generate_report_plan

def final_graph_builder():
    # Create a new StateGraph instance each time
    builder = StateGraph(ReportState, input=ReportStateInput, output=ReportStateOutput)
    section_builder_subagent = build_section_graph()
    
    # Add nodes
    builder.add_node("generate_report_plan", generate_report_plan)
    builder.add_node("section_builder_with_web_search", section_builder_subagent)
    builder.add_node("format_completed_sections", format_completed_sections)
    builder.add_node("write_final_sections", write_final_sections)
    builder.add_node("compile_final_report", compile_final_report)
    
    # Add edges
    builder.add_edge(START, "generate_report_plan")
    builder.add_conditional_edges("generate_report_plan",
                                  parallelize_section_writing,
                                  ["section_builder_with_web_search"])
    builder.add_edge("section_builder_with_web_search", "format_completed_sections")
    builder.add_conditional_edges("format_completed_sections",
                                  parallelize_final_section_writing,
                                  ["write_final_sections"])
    builder.add_edge("write_final_sections", "compile_final_report")
    builder.add_edge("compile_final_report", END)
    
    return builder.compile()

  # view agent structure

