# Day 6 Task: Robust Tool Calling and Structured Outputs

## 1. Objective

The objective of this activity is to build a robust AI agent that uses tools safely, validates arguments, handles tool failures without crashing, and produces structured outputs.

The project uses a college fee assistant scenario with two tools:

- `get_course_fee`: retrieves a course's fee.
- `calculator`: evaluates basic arithmetic expressions safely.

The agent uses the Groq provider with the OpenAI-compatible model `openai/gpt-oss-20b`.

## 2. Chat Completions and Important Fields

The Chat Completions API accepts a list of messages containing roles such as `system`, `user`, `assistant`, and `tool`.

Important response fields include:

- `choices[0].message`: contains the assistant's response.
- `choices[0].finish_reason`: indicates why the generation ended.
- `message.content`: contains the assistant's text response.
- `message.tool_calls`: contains requested tool calls when present.

### Finish reasons

| Finish reason | Meaning | Agent behavior |
|---|---|---|
| `stop` | The response ended normally. | Return the final answer when no tools are requested. |
| `length` | The response reached its token limit. | Increase the token limit and retry, subject to a maximum. |
| `tool_calls` | The assistant requested tool execution. | Validate and execute the requested calls, then return the results to the model. |

The exact finish reason depends on the response returned by the API. My current test logs do not show a `length` retry, so this behavior needs a separate test.

## 3. OpenAI-Compatible Servers

An OpenAI-compatible server exposes an API that follows the OpenAI API request and response conventions. This allows an application to use a compatible provider by configuring its client and model settings.

Compatibility does not guarantee that every provider supports every API feature identically. Tool calling, JSON mode, schema enforcement, and other capabilities should be tested with the selected provider and model.

In this project, the configured provider is Groq and the model is `openai/gpt-oss-20b`.

## 4. Tool Calling: Five-Step Process

The tool-calling process is:

1. The user sends a question.
2. The assistant decides whether a tool is needed and requests a tool call.
3. The application validates the tool name and arguments.
4. The application executes the tool and sends its result back in a tool message.
5. The assistant uses the result to provide a final answer.

The model requests tools; the application is responsible for executing them. Tool arguments must not be trusted without validation.

## 5. Tool Schemas and Validation

The project defines two tool schemas in `tools_v2.py`. The shared `SCHEMAS` dictionary is derived from the same definitions used to send the tools to the model.

The schemas use:

- `type` to specify the expected data type.
- `properties` to define allowed arguments.
- `required` to identify mandatory arguments.
- `enum` to restrict values such as `semester` to `odd` or `even`.
- `additionalProperties: false` to reject unlisted arguments.

The `validate.py` implementation checks missing arguments, unexpected arguments, incorrect types, and invalid enum values.

### Validation results

| Input | Result |
|---|---|
| `{'course_code': 'CS101'}` | OK |
| `{'course_code': 'CS101', 'semester': 'even'}` | OK |
| `{}` | Missing required argument |
| `{'course_code': 101}` | Wrong argument type |
| `{'course_code': 'CS101', 'semester': 'summer'}` | Invalid enum value |
| `{'course_code': 'CS101', 'year': 2026}` | Unexpected argument |

These tests confirm that the validator rejects several common argument errors before execution.

## 6. JSON Mode vs. Schema-Constrained Outputs

JSON mode requests valid JSON but does not, by itself, guarantee that the returned object follows a particular application schema.

Schema-constrained output specifies the expected fields and their types. Its actual enforcement depends on the API and model feature support.

| Feature | JSON mode | Schema-constrained output |
|---|---|---|
| Valid JSON syntax | Requested | Requested |
| Fixed field names | Not necessarily | Defined by the schema |
| Expected field types | Must be checked | Defined by the schema |
| Application validation | Still recommended | Still recommended |
| Main purpose | Obtain JSON | Obtain data in a known structure |

### Observed structured-output results

For the question, “What do I pay for AI202 if I have the merit scholarship?”, the demonstrations returned:

- Free text mode: a JSON object containing `query`.
- JSON mode: a JSON object containing `program`, `scholarship`, `action`, and `user_query`.
- Schema mode: an object containing `course_code`, `needs_tool`, and `wants_scholarship`.

The examples demonstrate different output shapes. They do not alone prove that the provider enforces every schema constraint.

## 7. Fault Injection and Error Handling

The `inject_faults.py` script tests invalid tool requests. The objective is to return readable error strings instead of allowing malformed calls to crash the application.

### Fault-injection observations

