"""Step 5: an agentic RAG helpdesk in LangGraph - tools + loop + memory."""
import ast
import operator

from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from lc_config import get_model, get_vectorstore

COURSE_FEES = {"CS101": 12000, "AI202": 18000, "DS303": 15000}   # same data as Day 1
store = get_vectorstore()





@tool
def search_handbook(query: str) -> str:
    """Search the college handbook and return relevant passages."""
    MAX_DISTANCE = 0.3

    results = store.similarity_search_with_score(query, k=3)

    relevant_docs = [
        (doc, score)
        for doc, score in results
        if score <= MAX_DISTANCE
    ]

    if not relevant_docs:
        return "NO_MATCH: this is not covered in the college handbook."

    return "\n\n".join(
        f"[{doc.metadata['source']}] {doc.page_content}"
        for doc, score in relevant_docs
    )



@tool
def get_course_fee(course_code: str) -> str:
    """Return the fee in rupees for a course code such as CS101, AI202 or DS303."""
    fee = COURSE_FEES.get(course_code.strip().upper())
    return f"{course_code.upper()} fee is Rs. {fee}" if fee else f"Unknown course code {course_code}"


OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


@tool
def calculator(expression: str) -> str:
    """Evaluate simple arithmetic such as '18000 + 15000' or '100 * 12'."""
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.left), ev(n.right))
        raise ValueError("only + - * / on numbers")
    try:
        return str(ev(ast.parse(expression, mode="eval").body))
    except Exception as e:                       # tell the model, don't crash the graph
        return f"Error: {e}"


@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check if a student with this attendance percentage (0-100) may write the end-semester exam."""
    if attendance_percent < 0 or attendance_percent > 100:
        return "ERROR: Attendance percentage must be between 0 and 100."

    if attendance_percent >= 75:
        return "ELIGIBLE: You may write the end-semester exam."

    if attendance_percent >= 65:
        return "CONDONATION: You need condonation to write the exam. Fee: Rs. 500 per course."

    return "NOT ELIGIBLE: Attendance below 65% does not meet the minimum requirement."

tools = [
    search_handbook,
    get_course_fee,
    calculator,
    check_exam_eligibility,
]
model = get_model().bind_tools(tools)
SYSTEM = (
    "You are the Greenfield College helpdesk. "
    "Use search_handbook for rules and policies, "
    "get_course_fee for course fees, and calculator for arithmetic. "
    "Answer briefly and name the source file. "
    "If the tools do not provide the answer, say you don't know. "
    "For exam eligibility based on attendance, always use "
    "check_exam_eligibility and do not guess the result. "
    "If search_handbook returns a result beginning with NO_MATCH:, "
    "say the answer is not covered in the college handbook. "
    "For a question involving multiple fees, complete all required tool calls "
    "before answering. Call get_course_fee separately for each course. "
    "For the maximum late fee, use search_handbook to retrieve fee_policy.md. "
    "Extract the maximum late fee stated in that policy and use calculator "
    "to add the course fees and maximum late fee. "
    "Do not give a blank answer. If a required tool result is missing, "
    "call the required tool again before answering. "
    "For a follow-up asking about a different number of late days, "
    "keep the course fees from the previous question, calculate the new "
    "late fee using the daily rate and number of days, and use calculator "
    "to calculate the new total. "
    "Keep all questions in the same conversation thread when requested."
)

def agent(state: MessagesState):
    """The LLM node: read the conversation, either answer or ask for a tool."""
    reply = model.invoke([("system", SYSTEM)] + state["messages"])
    return {"messages": [reply]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))          # runs every tool call in the last message
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)   # tool calls? -> "tools", else -> END
builder.add_edge("tools", "agent")                  # the LOOP back to the LLM
graph = builder.compile(checkpointer=InMemorySaver())  # checkpointer = memory per thread


def ask(question, thread_id):
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 10}
    print(f"\n[{thread_id}] USER: {question}")
    for step in graph.stream({"messages": [("user", question)]}, config, stream_mode="updates"):
        for node, update in step.items():
            for msg in update["messages"]:
                if getattr(msg, "tool_calls", None):
                    for c in msg.tool_calls:
                        print(f"   {node:6} -> call {c['name']}({c['args']})")
                elif node == "tools":
                    print(f"   {node:6} -> {msg.name} returned {msg.content[:55]!r}...")
                else:
                    print(f"   {node:6} -> ANSWER: {msg.content}")


if __name__ == "__main__":
    print(graph.get_graph().draw_mermaid())

    ask(
        "What CGPA do I need to be eligible for placements?",
        "task-run"
    )

    ask(
        "My attendance is 70%. Can I write the exam?",
        "task-run"
    )

    ask(
        "What is the total of the CS101 fee, the AI202 fee and the maximum late fee?",
        "task-run"
    )

    ask(
        "And if I pay only 5 days late instead?",
        "task-run"
    )

    ask(
        "What is the capital of France?",
        "task-run"
    )

    saved = graph.get_state(
        {"configurable": {"thread_id": "task-run"}}
    ).values["messages"]

    print(f"\nThread task-run has {len(saved)} messages saved in memory")
