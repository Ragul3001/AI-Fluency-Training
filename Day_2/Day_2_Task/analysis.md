# Day 2 Task: Reasoning and Acting — Direct Prompting, Chain-of-Thought, and ReAct

## 1. Scenario and Objective

This project compares three approaches to solving questions about college course fees: direct prompting, Chain-of-Thought (CoT), and a ReAct agent. The scenario includes arithmetic, logical reasoning, scholarship calculations, and a question that requires looking up course fees using tools. The course fees used in the experiment are CS101 at ₹12,000, AI202 at ₹18,000, and DS303 at ₹15,000.

The objective is to compare how the approaches answer questions, whether they use tools, how clearly their processes can be observed, and how consistently they produce answers.

## 2. Direct Prompting

Direct prompting asks the language model to answer a question immediately, without requesting visible reasoning steps. It relies on the model's learned knowledge and its interpretation of the prompt. In the comparison experiment, direct prompting correctly answered the course-instalment question with ₹9,562.50, the computer-sittings question with 90, and the height-ordering question with Ravi as tallest and Priya as shortest.

Direct prompting is fast and simple for questions with sufficient information. However, it does not independently look up external data or execute a calculator tool. The user receives the answer without a visible calculation, making it harder to inspect how the result was obtained.

## 3. Chain-of-Thought Prompting

Chain-of-Thought prompting asks the model to provide intermediate steps before its final answer. For the course-instalment problem, the model added the three fees to get ₹45,000, calculated the 15% scholarship as ₹6,750, obtained a payable amount of ₹38,250, and divided it into four instalments of ₹9,562.50.

In the experiment, CoT also correctly answered the computer-sittings and height-ordering questions. Its visible steps made the calculations and comparisons easier to check. However, CoT alone does not retrieve missing external information or independently execute tools. A detailed explanation can still contain mistakes, so its calculations should be verified when accuracy matters.

## 4. ReAct Agent

ReAct combines reasoning with actions and observations. The model decides what information or calculation it needs, calls a tool, receives the tool's result, and then continues toward a final answer.

The implemented agent has two tools: `get_course_fee`, which retrieves a course fee from the configured fee data, and `calculator`, which evaluates arithmetic expressions. The tool descriptions and parameter schemas tell the model which tools are available and how to call them.

In the scholarship comparison, the agent retrieved the fees of CS101, AI202, and DS303. It calculated the cost of CS101 and AI202 after a 10% scholarship as ₹27,000. It calculated the cost of all three courses after a 25% scholarship as ₹33,750. The first option was cheaper by ₹6,750.

The tool calls and returned values appeared in the terminal, making the process easier to audit. ReAct is useful when a question requires data retrieval or external computation, although it can be slower because it may require multiple model and tool calls. Its reliability also depends on the quality of the tools and the agent's decisions.

## 5. Comparison Table

| Basis | Direct Prompting | Chain-of-Thought | ReAct Agent |
|---|---|---|---|
| Reasoning depth | Direct answer with no visible steps | Shows intermediate reasoning steps | Reasons through actions and observations |
| Tool usage | No tool calls | No tool calls in this implementation | Calls course-fee and calculator tools when needed |
| Reliability on multi-step questions | Can be correct but intermediate calculations are not visible | Steps make calculations easier to inspect, but mistakes remain possible | Tool results can improve verification when the right tools are used |
| Transparency | Low; final answer only | Higher; steps are shown | Tool calls and observations are visible |
| Speed / cost | Usually lowest | May use more output tokens than direct prompting | May require multiple model and tool calls |
| Consistency across repeated runs | Depends on model and settings | Depends on model, prompt, and temperature | Depends on model, tools, and action choices |

## 6. Self-Consistency Observation

The instalment question was run five times using Chain-of-Thought prompting at temperature 0.8. All five responses gave the same numerical answer: ₹9,562.50 per instalment. Their original formatting differed, so the answer-extraction function was adjusted to normalize the numerical result before counting the majority answer. After normalization, the majority result was 5 out of 5.

The same question was also run five times at temperature 0, and all five runs returned ₹9,562.50. This observed result was consistent at both tested settings. However, five runs are a small sample, and temperature 0 does not guarantee identical outputs in every environment. The experiment demonstrates that formatting can vary even when the numerical answer remains the same.

## 7. Suitability Analysis

For simple questions with enough information already provided, direct prompting is suitable because it is quick and concise. CoT is useful for arithmetic and logic problems when showing the intermediate steps helps a person inspect the answer. In this experiment, both direct prompting and CoT correctly answered all three comparison questions, so the observed results do not show that CoT was more accurate.

For the scholarship comparison involving course fees, ReAct is the most suitable of the three approaches because it can retrieve the configured fee data and perform calculations using tools. The experiment displayed the tool calls, the calculated totals, and the final difference. This provides a clearer way to verify the result than relying only on an unassisted response.

## 8. Conclusion

Direct prompting is appropriate for straightforward questions where a concise answer is enough. Chain-of-Thought prompting can help with multi-step arithmetic or logical problems when intermediate steps are useful for checking the result. ReAct is more appropriate when a task needs external data, tool execution, or repeated interactions with tools before a final answer can be produced.

No approach is automatically correct in every situation. The best choice depends on the task, the need for external information, the value of visible evidence, and the cost of additional steps. In this project, the experiments showed that direct prompting and CoT both answered the three reasoning questions correctly, while ReAct demonstrated course-fee retrieval and tool-based scholarship calculations.
