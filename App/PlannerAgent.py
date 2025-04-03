from IPython.display import display
from rich.console import Console
from rich.markdown import Markdown as RichMarkdown
import asyncio
# Updated call_planner_agent function in Node.py (or relevant module)
from IPython.display import display
from rich.console import Console
from rich.markdown import Markdown as RichMarkdown
import asyncio

async def call_planner_agent(agent, prompt, config={"recursion_limit": 50}, verbose=False):
    events = agent.astream(
        {'topic' : prompt},
        config,
        stream_mode="values",
    )

    markdown_content = ""
    async for event in events:
        for k, v in event.items():
            if verbose:
                if k != "__end__":
                    display(RichMarkdown(repr(k) + ' -> ' + repr(v)))
            
            if k == 'final_report':
                print('='*50)
                print('Final Report:')
                md = RichMarkdown(v)
                display(md)
                markdown_content = v  # Capture the markdown content
    
    return markdown_content  # Return the content instead of filename