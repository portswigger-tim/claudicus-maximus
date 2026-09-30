---
type: llm
---

PASS if the reply is a commit message whose first line is a short summary in the imperative form (for example "Rename getUser to fetchUser") and that mentions both the rename and the updated call sites, in the subject or in a short body. It is only the message, with no page headings, no numbered steps, and no explanation of what a commit message is.
FAIL if the first line is long or vague, the message is a documentation-style page with headings or steps, or it leaves out the rename or the call sites.
