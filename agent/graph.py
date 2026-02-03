from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from agent.mock_llm import RuleBasedMockLLM
from agent.tools import list_products, add_product, get_statistics, calculate_discount, formatter


class AgentState(TypedDict):
    messages: Sequence[BaseMessage]


tools = [list_products, add_product, get_statistics, calculate_discount, formatter]

model = RuleBasedMockLLM()


def call_model(state):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}


def should_continue(state):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tools"
    return END


workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app_graph = workflow.compile()
