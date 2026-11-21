from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from mini_agent import messages
from mini_agent.nodes import (
    ERROR_GUIDE_NODE,
    LLM_NODE,
    SEARCH_NODE,
    AgentState,
    LLMNode,
    RagSearchNode,
    error_guide,
    llm_error_handler,
    search_error_handler,
)
from mini_agent.search import SEARCH_TOOL_NAME, DocumentSearch

# 도구 이름 → 그 도구를 실행하는 노드. 도구를 추가하면 노드를 만들고 여기에 한 줄을 더한다.
TOOL_NODES = {SEARCH_TOOL_NAME: SEARCH_NODE}


def build_graph(model: BaseChatModel, search: DocumentSearch) -> CompiledStateGraph:
    """시연 그래프. LLM이 검색을 요청하면 검색 노드를 거쳐 다시 LLM으로 돌아온다."""
    builder = StateGraph(AgentState)  # ty: ignore[invalid-argument-type]
    # 오류 처리기의 (state, NodeError) 모양이 LangGraph의 타입 정의에 빠져 있어 ty가 거부한다.
    builder.add_node(
        LLM_NODE,
        LLMNode(model),
        error_handler=llm_error_handler,  # ty: ignore[invalid-argument-type]
    )
    builder.add_node(
        SEARCH_NODE,
        RagSearchNode(search),
        error_handler=search_error_handler,  # ty: ignore[invalid-argument-type]
    )
    builder.add_node(ERROR_GUIDE_NODE, error_guide)

    builder.add_edge(START, LLM_NODE)
    builder.add_conditional_edges(
        LLM_NODE, route_after_llm, [*TOOL_NODES.values(), END]
    )
    builder.add_edge(SEARCH_NODE, LLM_NODE)
    builder.add_edge(ERROR_GUIDE_NODE, END)
    return builder.compile()


def route_after_llm(state: AgentState) -> str:
    """LLM이 도구를 요청했으면 그 도구의 노드로, 글로 답했으면 끝으로 보낸다.

    한 응답의 도구 요청은 모두 같은 도구라고 보고 첫 요청의 도구로 노드를 정한다.
    서로 다른 도구를 한 번에 요청하면 병렬 실행이 필요해 이 그래프의 범위 밖이다.
    """
    last = state["messages"][-1]
    if not isinstance(last, AIMessage) or not last.tool_calls:
        return END
    tool_name = last.tool_calls[0]["name"]
    if tool_name not in TOOL_NODES:
        raise ValueError(messages.no_node_for_tool(tool_name))
    return TOOL_NODES[tool_name]
