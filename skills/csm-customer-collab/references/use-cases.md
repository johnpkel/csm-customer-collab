# Use-case catalogue

Eleven use cases, each mapped to the DXP component that delivers it. For each one the customer **has** (they own the
product, or the usage data shows it in use), make a call: **Strong**, **Weak** or **Unknown**. Use cases they don't
have are **DXP gaps** (see `dxp-bundle.md`).

## Rules for every call
- Quote the number, the source and its date: "Weak: 0 deploys in the last 30 days (product usage table, to 15 Nov)".
- **Missing data or a missing source means Unknown, never Weak.** "I couldn't see it" is not evidence of failure.
- When the CSM's answer moves a call, say so: "Moving UC6 from Unknown to Strong, per CSM: live on the homepage
  since September."
- A call made only from the interview is labelled **per CSM**.
- Thresholds were set on 16 Nov 2026 from the spread across customer accounts (577 CMS customers, 425 Lytics
  customers). They are guides, not grades. Between Strong and Weak, the call is "Developing": name the number and
  what would make it Strong.
- Trends compare the last 30 days with the 30 before. If either window touches the known-bad data dates in
  `data-traps.md`, say so and lean on the latest window only.

---

## UC1 — Content operations at scale
**Component:** CMS. **Evidence:** active users, stacks, entries, content-management (CMA) API calls (a proxy for
authoring and publishing; there is no "entries published" metric).
- **Strong**: 35 or more users AND 14,000 or more CMA calls in the last 30 days, with CMA calls not down more than
  30% on the prior 30 days.
- **Weak**: fewer than 16 users, OR fewer than 1,000 CMA calls in 30 days, OR CMA calls down more than 50%.
- **Unknown**: no CMS usage row for the account.

## UC2 — Omnichannel delivery
**Component:** CMS delivery (CDN, GraphQL), locales, environments.
**Evidence:** total API calls in 30 days, number of stacks, locales and environments.
- **Strong**: 9.8 million or more API calls in 30 days AND (3 or more locales OR 3 or more stacks).
- **Weak**: fewer than 1 million API calls in 30 days, or total calls down more than 50%.
- **Unknown**: no CMS usage row.

## UC3 — Front-end hosting
**Component:** Launch. **Evidence:** Launch projects, deployments in the last 30 days.
- **Strong**: 1 or more projects AND 10 or more deployments in 30 days.
- **Weak**: projects exist but 0 deployments in 30 days (paid for, idle).
- **Unknown**: no CMS usage row. (No Launch projects at all = not in use: a DXP gap, not a Weak call.)

## UC4 — Workflow automation
**Component:** Automate. **Evidence:** automation executions in 30 days, execution errors, automation projects.
- **Strong**: 335 or more executions in 30 days with errors under 5% of executions.
- **Weak**: automations exist but fewer than 50 executions in 30 days, OR errors at 20% or more of executions.
- **Unknown**: no CMS usage row. (0 automations = not in use: a DXP gap.)

## UC5 — On-brand AI content
**Component:** Brand Kit, AI Credits. **Evidence:** none in Claude yet, so this is **per CSM** in v1.
Ask: "Are their editors using Brand Kit or the AI assistant to draft content? Roughly how often?"

## UC6 — Real-time personalization
**Component:** Personalize. **Evidence:** none in Claude yet (no Personalize usage data anywhere), so this is
**per CSM** in v1. Ask: "Is Personalize live? How many experiences are running, and on which pages?"

## UC7 — Experimentation
**Component:** Personalize A/B tests. **Evidence:** none in Claude yet, so this is **per CSM** in v1.
Ask: "Have they run an A/B test this year? Did they act on the result?"

## UC8 — Unified customer profile
**Component:** Lytics (Data Cloud). **Evidence:** known profiles by month, inbound events by month, custom streams
(data sources).
Known profiles are compared over the last 3 complete months; inbound events over the last 2 complete months (month
on month).
- **Strong**: known profiles above zero and flat or growing over 3 months, AND inbound events flat or growing month on
  month, AND 3 or more custom streams.
- **Weak**: 0 known profiles on a Lytics account that's sending events (nothing is being identified), OR known
  profiles down more than 20% over 3 months, OR inbound events down more than 30% month on month. Sanity-check sudden
  cliffs (a reload can look like a collapse) before calling Weak on a cliff alone.
- **Unknown**: no Lytics account linked to this customer.

## UC9 — Audience activation
**Component:** Lytics audiences + jobs (exports to ads, email, warehouse). **Evidence:** audiences, jobs. Job counts
mix imports and exports, so confirm exports with the CSM before calling Strong.
- **Strong**: 44 or more audiences AND 25 or more jobs.
- **Weak**: fewer than 6 audiences OR fewer than 4 jobs while events are still flowing ("data in, nothing out").
- **Unknown**: no Lytics account linked.

## UC10 — Journey orchestration
**Component:** Lytics Flows / Journey Orchestrations. Flows is a preview, enabled on request: check before treating
"no flows" as a gap. **Evidence:** flows, running flows, average steps per flow.
- **Strong**: 1 or more running flows with 2 or more steps on average.
- **Weak**: flows built but 0 running.
- **Unknown**: no Lytics account linked, or Flows not enabled on the account. 0 flows on an owned Lytics account is
  Unknown, not a gap: ask the CSM whether Flows is enabled.

## UC11 — Behavioral and predictive insight
**Component:** Lytics scores and lookalike models. **Evidence:** behavior-score audiences, lookalike models, healthy
lookalike models.
- **Strong**: 1 or more healthy lookalike models AND 10 or more behavior-score audiences.
- **Weak**: lookalike models exist but none healthy, OR 0 behavior-score audiences on an account with 44 or more
  audiences (scores exist but nobody uses them).
- **Unknown**: no Lytics account linked.
