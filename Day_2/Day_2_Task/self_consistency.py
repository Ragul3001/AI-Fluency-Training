"""Day 2, Part C: run the same CoT prompt several times and take the majority answer."""
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'Day_1')
    )
)

from config import client, MODEL, banner

from collections import Counter
from config import client, MODEL, banner
from cot_compare import COT_PROMPT, QUESTIONS

RUNS = 5
TEMPERATURE = 0      # deliberately NOT 0, so each run can differ



import re

def final_answer(text):
    """Extract the answer after the Final Answer label."""
    match = re.search(
        r"final answer\s*:\s*([^\n]+)",
        text,
        flags=re.IGNORECASE
    )

    if match:
        answer_text = match.group(1)
    else:
        # Fallback: use the last non-empty line
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        answer_text = lines[-1] if lines else ""

    numbers = re.findall(r"\d[\d,]*(?:\.\d+)?", answer_text.replace(",", ""))
    if not numbers:
        return "No numerical answer found"

    return f"{float(numbers[-1]):.2f}"


def run_many(question, runs=RUNS, temperature=TEMPERATURE):
    answers = []
    for attempt in range(1, runs + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": COT_PROMPT},
                      {"role": "user", "content": question}],
            temperature=temperature,
        )
        answer = final_answer(response.choices[0].message.content)
        print(f"   run {attempt}: {answer}")
        answers.append(answer)
    return answers

if __name__ == "__main__":
    banner("SELF-CONSISTENCY")
    question = QUESTIONS[0]
    print("QUESTION:", question, "\n")
    answers = run_many(question)
    winner, count = Counter(answers).most_common(1)[0]
    print(f"\nMajority answer ({count} of {len(answers)} runs): {winner}")