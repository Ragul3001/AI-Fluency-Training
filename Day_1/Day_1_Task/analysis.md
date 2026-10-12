# Comparing a Plain Chatbot, a Rule-Based Workflow, and an AI Agent

## 1. Introduction

Artificial intelligence systems can solve problems in different ways depending on their design and capabilities. A plain chatbot generates responses using a language model, a rule-based workflow follows predefined instructions, and an AI agent uses a language model with tools to perform tasks in multiple steps. In this project, I compared these three approaches using a college course-fee assistant scenario. The system answers questions about course fees, scholarship calculations, fee comparisons, and welcome messages for new AI students.

The course-fee information used in this project is stored locally in a Python configuration file. The course fees are CS101 at ₹12,000, AI202 at ₹18,000, and DS303 at ₹15,000. All three systems were tested with the same four questions to compare their capabilities and limitations.

## 2. Scenario and Private Data

The selected scenario is a college assistant that answers questions about course fees. Course-fee information is treated as private institutional data for this demonstration. The data is stored in the local `config.py` file and accessed by the rule-based workflow and AI agent.

The four test questions are:

1. What is the fee for AI202?
2. What is the total fee for CS101 and AI202 after a 10% scholarship?
3. Is DS303 more expensive than CS101, and by how much?
4. Write a two-line welcome message for new AI students.

These questions test data retrieval, arithmetic, comparison, and natural-language generation.

## 3. System 1: Plain Chatbot

The plain chatbot uses a language model to generate answers from the conversation. It does not use tools to retrieve the local course-fee data. Therefore, it cannot reliably answer questions about the actual fees stored in the configuration file.

During testing, the chatbot did not know the actual AI202 fee and provided general fee ranges instead. For the scholarship question, it asked for the course fees rather than calculating the correct total from the local data. For the DS303 comparison, it generated example fee amounts that did not match the stored course fees. However, it successfully generated a two-line welcome message for new AI students.

This demonstrates that a plain chatbot can communicate naturally and handle general text-generation tasks, but it may give incorrect or unsupported answers when it lacks access to the required data. It is suitable for general conversation, but it is not reliable for answering questions that require private institutional information.

## 4. System 2: Rule-Based Workflow

The rule-based workflow uses predefined Python rules without calling a language model. It identifies course codes in the user's question, retrieves the relevant fees from the configuration file, and applies predefined logic to calculate totals and scholarships.

During testing, it correctly returned the AI202 fee as ₹18,000. It also correctly calculated the total fee for CS101 and AI202 after a 10% scholarship as ₹27,000. However, it could not answer the question comparing DS303 with CS101 because no rule was implemented for that question. It also could not generate the requested welcome message because the workflow was designed to handle course-fee questions.

The rule-based workflow produces predictable results for the question types it supports. It can access the local course-fee data without using an LLM. Its main limitation is that it cannot easily handle questions that fall outside its predefined rules. Adding new question types requires additional programming.

## 5. System 3: AI Agent

The AI agent combines a language model, tools, and a loop. It uses the model to decide what action to take, calls tools when necessary, observes the returned results, and continues until it can provide a final answer or reaches its step limit.

This project uses two tools. The `get_course_fee` tool retrieves course fees from the local configuration data, while the `calculator` tool performs arithmetic expressions. The agent uses these tools to answer questions that require access to the course-fee data or calculations.

During testing, the agent successfully retrieved the AI202 fee and returned ₹18,000. For the scholarship question, it retrieved the fees for CS101 and AI202, then called the calculator with the expression `(12000+18000)*(1-0.10)`. The calculator returned 27000.0, and the agent correctly answered ₹27,000. For the DS303 comparison, it retrieved both fees and correctly reported that DS303 costs ₹3,000 more than CS101. It also generated the two-line welcome message without needing a tool.

These results demonstrate how an AI agent can combine natural-language understanding with tool use. Unlike the plain chatbot, it can access the local data through its tools. Unlike the rule-based workflow, it can select tools based on the question and respond to different types of requests. However, an agent's behavior depends on the language model, tool definitions, and error handling, so its tool calls and answers still need to be tested.

## 6. Comparison Table

| Comparison criterion | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| Flexibility | Flexible for natural-language conversation | Limited to predefined rules | Flexible and can choose tools |
| Decision-making | Generates answers from the conversation | Follows fixed conditions | Selects actions using the language model |
| Tool usage | No tools used in this project | Uses predefined Python logic | Uses tools selected by the model |
| Private-data access | No access to the local fee data in this implementation | Reads the local fee data | Reads the local fee data through tools |
| Multi-step task handling | Limited when external data or calculations are needed | Handles only programmed sequences | Can retrieve data, use tools, and continue through a loop |
| Automation | Generates conversational responses | Automates supported cases | Automates multiple supported tasks using tools |
| Reliability | May produce unsupported answers | Predictable for implemented rules | Can be effective, but model and tool-call errors are possible |

## 7. Which System Is Most Suitable?

The most suitable system depends on the requirements of the task.

A plain chatbot is suitable for general questions, explanations, and text generation. It is less suitable when answers must be based on specific private data that has not been provided to the model.

A rule-based workflow is suitable when the required questions and calculations are known in advance. It is predictable and easy to test, but its coverage depends on the rules written by the developer.

An AI agent is the most suitable option for this college assistant when it must answer different questions, retrieve private course-fee data, perform calculations, and generate natural-language responses. It combines the language model's flexibility with the accuracy of tools that operate on the stored data. The agent must still be tested and protected against invalid tool calls or other failures.

## 8. Conclusion

This project demonstrates the differences between a plain chatbot, a rule-based workflow, and an AI agent using the same college course-fee scenario. The plain chatbot generated natural responses but did not reliably answer questions requiring the local fee data. The rule-based workflow correctly answered the fee and scholarship questions for which rules were implemented, but it could not handle the unsupported comparison and welcome-message requests