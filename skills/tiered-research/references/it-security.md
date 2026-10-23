# IT security research

Read this when the question or the claims are about IT security: vulnerabilities, advisories, breaches, security tools, hardening guidance, or a defence plan. It adds security-specific corpora and traps to the general method; the tiers and verdicts stay as in `source-tiers.md` and `verdict-protocol.md`. Origin: the WordPress-VPS defence research of 2026-10-23 (see `readme.md`).

## 1. Corpus by claim type

| Claim is about | Search first (T1) | Then | Notes |
|---|---|---|---|
| A vulnerability in a product | The project's own advisory page (e.g. `nginx.org/en/security_advisories.html`, `php.net/archive/<year>.php`, `nodejs.org/en/blog/vulnerability`), the GitHub security advisories of its repo | The CVE record from the CNA: `https://cveawg.mitre.org/api/cve/<CVE-ID>` | The project and the CNA may rate severity differently; record both (§2.1). |
| Whether a distro is patched | The distro tracker: `security-tracker.debian.org/tracker/<CVE>`, `ubuntu.com/security/<CVE>`, the distro's `-security` suite | — | Trackers can lag upstream by more than a week; never infer "patched" from upstream alone, nor "unpatched" from the main suite alone. |
| Exploitation in the wild | Vendor's own telemetry post (e.g. a cloud provider's threat blog), CISA KEV catalogue | Security-vendor blogs (T4) | Record the date of first observed exploitation separately from the disclosure date. |
| A breach or incident at an organisation | The victim's own statement (trust centre, status page, blog, filing) | News (T4), attacker leak-site claims (T4) | See §2.3. |
| A security tool's status | `api.github.com/repos/<owner>/<repo>` (licence, `pushed_at`, `archived`), `/releases/latest`, the README, the vendor's product and pricing pages | Aggregators (T4) | Status decays: see §2.4. |
| A tool's or service's free tier, price, licence | The vendor's pricing page and licence file on the day of checking | — | A README licence claim and GitHub's licence field can disagree; record both. |
| A configuration flag's effect | The owner's reference docs and, when docs are silent, the source code of the function that reads the flag | — | See §2.5. |
| Interaction between two components (firewall vs container runtime, proxy vs IP-based blocking) | Each component's own docs on the other | — | See §2.6. |
| Hardening or defence structure | Framework owners: NIST CSRC (glossary, CSF 2.0, SP 800-61r3, SP 800-63B), CIS Controls (v8.1, IG1), OWASP cheat sheets | Practitioner lists (T4) | See §2.8. |
| Attack trends ("attacks now take days") | Vendor threat reports with their own data (Mandiant M-Trends, Google GTIG), peer-reviewed studies | Commentary (T4) | Separate the measured trend from the claimed cause (§2.9). |

## 2. Traps and the rule for each

1. **Severity is plural.** The project, the CNA and each distro may give different ratings for the same CVE (e.g. nginx "medium", F5 CVSS v4 9.2, Ubuntu "Medium"). Record all, with the scope that explains the split (configuration-dependent triggers, attack complexity). Do not pick one.
2. **"Incident" vs "security release".** A post saying a product "had an incident" often means it shipped a fix. Check whether there was a compromise or only a patch; if the sentence joins several unrelated items (a CA key compromise, a vendor breach, a CVE batch), mark it CONFLATED and list the pieces.
3. **Attacker claims are T4, however detailed.** In a breach, the victim's statement is T1 for what it says and silent on what it omits. A detail found only in the attacker's claims (e.g. "keys committed in the repository") is "reported", even when the victim's remediation ("we will expand secret scanning") seems to fit it. Never fill the victim's silence with the attacker's version.
4. **Free and maintained are dated facts.** Tools change licence, close free tiers, reach end of life or go feature-complete (2026 examples: Wordfence CLI free licences ended 2026-10-14; gitleaks became security-fixes-only; Promtail reached EOL). Check the status on the day of the research and write the date. An answer given from memory before the research must be re-checked and, if wrong, listed as a revision.
5. **A flag can switch off more than its name says.** Read the function that consumes the flag before recommending it (e.g. WordPress `DISALLOW_FILE_MODS` also disables all background auto-updates through `wp_is_file_mod_allowed()`).
6. **One layer can silently bypass another.** Before relying on a control, search each neighbouring component's docs for known bypasses (e.g. Docker's published ports skip ufw; IP-based blocking behind a proxy blocks the proxy unless the real-IP header is configured).
7. **Security tools are supply chain.** Check the tool's own security advisories before recommending it (e.g. Trivy's March 2026 compromise, GHSA-69fq-xp46-6x23). Recommend pinned, signature-verified installs, never `latest` or mutable tags.
8. **Use a framework as the structure, not a practitioner's list.** Organise a defence plan by an owner-published framework: defence in depth (NIST glossary) for layers, NIST CSF 2.0 functions for the lifecycle, CIS Controls v8.1 / IG1 as the checklist. A circulating "N principles" list is an input to map onto the framework and credit, not the frame.
9. **Trend measured, cause claimed.** Time-to-exploit data (T1 vendor data) and the claim that AI causes the change (often T4) are separate rows. A lab capability study (T2) is not real-world timing.
10. **Fit verdicts name the scale.** "Use now / optional / not relevant" must state the deployment it was judged for (e.g. one VPS, small team). Keep the not-relevant tools in the report with their facts; the reader may need them for study or other work.
11. **Repository red flags are facts to record, not to resolve.** Star counts implausible for the repository's age, a backup of a deleted upstream, a disclaimer that forbids the advertised use, a null licence field with commercial terms in the README, an extra EULA over an open-source licence. Write each as found.

## 3. Delegating security research to subagents

- A brief that asks a subagent to describe offensive tools' capabilities, attack workflows or campaigns can be stopped by a safety classifier mid-write, losing the whole output. Write defender-oriented briefs: purpose in one neutral sentence from the README, licence, maintenance, requirements, fit for the defender, and caveats (own systems only, staging clone, spend caps). Ask for metadata, not technique.
- Split the work by layer or corpus (host and edge; application; inventory, secrets and operations; tools), give each subagent its own output file in the scratchpad, and require the source table with tier, `source-date` and `checked` columns.
- Spot-check the most consequential claims yourself against T1 before publishing (for example, the advisory behind an "urgent" item).
