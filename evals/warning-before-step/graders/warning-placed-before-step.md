---
type: llm
---

PASS if a warning or caution about the data loss appears before the step that runs `make db-reset`, either as a line above the step list or as its own earlier step.
FAIL if the warning comes only after the step that runs `make db-reset`, or is inside that step, or there is no warning.
