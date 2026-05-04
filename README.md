1. Overview

The Domain Mapping System defines a structured hierarchy for question generation.

The hierarchy follows this format:

```text
Domain → Topic → Subtopic
```

This ensures that every generated question is linked to a valid academic or technical category.

---

2. Objective

The objective of this task is to ensure that the question generator produces structured, domain-relevant, and meaningful questions.

This system prevents random question generation by forcing the generator to select a valid:

- Domain
- Topic
- Subtopic

before creating a question.

---

. Domains Included

The mapping contains the following domains:

1. DSA
2. Machine Learning
3. DBMS
4. Operating Systems
5. Computer Networks
6. Generic

The `Generic` domain is used as a fallback when an unknown domain is provided.

---

4. Hierarchy Rules

Each domain contains multiple topics.

Each topic contains multiple subtopics.

Example:

```json
{
  "DSA": {
    "Arrays": ["Two Pointer", "Sliding Window", "Prefix Sum", "Kadane Algorithm"]
  }
}
```

This means:

```text
Domain: DSA
Topic: Arrays
Subtopics: Two Pointer, Sliding Window, Prefix Sum, Kadane Algorithm
```

---

5. Validation Rules

The system must follow these validation rules:

  Rule 1: Mapping must not be empty

  If the mapping is empty, question generation must be blocked.

  Rule 2: Domain must be valid

  If the selected domain exists in the mapping, use it.

  If the selected domain does not exist, use the fallback domain:

```text
Generic
```

Rule 3: Topic must belong to selected domain

A topic cannot be selected unless it exists inside the selected domain.

Rule 4: Subtopic must belong to selected topic

A subtopic cannot be selected unless it exists inside the selected topic.

Rule 5: No overlapping topics across domains

Topics should be unique within their domain and should not be reused unnecessarily across unrelated domains.

Rule 6: No vague topic names

Avoid vague topics such as:

- Basics
- Introduction
- Miscellaneous
- General

Instead, use specific topics such as:

- CPU Scheduling
- SQL Queries
- Feature Engineering
- Graphs

---

6. Question Generator Behavior

The question generator should follow this flow:

```text
User Input
→ Select domain
→ Validate domain
→ Select topic
→ Validate topic
→ Select subtopic
→ Validate subtopic
→ Pass domain, topic, and subtopic to prompt
→ Generate question
```

---

7. Prompt Format

The selected values should be passed to the LLM prompt like this:

```text
Generate one interview-style question.

Domain: DSA
Topic: Arrays
Subtopic: Sliding Window
Difficulty: Medium

The question must strictly belong to the selected domain, topic, and subtopic.
```

---

8. Edge Case Handling

Case 1: Unknown Domain

Input:

```text
Cyber Security
```

If this domain does not exist in the mapping, the system should use:

```text
Generic
```

Case 2: Empty Mapping

If the mapping is empty:

```json
{}
```

The system should block question generation and return:

```text
Question generation blocked: domain mapping is empty.
```

Case 3: Invalid Topic

If the topic does not belong to the selected domain, the system should select a valid topic from that domain.

Case 4: Invalid Subtopic

If the subtopic does not belong to the selected topic, the system should select a valid subtopic from that topic.

---
