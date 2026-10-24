# Verdict protocol

## 1. Corpus first

For each claim, before searching, write the corpus that would contain it if it were true. Each domain reference has a corpus-by-claim-type table and the wrong-corpus incidents behind it (AI agents: `ai-agents.md` §1 and §3; IT security: `it-security.md` §1).

Rules:

- A vendor has several documentation properties (product docs, platform docs, cookbook, engineering blog, changelog). Name which one.
- "X does Y" about an organization may be about one team's post, not about the organization's public repository.
- Widen the search only after the named corpus is exhausted, and say that it was.

## 2. Verdict vocabulary

| Verdict | Meaning | Must include |
|---|---|---|
| CONFIRMED | the source says it, in substance | source URL, quote or paraphrase, source date |
| PARTLY | the source says part of it, or with a condition the claim dropped | which part, the condition |
| NOT FOUND | searched the named corpus and it is not there | the corpus searched; a second corpus tried, if any |
| CONTRADICTED | a source of equal or higher tier says otherwise | the source, and a check that the claim and the source are about the same object |
| CONFLATED | the sentence joins pieces from different sources | each piece with its real source |
| WRONG OBJECT | the claim is about X; it was being checked against Y | both objects named |
| INVENTED | the object described does not exist | how its absence was established (tree listing, API, direct fetch) |

A verdict never says only "wrong". It says which of these, and shows the evidence.

## 3. Report shape

1. **Outcome first**: how many claims, how many in each verdict; which verdicts of your own you revised, and why.
2. **Source table** (tiered, dated) before the discussion.
3. **Per claim**, one short block: quote → corpus → verdict → evidence → what it changes downstream.
4. **Disagreements** as a table with the scope line that explains each.
5. **What is only reported**, kept separate from what is established.
6. Sources list with links.

Numbers go in tables, not prose. A revised verdict is stated as a revision, with the first verdict and the reason it was wrong; that is the most useful line in the report.
