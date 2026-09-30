---
description: A how-to guide should be numbered, imperative, one action per step, in strict STE style.
max_turns: 10
allowed_tools: [Read, Skill]
---

Write a short how-to guide for rotating an API key in our internal tool, vault-cli. The steps are: create a new key with `vault-cli key create --name prod`, put the new key in the app config, then revoke the old key with `vault-cli key revoke --id OLD_ID`. Reply with only the guide, with no notes or commentary.
