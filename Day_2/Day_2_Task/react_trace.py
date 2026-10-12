"""Day 2 Task: ReAct agent with visible tool actions and observations."""

from agent import agent

QUESTION = (
    "Which option costs less: CS101 and AI202 together with a 10% scholarship, "
    "or CS101, AI202 and DS303 together with a 25% scholarship? "
    "Use the course-fee tools and calculator to determine the difference."
)

print("QUESTION:", QUESTION, "\n")
print("--- ReAct: Thought -> Action -> Observation ---")
answer = agent(QUESTION, max_steps=15, verbose=True)
print("\nFINAL ANSWER:", answer)
