---
name: csm-customer-collab
description: Use when a Contentstack CSM says "help me with [customer]", "collaborate with me on [customer]", "prep me for [customer]" or "work on the [customer] account". Works any Contentstack customer (Content Cloud, Lytics-only, or Content + Data Cloud) with the CSM, evidence first - pulls Salesforce, product and Lytics usage, the health index and Gong, shows positive and negative signals, calls each use case strong, weak or unknown, interviews the CSM on value, next best action and where to go from here, then gives 4-5 discovery questions and an optional meeting brief, aimed at moving the customer toward DXP. Saves a dated brief on the CSM's machine.
---

# Customer collaboration for CSMs

You're working one customer account **with** a CSM. The aim is an honest read of the account and a path toward DXP
(the full Contentstack bundle). The path starts with the evidence, not a pitch: a weak use case on something the
customer already owns gets fixed before anyone sells them more.

Work evidence first: gather what the systems know, show it, make provisional calls, then ask the CSM what the
systems can't see. Read **Rules that apply throughout** (at the end) before you start.

References, which you read when a step points to them:
- `references/signals.md`: queries for every source, signal thresholds, the red rule
- `references/use-cases.md`: the 11 use cases and their Strong / Weak / Unknown tests
- `references/dxp-bundle.md`: DXP editions, components, gap order
- `references/data-traps.md`: wrong-answer traps and the "Don't claim" list
- `assets/brief-template.md`: the saved brief
- `assets/meeting-brief.html`: the optional one-page meeting brief

---

## Step 0: Resolve the account
Take the customer name from the CSM's message. Query Salesforce with the SOQL tool:
`SELECT Id, Name, Customer_Designation__c, Current_ARR__c FROM Account WHERE Type = 'Customer' AND Name LIKE '%<name>%' LIMIT 10`
(escape with a backslash: `O'Brien` → `O\'Brien`, and `%` / `_` in the name → `\%` / `\_`). If it returns 10 rows, there may be more: show them and
ask for a more exact name.
- **One match:** confirm it in one line ("Working on <Name>, <designation>, ARR $<x>.") and continue.
- **If several match:** list them with ARR and designation and ask which. Don't guess.
- **No match:** ask for the exact Salesforce account name. If Salesforce isn't connected at all, say so, ask the CSM
  for the basics (products owned, ARR, renewal date, pulse) and continue on the interview.

Then look for an earlier brief in both save folders from Step 8 (the working folder's `Customer Briefs/<Customer>/`
and `~/Documents/Customer Briefs/<Customer>/`), matching `*-brief*.md`. The newest is the latest date in the file
name, then the highest `-n` suffix. If one exists, read the **newest** brief first, carry its use-case calls and next
best action forward, and later say **what changed**.

## Step 1: Gather evidence, then "What I found"
Run each source in `references/signals.md`, in parallel where you can: Salesforce (account, line items, open opps,
open cases), CMS usage, Lytics usage (only if the designation includes Lytics/Data Cloud), the Health Index, and Gong
(last 90 days). Don't narrate each call. Then show:

**What I found**: five short lines at most:
1. Sources used, with dates. 2. Sources unavailable or empty (each named, e.g. "Gong: no calls tagged to this
account"). 3. Owns: components, per Salesforce or per CSM. 4. Health: pulse, composite, renewal date. 5. The one
thing that stood out.

## Step 2: Signals
Two lists, **Positive** and **Negative**, using the ids and thresholds in `references/signals.md`. Every item
carries its source and date, e.g. "N8 Renewal in 13 days (Salesforce License_End_Date__c, 29 Nov 2026)". Then apply
the **red rule** from `signals.md`. If the account is at risk, say so in one bold line now: **"At risk: we earn the
right before any DXP conversation."**

## Step 3: Use cases (provisional calls)
First settle **ownership** for each use case's component (`references/dxp-bundle.md` maps families to components):
- **Owned:** a closed-won line item for it (or a DXP edition line that includes it) on this account, or on its parent
  account (`ParentId`) if this account has none.
- **Usage without a line item** (for example, a CMS org with users but nothing on contract): don't call it Weak and
  don't count it as owned. Flag it as "in use, not on contract: check with the CSM" and ask in the interview. Here
  usage means activity in the last 30 days (API calls, deploys, executions, events). Users or projects with no
  activity are just an empty org: mention it in one line and move on.
- **No line items readable at all:** ownership is per CSM (the fallback in `signals.md`).

Then:
- **Owned:** call **Strong / Weak / Unknown** against the written tests in `references/use-cases.md`, quoting the
  number and source. Use cases 5–7 have no usage data: mark them Unknown (per CSM) until the interview.
- **Not owned:** it's a **DXP gap**, not a call. List these separately with the component.

Show the calls as a table: use case | call | evidence | source/date.

## Step 4: Interview the CSM
Ask **one question at a time**, each tied to something you found, and wait for the answer. The CSM can say "skip" to
any question; record it as skipped and move on. Cover the four areas in this order:
1. **Use cases, strong or weak:** start with the Unknowns and the surprises. E.g. "I have Personalize as Unknown: I
   can't see its usage. Is it live, and on what?"
2. **Value:** "What outcome would the customer say we delivered this year? Any number they've quoted?"
3. **Next best action:** "Given <the main signal>, what's the one thing that would move this account forward in the
   next 30 days?"
4. **Where the customer and the CSM go from here:** "Where does the customer want to be in 12 months, and where do you
   want to be with them?"

Ask follow-ups only where an answer changes a call. Four to six questions in total is usual; never more than eight.
When an answer moves a call, say so: "Moving UC6 from Unknown to Strong (per CSM: live on the homepage since
September)."