| Test | Expected handling | Observed result |
|---|---|---|
| Good call | Execute valid tool | Fee returned: `18000` |
| Invalid JSON | Return parsing error | Error string returned |
| Unknown tool | Reject tool name | Available tools listed |
| Missing required argument | Reject arguments | Error string returned |
| Wrong argument type | Reject incorrect type | Error string returned |
| Invalid enum value | Reject unsupported value | Allowed values listed |
| Extra argument | Reject unexpected field | Error string returned |
| Unknown course code | Return a useful error | Valid course codes listed |
| Unsafe calculator expression | Reject unsupported expression | Calculator error returned |
| Empty arguments string | Reject missing expression | Error string returned |

All ten displayed tests completed without an uncaught exception. The errors were represented as strings that can be sent back to the assistant so it can potentially correct its request.

## 8. Robust Agent and Safety Guards

The robust agent implements several protective behaviors:

- **JSON parsing:** catches malformed tool arguments.
- **Tool-name checking:** rejects unknown tools.
- **Argument validation:** checks arguments against the corresponding schema.
- **Exception handling:** converts tool execution exceptions into error strings.
- **Token-limit retry:** increases `max_tokens` when the response ends with `length`, up to a configured limit.
- **Repeated-call guard:** stops repeated calls with identical tool names and arguments.
- **Maximum-step guard:** prevents the agent from continuing indefinitely.
- **Tool-result messages:** returns results using the matching `tool_call_id`.

A robust implementation should return exactly one tool-result message for every tool call in an assistant response, including when a guard is triggered. This keeps the conversation history consistent.

### Observed agent questions

| Question | Observed behavior | Result |
|---|---|---|
| Total CS101 and AI202 fees after a 10% scholarship | Two fee lookups and one calculator call | ₹27,000 |
| Compare DS303 and CS101 | Two fee lookups and one calculator call | DS303 is ₹3,000 more expensive |
| Fee for ME404 | Direct assistant response; no tool call was logged | Invalid course explained |
| Welcome message | Direct response without tools | Welcome message generated |

The first two questions required three sequential tool-calling steps each. Parallel tool execution and a token-limit retry were not demonstrated in this output and need separate tests.

## 9. Parallel Tool Calls

Parallel tool calls allow an assistant response to request multiple independent tools at once. For example, looking up the fees of CS101 and AI202 can be performed independently before calculating their total.

For each returned tool call, the application must:

1. Validate its name and arguments.
2. Execute or reject it.
3. append a tool message with that call's matching `tool_call_id`.
4. Send the complete tool results back to the assistant.

The number of tool calls in a response and the number of execution steps are different measurements. The current logs show one tool call per step, so parallel execution remains to be verified.

## 10. Before-and-After Guard Observations

| Risk | Protection in the implementation | Evidence |
|---|---|---|
| Malformed arguments | JSON parsing error handling | Invalid JSON test returned a string |
| Unexpected argument | Schema validation | Extra `year` field rejected |
| Incorrect type | Type validation | Integer course code rejected |
| Unsupported enum | Enum validation | `summer` rejected |
| Unknown tool | Tool registry lookup | `send_email` rejected |
| Unsafe expression | Restricted calculator parser | Unsupported expression rejected |
| Endless repetition | Repeated-call and step limits | Guard code present; trigger test still needed |
| Truncated output | Token-limit retry | Code present; retry test still needed |

The fault-injection tests provide evidence for the first six protections. The repeated-call and token-limit guards should also be tested directly to demonstrate their behavior.

## 11. Limitations

- A valid schema cannot guarantee that a requested course or business value exists.
- A tool can return an error string even when its arguments are valid.
- Provider compatibility varies, so JSON and schema behavior must be tested.
- Repeated-call protection may stop a loop, but it does not prove that every earlier action made progress.
- Parallel calls require careful handling of every tool-call ID.
- A token-limit retry needs a maximum to avoid unbounded retries.
- The current output does not demonstrate parallel calls or a `length` retry.

## 12. Conclusion

This project demonstrates a college fee assistant with validated tool arguments, controlled calculator operations, fault injection, tool execution, and structured-output examples.

The observed tests show that malformed JSON, missing arguments, incorrect types, unsupported enum values, unexpected arguments, unknown tools, unknown course codes, and unsafe calculator expressions are handled without uncaught exceptions in the displayed tests.

The agent also correctly calculated the combined scholarship-adjusted fee as ₹27,000 and the difference between DS303 and CS101 as ₹3,000.

Further testing is needed to demonstrate parallel tool calls, repeated-call termination, and token-limit retry behavior. These results should be documented only after the corresponding tests have been run.
