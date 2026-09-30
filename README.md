# claudicus-maximus

A Claude Code plugin.

## Layout

- `.claude-plugin/plugin.json` – manifest
- `skills/` – skills (`plain-english-writing`)
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
