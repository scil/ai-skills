# Binding: shell scripts (POSIX sh and Bash)

How the catalog's questions show up in shell scripts. If a plan adds or changes a shell script, load this file. A shell script is a `*.sh` file, a Git hook, or a CI or deploy step in shell. Checked against Bash 5.2 and GNU grep 3.11 (2026-11).

Each entry: **shows up as** · **look for** · **fix**.

## K. A pipeline judges input

**K2.5: a negative match passes on empty input.**
- *Shows up as:* a gate is written as `cmd | grep -qv 'healthy'`. Its intent is to fail on any line that does not say healthy. If `cmd` prints nothing, `grep -v` matches no line and returns 1, so the gate passes. Three causes give empty output: `cmd` fails, nothing runs, or a filter drops every line. A count check (`grep -c` gives 0) passes the same way. A listing that leaves out stopped items also shrinks the input with no error, for example `docker compose ps` without `--all`.
- *Look for:* `grep -v`, `grep -qv` or `! grep -q` as a pass condition. Also look for a pipe whose first command can fail while nothing reads its exit status, and for a gate that never counts its input.
- *Fix:* capture the output in a variable and check the exit status of the command. If the output is empty, fail. Then test the lines: `grep -v 'healthy' <<<"$out" | grep -q .`. List stopped items too (`--all`). One test runs the gate with nothing running.
