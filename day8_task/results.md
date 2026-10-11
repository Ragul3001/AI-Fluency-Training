# Day 8 — Agentic AI: Task Results

## 1. Configuration

- **Model:** `openai/gpt-oss-20b`
- **Embedding provider:** `fastembed`
- **Embedding vector length:** 384
- **MAX_DISTANCE:** `0.3`

## 2. Part A — Placement Policy Ingestion

Created `data/placement_policy.md` and indexed it using `python 1_ingest.py`.

The placement policy was retrieved successfully using `python 2_search.py`.

**Test question:** What CGPA do I need to be eligible for placements?

**Result:** `placement_policy.md` was retrieved with a distance score of `0.185`. Students need a CGPA of 6.5 or above and no standing arrears to be eligible for campus placements.

## 3. Part B — Exam Eligibility Tool

Tested `check_exam_eligibility` with four attendance values.

| Attendance | Result | Correct? |
|---|---|---|
| 82% | Eligible to write the exam | Yes |
| 70% | Condonation required; Rs. 500 per course | Yes |
| 50% | Not eligible | Yes |
| 120% | Error: attendance must be between 0 and 100 | Yes |

## 4. Part C — Relevance Guard

Implemented `search_handbook` using `similarity_search_with_score(query, k=3)` and a maximum distance threshold of `0.3`.

| Query | Distance score(s) | Result |
|---|---|---|
| What CGPA do I need to be eligible for placements? | 0.185 | Relevant placement policy retrieved |
| What is the capital of France? | 0.581, 0.586, 0.588 | Rejected with `NO_MATCH` |

The France question returned:

`NO_MATCH: this is not covered in the college handbook.`

## 5. Part D — Agent Run Results

| # | Tools called (in order) | Agent's answer (short) | Correct? (Y/N) | If N, why? |
|---|---|---|---|---|
| 1 | search_handbook | Placement eligibility requires a CGPA of 6.5 or above | Y | — |
| 2 | check_exam_eligibility | At 70% attendance, condonation is required; Rs. 500 per course | Y | — |
| 3 | get_course_fee (CS101), get_course_fee (AI202), search_handbook, calculator | Total = Rs. 32,000 | Y | — |
| 4 | calculator | Total with a 5-day late fee = Rs. 30,500 | Y | — |
| 5 | search_handbook | The agent does not know the capital of France because it is not covered in the handbook | Y | — |

## 6. Conclusion

All five required questions were tested in the same conversation thread, `task-run`. The agent used the expected tools for the fee calculation and attendance check, retained context for the follow-up question, and rejected an unrelated question using the relevance guard.