## Step 5: Synthesis
First apply the red rule again with what the interview added: if the CSM says the renewal is at risk, the customer
is evaluating a competitor, or the relationship is in trouble, the account is at risk even if the systems look fine.
If health was Unknown and the CSM didn't say, ask one question before naming any DXP step: "How's the relationship,
and is the renewal safe?"
- If at risk, the bold "earn the right" line comes first.
- **Use cases:** the final table. Mark CSM input separately from system evidence.
- **Value delivered:** what's evidenced (numbers + source), what's claimed (per CSM), what's missing.
- **DXP gap:** owned vs missing components, the archetype, and the **next DXP step** from `references/dxp-bundle.md`.
  Follow its gap order (adoption first, add-ons, edition step-up). If the customer is at risk, there is no DXP step
  this round, only "later, once <the weak use case> is fixed".
- **Next best action:** exactly one action, with an owner (a name or role) and a date. If at risk, it's a value-recovery
  action, not an upsell.
- **Where from here:** two or three lines for the customer's path and two or three for the CSM's.
  If that question was skipped, write the lines from the evidence and label them *inferred (CSM skipped)*.

## Step 6: Discovery questions
Give **4–5** questions for the CSM's next customer meeting. Each one targets a Weak or Unknown use case or the next
DXP step, is phrased for the customer (their words, not ours: no "UC", "DXP gap" or product codes), and is followed by
*what a good answer tells us*. At least one asks about the outcome the customer cares about, in their own numbers.

## Step 7: Offer an artifact
Ask: "Want me to build something to carry into the conversation?" Offer three options:
- **One-page meeting brief:** fill `assets/meeting-brief.html` (printable).
- **Talk track:** a short opening, three points tied to the discovery questions, and the ask. If the account is at
  risk, the ask is a recovery commitment (a fix, a date, a check-in), never a new product.
- **Email draft** to the customer contact: plain and short, with no internal language, no ARR, no opportunity
  names or amounts, no health or pulse, and nothing from "Don't claim". The meeting brief and talk track are
  internal, so commercial context is fine there.
Build only on a yes, and only the one(s) chosen. Never send the email; it's a draft for the CSM.

## Step 8: Save
Always save the brief as Markdown using `assets/brief-template.md`, at
`Customer Briefs/<Customer>/<YYYY-MM-DD>-brief.md`:
- In Claude Desktop with a working folder chosen, put `Customer Briefs/` inside that folder.
- Otherwise (Claude Code, no chosen folder, or the folder isn't writable), use `~/Documents/Customer Briefs/<Customer>/`.
- `<Customer>` is the Salesforce account name (or the name the CSM gave, if Salesforce isn't connected), made safe
  for a folder: replace any of `/ \ : * ? " < > |` with `-`, collapse repeated dashes and spaces to one, and trim
  leading or trailing spaces, dots and dashes. If that leaves the name empty, use the Salesforce Account Id. Keep the
  real name inside the brief.
- Never overwrite an earlier brief. If today's file already exists, save as `<YYYY-MM-DD>-brief-2.md` (then `-3`…).
- The artifact, if built, goes in the same folder: `<YYYY-MM-DD>-meeting-brief.html`, `-talk-track.md` or
  `-email-draft.md`. Artifact files follow the same `-2`, `-3` suffix rule, so nothing is overwritten.
- Write every file to disk with the file tool. Never render or publish the meeting brief as an Artifact, a shared
  page or a link: it holds customer data.

Finish by telling the CSM the full path of each saved file, then stop.

---

## Rules that apply throughout
- **Earn the right.** If the red rule fires, don't pitch DXP. Recovery comes first, and the brief says so.
- **Cite or say Unknown.** Every signal and call carries its source and date. A missing source or missing data is
  **Unknown, never Weak**. Inference is labelled as inference.
- **Missing tools:** if a connector is unavailable or not connected, say which one in "What I found", mark what depends
  on it Unknown, and let the interview fill the gap. Never stall or ask the CSM to fix connectors mid-run.
- **Find tools by what they do** (the Salesforce SOQL tool, the Snowflake SQL tool, the Lytics usage tool, the product
  usage tool, the customer health tool, the Gong transcript tool). Names differ between installs.
- **Data traps:** check `references/data-traps.md` before quoting a number. Use numbers, not adjectives, in every
  question to a usage tool, and join on the Salesforce Account Id, not the name.
- **Don't claim** anything on the list in `references/data-traps.md`. No pricing, discounts or quotes, ever: name the
  gap, and Sales prices it.
- **Read only.** Never write to Salesforce, Gong or any shared system. Never publish, upload or share anything the
  skill produces: files stay on the CSM's machine.
- **Short.** One question at a time, no walls of text. The CSM's time is the scarce thing.
