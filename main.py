from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.graph import app_graph
from langchain_core.messages import HumanMessage
from servers.db import init_db

app = FastAPI(title="AI Agent with MCP")


class QueryRequest(BaseModel):
    query: str


@app.on_event("startup")
async def startup():
    await init_db()


@app.post("/api/v1/agent/query")
async def query_agent(request: QueryRequest):
    try:
        inputs = {"messages": [HumanMessage(content=request.query)]}
        final_state = await app_graph.ainvoke(inputs)

        last_message = final_state["messages"][-1]
        return {
            "query": request.query,
            "response": last_message.content,
            "history": [m.content for m in final_state["messages"]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
