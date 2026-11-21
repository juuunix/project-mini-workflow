from collections.abc import Callable, Mapping
from datetime import date

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import RetryPolicy

from mini_agent import messages
from mini_agent.nodes import (
    DATE_NODE,
    DATE_TOOL_NAME,
    ERROR_GUIDE_NODE,
    LLM_NODE,
    SEARCH_NODE,
    AgentState,
    DateNode,
    LLMNode,
    RagSearchNode,
    ToolRunner,
    error_guide,
    llm_error_handler,
    tool_calls_of,
    tool_error_handler,
)
from mini_agent.search import SEARCH_TOOL_NAME, DocumentSearch

# LLM 호출의 시간 초과와 연결 오류는 일시적이라고 보고, 1초부터 2배씩 기다리며 3번까지 시도한다.
# LangGraph의 기본 설정은 TimeoutError를 재시도하지 않아 재시도할 예외를 직접 지정한다.
LLM_RETRY_POLICY = RetryPolicy(
    max_attempts=3,
    initial_interval=1.0,
    backoff_factor=2.0,
    jitter=False,
    retry_on=(TimeoutError, ConnectionError),
)


def build_graph(
    model: BaseChatModel,
    search: DocumentSearch,
    llm_retry: RetryPolicy = LLM_RETRY_POLICY,
    today: Callable[[], date] = date.today,
) -> CompiledStateGraph:
    """시연 그래프. LLM이 도구를 요청하면 그 도구의 노드를 거쳐 다시 LLM으로 돌아온다."""
    # 도구 이름 → (노드 이름, 노드). 도구를 추가하면 여기에 한 줄을 더한다.
    # 노드 등록, LLM으로 돌아가는 연결, 조건부 연결의 갈 곳은 이 표에서 만든다.
    # 가짜 LLM을 쓰는 동안에는 그 도구를 언제 요청할지 FakeLLM에도 규칙을 더해야 한다.
    tools: dict[str, tuple[str, ToolRunner]] = {
        SEARCH_TOOL_NAME: (SEARCH_NODE, RagSearchNode(search)),
        DATE_TOOL_NAME: (DATE_NODE, DateNode(today)),
    }
    routes = {tool: node_name for tool, (node_name, _) in tools.items()}

    builder = StateGraph(AgentState)  # ty: ignore[invalid-argument-type]
    # 오류 처리기의 (state, NodeError) 모양이 LangGraph의 타입 정의에 빠져 있어 ty가 거부한다.
    builder.add_node(
        LLM_NODE,
        LLMNode(model),
        retry_policy=llm_retry,
        error_handler=llm_error_handler,  # ty: ignore[invalid-argument-type]
    )
    for node_name, node in tools.values():
        builder.add_node(
            node_name,
            node,
            error_handler=tool_error_handler,  # ty: ignore[invalid-argument-type]
        )
        builder.add_edge(node_name, LLM_NODE)
    builder.add_node(ERROR_GUIDE_NODE, error_guide)

    builder.add_edge(START, LLM_NODE)
    builder.add_conditional_edges(
        LLM_NODE,
        lambda state: route_after_llm(state, routes),
        [*routes.values(), END],
    )
    builder.add_edge(ERROR_GUIDE_NODE, END)
    return builder.compile()


def route_after_llm(state: AgentState, routes: Mapping[str, str]) -> str:
    """LLM이 도구를 요청했으면 그 도구의 노드로, 글로 답했으면 끝으로 보낸다.

    한 응답의 도구 요청은 모두 같은 도구라고 보고 첫 요청의 도구로 노드를 정한다.
    서로 다른 도구를 한 번에 요청하면 병렬 실행이 필요해 이 그래프의 범위 밖이다.
    """
    calls = tool_calls_of(state)
    if not calls:
        return END
    tool_name = calls[0]["name"]
    if tool_name not in routes:
        raise ValueError(messages.no_node_for_tool(tool_name))
    return routes[tool_name]
