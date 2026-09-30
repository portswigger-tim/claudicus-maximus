# claudicus-maximus

A Claude Code plugin with one skill, `plain-english-writing`. It helps Claude write clear documentation and other prose. It uses Diataxis for documentation page types, and ASD-STE100, Strunk and gov.uk guidance for wording. The rules are guidelines: Claude can bend one when meaning or readability would suffer.

## Layout

- `.claude-plugin/plugin.json` – manifest
- `skills/plain-english-writing/SKILL.md` – the skill
- `skills/plain-english-writing/references/ste-and-style.md` – the full rule list, with the reason for each rule
- `evals/` – eval cases for `claude plugin eval` (one folder per case)

## Try it locally

```bash
claude --plugin-dir .
```

## Run the evals

The evals call the model, so they use your plan's usage or API bill.

```bash
claude plugin eval . --ablation none
```

Drop `--ablation none` to also run each case without the plugin and see the difference.

Use a judge model that is stronger than the default for the `llm` graders:

```bash
claude plugin eval . --ablation none --judge-model sonnet
```

Run one case with `--case '<name>'`. The flag takes one value, so a second `--case` replaces the first.

## Known gaps

- **`explanation-nuance`** can score about 0.9. The model sometimes softens the author's hedge (for example "usually worth it" becomes "in general … worth it for any service"), and the judge fails that run. One failing run in five is expected. If it fails more often, the skill's guidance on keeping hedges needs a stronger example.
- **The judge only returns votes.** `claude plugin eval` does not show why a judge failed a run. To find the cause, split a rubric into single-clause graders.
- **The style regex graders are approximate.** For example, `no-passive-in-steps` misses passives that use an irregular participle it does not list.
- **The skill does not fire for every short text.** It did not fire for a commit message. That is fine: the reply was good without it.
