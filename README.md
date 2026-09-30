# claudicus-maximus

A Claude Code plugin with one skill, `plain-english-writing`. It helps Claude write clear documentation and other prose. It uses Diataxis for documentation page types, and ASD-STE100, Strunk and gov.uk guidance for wording. The rules are guidelines: Claude can bend one when meaning or readability would suffer.

## Layout

- `.claude-plugin/plugin.json` – plugin manifest
- `.claude-plugin/marketplace.json` – marketplace manifest, so the repository can be added as a marketplace
- `skills/plain-english-writing/SKILL.md` – the skill
- `skills/plain-english-writing/references/ste-and-style.md` – the full rule list, with the reason for each rule
- `evals/` – eval cases for `claude plugin eval` (one folder per case)
- `evals-bash/` – eval cases that need Bash (run separately)
- `tests/` – unit tests for the readability script (`python3 -m unittest discover -s tests`) and `tests/trigger/`, which measures how often the skill fires on its own

## Install

This repository is also a plugin marketplace. In Claude Code:

```
/plugin marketplace add portswigger-tim/claudicus-maximus
/plugin install claudicus-maximus@claudicus-maximus
```

Or from a terminal:

```bash
claude plugin marketplace add portswigger-tim/claudicus-maximus
claude plugin install claudicus-maximus@claudicus-maximus
```

Use `/plugin marketplace update` to pick up new versions. The skill runs on its own when you write or edit text. You can also call it by name: `/claudicus-maximus:plain-english-writing`.

## Try it locally

```bash
claude --plugin-dir .
```

## Run the evals

The evals call the model, so they use your plan's usage or API bill.

```bash
claude plugin eval . --ablation none
```

The `readability-script` case needs Bash, so it lives in `evals-bash/` and is not part of the default suite. It checks that the model runs the skill's readability script. Run it with:

```bash
claude plugin eval . --eval-dir evals-bash --ablation none --allow-tools "Bash(python3 *)"
```

Bash evals run in a sandbox. The harness refuses to run them if a credential store such as `~/.docker` holds a symbolic link. On a Mac with Docker Desktop, in Claude Code 2.1.280, the links in `~/.docker/bin` trigger this ([anthropics/claude-code#94308](https://github.com/anthropics/claude-code/issues/94308)). A temporary workaround is to move `bin` *outside* `~/.docker` for the run and put it back afterwards. Renaming it inside `~/.docker` does not help.

```bash
mv ~/.docker/bin ~/.docker-bin-parked; claude plugin eval . --eval-dir evals-bash --ablation none --allow-tools "Bash(python3 *)"; mv ~/.docker-bin-parked ~/.docker/bin
```

Docker Desktop keeps its tool links in `bin`, so restore it even if the eval fails. Check with `ls ~/.docker/bin`.

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

## Trigger test

`claude plugin eval` loads only this plugin, so it cannot tell you whether the skill fires in a busy session with many other tools and skills. `tests/trigger/` checks that. It runs 10 varied prompts, 8 that should fire the skill and 2 that should not, in a normal session, and counts skill calls:

```bash
python3 tests/trigger/drive.py --reps 2
```

Each run is a real model call (about $0.15). The last result was 16 of 16 writing prompts fired and 0 of 4 unrelated prompts fired. Before the description named explanations and chat messages, 13 of 16 fired, and the missed prompts were an explanation page and a Slack message.
