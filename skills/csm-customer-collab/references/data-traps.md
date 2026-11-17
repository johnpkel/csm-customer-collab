# Data traps

Each of these has produced a wrong answer at least once. Check this list before stating any number.

## Lytics usage tool
- **Vague words silently drop filters.** "Few export jobs" returned the top accounts with no job filter at all.
  Always use numbers ("4 or fewer jobs", "at least 1 million events in the last 30 days"), and read its "This is our
  interpretation" line.
- **No contract caps or entitlements.** Asking for usage and a cap in one question makes it refuse the whole thing.
  Caps come from the order form or the CSM.
- **Production isn't always a customer.** Thousands of production accounts are trials or mislabelled dev accounts.
  Filter by the linked Salesforce Account Id.
- **Customers have several Lytics accounts**, and most sub-accounts are empty. Roll up by Salesforce Account Id;
  per-account numbers mislead.
- **Feature counts are today's snapshot only.** There is no history, so "audiences went down" can't be claimed from
  them.
- **Job counts mix imports and exports** and carry no status. Confirm exports with the CSM.
- **Known profiles are a monthly peak.** October 2025 is backfill; daily data starts 10 Nov 2025. Sanity-check sudden
  cliffs before calling a collapse.
- **Events don't predict churn.** Churned accounts kept sending events to the end. Adoption (audiences, jobs, flows,
  logins) carries the signal.
- Sometimes the tool returns only SQL. Run it with the Snowflake SQL tool.

## CMS usage
- **No "entries published" metric.** Asking for one makes the product usage tool refuse. Use CMA API calls as the
  authoring proxy.
- **Known-bad dates:** 29 Jul–21 Sep 2026 (missing API keys) and 1 Jul–30 Sep 2026 (bandwidth spikes). Don't trend
  across them.
- Name matching (`ILIKE '%name%'`) pulls in other companies' orgs. Join on the Salesforce Account Id.

## Personalize, Brand Kit, AI
- **No usage data anywhere in Claude** for Personalize, Brand Kit or AI credits. These use cases are per CSM in v1,
  and "no data" is Unknown, never Weak.

## Health Index
- The composite can look fine while the CSM pulse is red (a red-pulse account scored 62 in Nov 2026). Always read
  `CSM_Pulse__c` alongside it.
- Some accounts aren't scored. Use `CSM_Pulse__c` then.
- A component score of 0 can mean "no data" rather than "bad". For example, case stability can read 0 with no open
  cases. Check the source (open cases in Salesforce) before quoting a 0 component as a negative.

## Salesforce
- `SBQQ__Subscription__c` is not readable. Ownership comes from closed-won `OpportunityLineItem`.
- Bundle components are often $0 "Included" lines. Don't filter ownership by price.
- `CS_Manager__c` is a User Id. Read `CS_Manager__r.Name`.
- `Opportunity.Amount` is not ARR. Use `Current_ARR__c` for ARR.
- A CSM's Salesforce profile may not see line items. If so, use the fallback in `signals.md`.

## Gong
- The Gong tool returns calls from **other** accounts when the asked-for account has none (for example, a sister
  brand's calls). Use only calls tagged to this account; no calls = Unknown.

## Don't claim
Never say or write these, to the CSM or in anything built for the customer:
- That Lytics is an AI decisioning engine today (decisioning and Adaptive Journeys are direction, not product).
- That ad audiences update instantly, or that match rates are guaranteed.
- That Flows is generally available: it's a preview, enabled on request. Check the account first.
- Any roadmap or GA date.

Also never: prices, discounts or quotes; unreleased features; anything the customer hasn't been told about another
customer.
