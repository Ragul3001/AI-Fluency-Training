# Day 3 Task: From Prompt to Action
## Understanding LLMs, Tools, and Agents

### 1. Scenario: College Fee Assistant

For this task, I created a college fee assistant scenario. The assistant answers general questions about AI agents and helps calculate college course fees and scholarship amounts.

The example uses three questions:

1. What is an AI agent?
2. What is the total fee for CS101 (₹12,000) and AI202 (₹18,000) after a 10% scholarship?
3. What is the fee difference between DS303 (₹15,000) and CS101 (₹12,000)?

I implemented a calculator tool in `my_tools.py`, a plain LLM script in `no_tool.py`, and a tool-enabled script in `with_tool.py`. Both scripts use the Groq API with the configured model.

### 2. What Is a Large Language Model?

A Large Language Model (LLM) is an AI model trained on large amounts of text to understand and generate language. It can answer general questions, explain concepts, summarize information, and help with reasoning.

In my scenario, the LLM answered “What is an AI agent?” without using an external tool. It explained the concept and provided examples. It also answered both fee calculation questions correctly in my test.

However, an LLM generating a correct calculation does not mean it has independently verified the arithmetic using an external calculator. Its answer may depend on its reasoning and can sometimes contain mistakes. For calculations that require reliable verification, an external tool is useful.

### 3. What Is an AI Agent?

An AI agent is a system that uses an LLM to interpret a request, decide what action is appropriate, and use available tools when necessary. A plain LLM response is generated directly from the conversation, whereas a tool-enabled agent can request an external operation and use its result to prepare the final response.

In my implementation, the model answered the general AI-agent question directly. For the fee questions, it requested the calculator tool, received the arithmetic result, and then explained the answer. This demonstrates how tool access can extend an LLM beyond generating text alone.

### 4. What Is a Tool and a Tool Call?

A tool is an external function that performs a specific operation for the model. In this task, the calculator function evaluates a basic arithmetic expression and returns the result as text.

A tool call occurs when the model requests that function with particular arguments. For example, it requested the expression `(12000+18000)*0.9` to calculate the total fee after a 10% scholarship.

A tool schema describes the function's name, purpose, and parameters. The name identifies the function, the description explains when it should be used, and the parameters specify the input format. This information helps the model decide whether the tool is suitable and construct a valid request.

### 5. How a Tool Call Works

The tool-enabled calculation follows these steps:

1. The user asks for the total fee after a scholarship.
2. The question and the available calculator tool schema are sent to the LLM.
3. The LLM decides that the calculator is appropriate and requests the expression `(12000+18000)*0.9`.
4. The Python program reads the tool name and arguments.
5. The calculator evaluates the expression and returns `27000.0`.
6. The program sends the tool result back to the LLM.
7. The LLM generates a final answer explaining that the payable fee is ₹27,000.

For the general question about AI agents, the model did not request the calculator because it could answer directly. The tool-enabled script therefore did not execute a tool for that question.

### 6. Why Tools Should Return Text on Failure

A tool should handle expected errors and return a readable error message rather than allowing an ordinary failure to terminate the entire program. For example, the calculator returns a message beginning with `Calculator error:` if it cannot evaluate an expression.

This approach allows the application to report the problem, log it, or ask the model to try again. It makes the application more robust. However, the program must still check the returned result and avoid treating an error message as a successful calculation.

### 7. Comparison: Plain LLM vs. LLM With One Tool

| Basis | Plain LLM prompt | LLM with one tool |
|---|---|---|
| Source of answer | Generated from the model's response to the prompt | Can use the model's response together with an external function result |
| Fetch or compute outside its own memory | Cannot directly execute the calculator function when no tool is provided | Can request an external calculation through the available tool |
| Reliability on numeric questions | Can calculate correctly, but arithmetic is not externally verified | Calculator result provides an explicit arithmetic result |
| Transparency | Shows the generated explanation, but not an external calculation trace | Can show the tool name, arguments, and result |
| Speed and cost | Usually needs one model request | A tool-enabled calculation may require a tool-selection request and another model request |

### 8. Observations From My Runs

#### Question 1: What is an AI agent?

The plain LLM gave a detailed explanation of AI agents, including their characteristics, types, and examples. In the tool-enabled run, the model answered the same question directly and displayed `No tool call`.

This was appropriate because the question was conceptual and did not require arithmetic. Providing a calculator did not mean that the calculator had to be used for every question.

#### Question 2: Total fee after a 10% scholarship

The plain LLM calculated the subtotal as ₹30,000, the scholarship as ₹3,000, and the payable fee as ₹27,000.

In the tool-enabled run, the model called `calculator` with `(12000+18000)*0.9`. The calculator returned `27000.0`, and the model used that result to explain the calculation.

Both answers were correct in this test. The main difference was that the tool-enabled run included an explicit calculator result.

#### Question 3: Difference between DS303 and CS101

The plain LLM answered that the fee difference was ₹3,000. In the tool-enabled run, the calculator evaluated `15000 - 12000` and returned `3000`. The final response correctly stated that DS303 costs ₹3,000 more than CS101.

Again, both answers were correct. The external calculator provided a verifiable arithmetic result for the tool-enabled answer.

### 9. Suitability and Conclusion

For general explanations, such as defining an AI agent, a plain LLM prompt was sufficient in my scenario. For arithmetic tasks, the model also answered correctly without a tool in my observed runs. However, the calculator made the arithmetic operation explicit and allowed the program to pass the computed result back to the model.

This experiment demonstrates that tool access does not guarantee that the model will always make the correct tool choice, but a well-designed tool can improve the reliability and transparency of operations that require external computation. The program should also validate tool arguments and handle errors appropriately.

More generally, a plain LLM is often suitable for explanations, brainstorming, rewriting, and other language tasks that do not require external data or exact computation. Tools are valuable when a task requires calculations, current information, database access, file reading, or an operation that the model cannot independently execute. The choice depends on the task's accuracy requirements, the available tools, and the cost and latency of additional calls.