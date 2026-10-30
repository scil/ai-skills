# Binding: Ansible (playbooks and roles that audit or change hosts)

How the catalog's questions show up when a plan audits or changes hosts with Ansible. Load this file when the tree has `ansible.cfg`, `playbooks/`, `roles/<name>/tasks/`, or an inventory. Checked against ansible-core 2.21 (2026-10).

Each entry: **shows up as** · **look for** · **fix**.

## G. The domain says what exists

**G4.4 — a lock-out guard whose input list came back empty.**
- *Shows up as:* before writing `authorized_keys` exactly from an allowlist, a task fingerprints the key Ansible logs in with and the listed keys, and an `assert` checks that the first is among the second. The probe is a multi-line `shell` on the control machine: `ssh-keygen -lf {{ (ansible_ssh_private_key_file ~ '.pub') | quote }}`. The inventory gives the key as `~/.ssh/<key>`; `quote` puts it in single quotes, the shell does not expand `~`, `ssh-keygen` fails, and `set -o pipefail` without `-e` lets the later lines run, so the task succeeds with no `login` line. The guard's input is empty. Here Jinja's `first` raised on the empty list and the play failed closed; the same guard written as `select(...) | list | length == 0` or `intersect` would have passed and written a list that locks Ansible out.
- *Look for:* `| quote` on a path that may start with `~` (key files, `ansible_ssh_private_key_file`, `lookup('env', 'HOME')` concatenations); multi-command `shell` with `pipefail` but no `-e`; an `assert` over a list derived from command output with no check that the list is non-empty.
- *Fix:* `| expanduser | quote` for control-machine paths; `set -euo pipefail` in every multi-command `shell`; the guard first asserts that its input is non-empty (the login fingerprint exists), then asserts membership; one test runs the guard with a key that is not listed and expects the refusal.

## I. One truth, several copies

**I5.1 — an enforce role's own file flagged by the audit of the same set.**
- *Shows up as:* an enforce role copies an MU plugin from `roles/<enforce>/files/` into `wp-content/mu-plugins/`, and the audit role compares that directory with `cs_mu_plugin_allowlist` (name and SHA-256) kept in inventory variables. After a correct enforce run, the audit reports the role's own plugin as unknown.
- *Look for:* `copy: src=` in an enforce role whose `dest` is a directory, path or file that an audit role reads with `find`, `stat` or a hash comparison.
- *Fix:* the audit adds the enforce role's files to its expected set by hashing them from the repository (`lookup('ansible.builtin.file', playbook_dir ~ '/../roles/<enforce>/files/<file>', rstrip=false) | hash('sha256')`), so the two never drift; the hand-kept allowlist holds only what the role does not install.
