---
type: llm
---

PASS if a warning or caution about the data loss appears before the step that runs `make db-reset`, starts with a clear command or condition (for example "Do not run this on ..." or "Make sure that ..."), and states the result (all data in the test database is deleted).
FAIL if the warning comes after the step, is buried in the middle of a paragraph, or does not say what is lost.
