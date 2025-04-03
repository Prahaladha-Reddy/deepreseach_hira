from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from App.PlannerAgent import call_planner_agent
from Node import final_graph_builder

app = FastAPI()
reporter_agent = final_graph_builder()

class RequestData(BaseModel):
    topic: str

@app.post("/generate_report/")
async def generate_report(data: RequestData):
    """API endpoint to generate a report."""
    result = await call_planner_agent(agent=reporter_agent, prompt=data.topic)
    return {"report": result}  # Now contains the markdown content

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)