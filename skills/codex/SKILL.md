---
name: codex
description: "Delegate coding to OpenAI Codex CLI (features, PRs)."
---


## Host integration

Resolve sibling skills from this bundle first. For browser control, read the sibling ego-browser skill (or its installed user-wide copy) and use ego-browser CLI with TaskSpace. Map tool names to the tools actually available in Claude Code or Codex; examples do not grant permissions. Resolve runtime paths on the current host rather than treating imported paths as proof of installation. Preserve current user authorization for external writes; installing this bundle starts no generation, upload, post, watcher or episode.

# Codex CLI

Delegate coding tasks to [Codex](https://github.com/openai/codex) via the Hermes terminal. Codex is OpenAI's autonomous coding agent CLI.

## When to use

- Building features
- Refactoring
- PR reviews
- Batch issue fixing

Requires the Codex CLI. Repository checks apply by default; when the installed `codex exec --help` exposes `--skip-git-repo-check`, use that flag for authorized browser/non-repository work rather than creating an unnecessary git repository.

## Prerequisites

- Codex installed: `npm install -g @openai/codex`
- OpenAI auth configured: either `OPENAI_API_KEY` or Codex OAuth credentials
  from the Codex CLI login flow
- Run inside the intended repository for code work. For non-repository tasks, check local `exec --help` and use supported `--skip-git-repo-check` without initializing unrelated directories.
- Use `pty=true` in terminal calls — Codex is an interactive terminal app

For Hermes itself, `model.provider: openai-codex` uses Hermes-managed Codex
OAuth from `~/.hermes/auth.json` after `hermes auth add openai-codex`. For the
standalone Codex CLI, a valid CLI OAuth session may live under
`~/.codex/auth.json`; do not treat a missing `OPENAI_API_KEY` alone as proof
that Codex auth is missing.

## Checking usage limits on the Mac mini

- Read current `codex --help`, `codex login status`, and `codex doctor --summary --no-color --ascii` before trying a reset. Compare the current `/status` output against timestamped Hermes provider errors; old HTTP 429 logs do not prove that the account is still exhausted.
- Hermes-managed OAuth and standalone Codex CLI credentials can differ. Compare the ChatGPT account/user identifiers locally without exposing access/refresh tokens; matching token strings is not required for the same account.
- Open an interactive read-only CLI in an empty scratch directory for diagnosis. Skip updates unless needed/authorized and choose **Continue without trusting** for unreviewed hooks; do not approve arbitrary hooks to reach `/status`.
- With Hermes PTY, send `/status` using `process_manage(action='write', data='/status')`, then send a separate raw carriage return (`data='\r'`). `submit` appends LF and can insert a newline, causing the slash command to be submitted as ordinary model text instead of executed locally.
- Capture the full status panel with `process_manage(action='log')`; `poll` previews can omit the relevant quota or show only another model's limits. Preserve the distinction between account limits and model-specific limits.
- For deterministic quota checkpoints, use the installed Codex app-server stdio RPC: start `codex --no-daemon app-server --listen stdio://`, send `initialize` with clientInfo name/version, await its response, notify `initialized`, then request `account/rateLimits/read`. Read only the `codex` bucket from `rateLimitsByLimitId` (or the legacy `rateLimits`) and its window with `windowDurationMins=10080`; preserve actual `usedPercent` and `resetsAt` with observation time. Apply timeouts and terminate the read-only process after the response. Do not start a thread/model turn or read credential files merely to measure quota. Account-wide rounded deltas are not exact episode attribution or a guaranteed hard cap; use cumulative baselines and a safety margin.
- `hermes auth reset openai-codex` only clears local credential exhaustion status; it is not an OpenAI quota reset. Redeem a provider-side reset only through a real eligible reset control and with the user's authorization; never buy credits, change plans/accounts, or overwrite credentials as a substitute.
- A response saying the selected model requires a newer Codex client is a version-compatibility error (HTTP 400), not usage exhaustion. Report or address that separately; do not claim a reset fixed it.

## One-Shot Tasks

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

For scratch work (Codex needs a git repo):
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

## Background Mode (Long Tasks)

```
# Start in background with PTY
terminal(command="codex exec --sandbox workspace-write 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--sandbox workspace-write` (`-s`) | Sandboxed but auto-approves file changes in the workspace (the recommended auto-build mode) |
| `--dangerously-bypass-approvals-and-sandbox` | No sandbox, no approvals (fastest, most dangerous; `--yolo` still works as a hidden alias) |
| `--sandbox danger-full-access` | No Codex sandbox; useful when the host service context breaks bubblewrap |

> **Deprecated:** `--full-auto` still works but the live CLI warns to use `--sandbox workspace-write` instead.

## Hermes Gateway Caveat

When invoking the Codex CLI from a Hermes gateway/service context (for example,
Telegram-driven agent sessions), Codex `workspace-write` sandboxing may fail even
when the same command works in the user's interactive shell. A typical symptom is
bubblewrap/user-namespace errors such as `setting up uid map: Permission denied`
or `loopback: Failed RTM_NEWADDR: Operation not permitted`.

In that context, prefer:

```
codex exec --sandbox danger-full-access "<task>"
```

Use process boundaries as the safety layer instead: explicit `workdir`, clean git
status before launch, narrow task prompts, `git diff` review, targeted tests, and
human/agent confirmation before committing broad changes.

## Browser-control handoffs

- For an explicitly requested browser handoff, check installed CLI authentication and MCP availability without reading credential values. Ask Codex to load its applicable browser instructions and test the existing authenticated connection using its normal consent path.
- A native desktop input failure does not prove a separately authorized browser extension connection is unusable. Test the configured browser integration; never bypass OS locks, browser consent, or site permissions.
- Scope the handoff to the exact existing target ID, permitted fields, forbidden publication/visibility actions, source assets, and evidence directory. Run only one editor on the target.
- Keep known-blocked fields separate from independently feasible fields. Do not guess content certification from ambiguous ASR, substitute unapproved images, or call a partial draft complete.
- Require close/reopen readback and saved screenshots. After the worker exits, inspect those exact-target artifacts yourself and compare text fields programmatically before claiming success.

## PR Reviews

Clone to a temp directory for safe review:

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## Parallel Issue Fixing with Worktrees

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --sandbox workspace-write exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --sandbox workspace-write exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## Batch PR Reviews

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## Rules

1. **Always use `pty=true`** — Codex is an interactive terminal app and hangs without a PTY
2. **Repository scope** — use the existing repository for code work; supported `exec --skip-git-repo-check` permits non-repository tasks without a dummy git initialization.
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits cleanly
4. **`--sandbox workspace-write` for building** — auto-approves changes within the sandbox (`--full-auto` is deprecated for this)
5. **Background for long tasks** — use `background=true` and monitor with `process` tool
6. **Don't interfere** — monitor with `poll`/`log`, be patient with long-running tasks
7. **Parallel is fine** — run multiple Codex processes at once for batch work
