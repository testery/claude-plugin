---
name: testery-add-file
description: Attach a file (artifact, log, or input) to an existing Testery test run. Use to add context to a run after it has been created.
---

# Add a file to a test run

Wraps `testery add-file`. The file path is a **positional argument** (`FILE_PATH`), not a flag.

```bash
testery add-file ./path/to/file \
  --token "$TESTERY_TOKEN" \
  --test-run-id <id> \
  [--kind <KIND>]
```

Flags:
- `FILE_PATH` (positional, required): the local file to attach.
- `--test-run-id <id>`: the test run to attach the file to.
- `--kind <KIND>`: the kind of file being uploaded (e.g. pass `DotCover` for a DotCover JSON coverage file).
- Auth: `--token` / `--profile`, falling back to `~/.testery/credentials` or `$TESTERY_API_TOKEN`.
