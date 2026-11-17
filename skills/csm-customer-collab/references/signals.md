# Evidence queries and signals

Run every source you can reach, in parallel where possible. Find each tool by what it does: the **Salesforce SOQL
tool**, the **Snowflake SQL tool** (runs SQL), the **Lytics usage tool**, the **product usage tool**, the **stack usage
tool**, the **customer health tool**, the **Gong transcript tool**. If a tool isn't connected, write "Not connected"
for that source in "What I found" and move on. Never stall.

`<ID>` below is the 18-character Salesforce Account Id from step 0. Join on it, not on the account name: name
matching pulls in other companies. If Salesforce isn't connected there is no Account Id: ask the plain-language usage
tools by the exact customer name, label every number "matched by name: verify with CSM", and if more than one company
comes back, mark that source Unknown.

## Salesforce

**Account:**
```sql
SELECT Id, Name, ParentId, Customer_Designation__c, CSM_Pulse__c, Current_ARR__c, License_End_Date__c,
       CS_Manager__r.Name, Success_Tier__c, Account_Plan_URL__c,
       (SELECT Priority, Status, CreatedDate FROM Cases WHERE IsClosed = false ORDER BY CreatedDate LIMIT 20),
       (SELECT Name, StageName, Amount, CloseDate, Type FROM Opportunities WHERE IsClosed = false LIMIT 10)
FROM Account WHERE Id = '<ID>'
```

**What they own:** closed-won line items over the last 3 years. Keep the $0 "Included" lines: bundle components are
often priced at zero.
```sql
SELECT Product2.Family, Product2.Name, Product2.ProductCode, MAX(Opportunity.CloseDate) last_close
FROM OpportunityLineItem
WHERE Opportunity.AccountId = '<ID>' AND Opportunity.IsWon = true AND Opportunity.CloseDate = LAST_N_YEARS:3
GROUP BY Product2.Family, Product2.Name, Product2.ProductCode ORDER BY Product2.Family LIMIT 200
```
Map the families to components with `dxp-bundle.md`. A DXP edition shows only in `ProductCode` (`DXP_TIER_X1/X3/X5…`);
a code like `TIER_X5` without `DXP` is a CMS edition, not DXP. Use the latest close date per family, because older
lines may have been dropped at renewal. If this account has no line items but has a `ParentId`, run the same query
on the parent and label the result "per parent account".

**Fallback:** if the line-item query errors or returns nothing, use `Customer_Designation__c` for the archetype
(Content Cloud / Lytics CDP Only / Content + Data Cloud) and ask the CSM which products the customer owns. Mark the
DXP gap **per CSM**. `SBQQ__Subscription__c` is not readable, so don't try it.

## CMS usage
This covers CMS, Launch and Automate, by month or in 30-day windows. Run it with the Snowflake SQL tool:
```sql
SELECT IFF(date >= DATEADD(day,-30,CURRENT_DATE),'last_30','prior_30') win,
       MAX(users) users, MAX(stacks) stacks, MAX(entries) entries, MAX(locales) locales, MAX(environments) envs,
       SUM(cma_count) cma_calls, SUM(total_api_count) api_calls,
       SUM(automation_total_executions) automate_execs, SUM(automation_execution_errors) automate_errors,
       MAX(total_automations) automations, MAX(total_launch_projects) launch_projects,
       SUM(total_launch_deployment_count) launch_deploys
FROM DBT_PROD.MARTS.FCT_ORG_DAILY_PRODUCT_USAGE
WHERE account_id = '<ID>' AND date >= DATEADD(day,-60,CURRENT_DATE)
GROUP BY 1
```
With no SQL tool, ask the product usage tool in numbers: "For customer account <Name>, for the last 30 days and the 30
days before: max users, stacks, locales; total CMA API calls; total API calls; automation executions; Launch projects
and deployments." Don't ask for "entries published", because that metric doesn't exist and the tool refuses. If a
usage tool answers with SQL only, run that SQL with the Snowflake SQL tool.

## Lytics usage
Use this only if the designation includes Lytics or Data Cloud. Customers often have several Lytics accounts, so
always roll them up by Salesforce Account Id.
```sql
SELECT COUNT(*) lytics_accounts, SUM(u.audience_count) audiences, SUM(u.job_count) jobs,
       SUM(u.flow_count) flows, SUM(u.running_flow_count) running_flows, AVG(NULLIF(u.avg_steps_per_flow,0)) avg_steps,
       SUM(u.lookalike_model_count) lookalikes, SUM(u.healthy_lookalike_model_count) healthy_lookalikes,
       SUM(u.behavior_score_audience_count) score_audiences, SUM(u.custom_stream_count) custom_streams,
       MIN(u.days_since_last_ui_login) days_since_login
FROM DBT_PROD.MARTS.FCT_LYTICS__ACCOUNT_USAGE_CURRENT u
JOIN DBT_PROD.MARTS.DIM_LYTICS_ACCOUNT a ON a.aid = u.aid
WHERE a.salesforce_account_id = '<ID>' AND a.account_type = 'production' AND NOT COALESCE(a.is_deleted, FALSE)
```
For the trends, ask the Lytics usage tool with exact numbers and windows, one metric per question:
- "Inbound events per month for production Lytics accounts linked to Salesforce account <Name>, for the last 4 complete months."
- "Known profiles at the end of each of the last 4 complete months for production Lytics accounts linked to Salesforce account <Name>."

Read its "This is our interpretation" line each time. If a filter you asked for is missing, the answer is wrong.

## Health Index
```sql
SELECT week_start_date, operational_health_score,
       GET_PATH(usage_metadata,'momentum.score')::DOUBLE momentum, GET_PATH(usage_metadata,'breadth.score')::DOUBLE breadth,
       GET_PATH(engagement_metadata,'csm_pulse.score')::DOUBLE pulse, GET_PATH(engagement_metadata,'gong_sentiment.score')::DOUBLE gong,
       GET_PATH(support_metadata,'case_stability.score')::DOUBLE cases
FROM DBT_PROD.MARTS.FCT_HEALTH_INDEX_OPERATIONAL_V2 WHERE account_id = '<ID>'
ORDER BY week_start_date DESC LIMIT 5
```
The composite runs 0–100. On 9 Nov 2026 the 10th percentile was 45, the 25th was 61 and the median 74. Component
scores run 0–1. If the account isn't scored, use `CSM_Pulse__c`. If there's no composite and no pulse either, health
is Unknown, not fine: ask the CSM about the relationship and renewal before naming any DXP step (SKILL.md Step 5).

## Gong
Use whichever Gong tool is connected (a Snowflake Gong search or a Gong connector). Ask it: "Calls tagged to the account <Name> in the last 90 days: main themes, asks,
complaints or risks, competitors named, and champions, each with the call date. 8 bullets maximum." Use background
mode if it offers one.
- If it returns calls from **other** accounts, don't use them. A related or parent account (`ParentId`) is worth one
  more search, labelled as the parent's.
- If there are no calls tagged to the account, Gong is **Unknown** and goes in the "missing" line.

---

## Positive
Each signal carries its source and date.
- **P1** `CSM_Pulse__c` = "Healthy (Green)".
- **P2** Health composite 74 or above (median or better), or rising for 3 weeks in a row.
- **P3** Usage growing: CMA calls, API calls, events or known profiles up 10% or more on the prior window.
- **P4** Breadth: 3 or more use cases Strong.
- **P5** Executive champion or sponsor named on a call in the last 90 days.
- **P6** Renewal more than 12 months away.
- **P7** An open expansion opportunity: any open opportunity that isn't the renewal. The renewal usually has "RNW"
  or "Renewal" in its name; a renewal priced above ARR is an uplift, not expansion. Don't compare `Amount` to ARR.
- **P8** Recent login: last Lytics UI login 7 or fewer days ago.

## Negative
- **N1** `CSM_Pulse__c` = "Concerning (Yellow)". **N1R** = "Poor (Red)".
- **N2** Health composite under 61 (bottom quarter). **N2R** = under 45 (bottom 10%).
- **N3** Usage falling: CMA calls, API calls, events or known profiles down 30% or more.
- **N4** Data in, nothing out: events flowing but fewer than 4 jobs, or audiences built but nothing exported.
- **N5** Owned but idle: a component on the line items (including $0 bundle-included lines) with zero usage, or usage
  below its use case's Weak line (for example, Launch projects but 0 deploys, or 2 Automate executions in 30 days).
- **N6** P1/P2 cases open, or any case open more than 180 days.
- **N7** A competitor named on a call in the last 90 days.
- **N8** Renewal in under 6 months (`License_End_Date__c`). **N8R** = under 90 days.
- **N9** No Lytics UI login for 30 or more days (134 or more is the bottom quarter).

## The red rule ("earn the right")
The account is **at risk** if any of these hold: **N1R**; **N2R**; **N8R** together with N1 or N1R; or the CSM
says in the interview that the renewal is at risk, a competitor is being evaluated, or the relationship is in trouble.
When it's at risk, the next best action is value recovery, and the DXP step waits. Say this plainly at the top of the
synthesis. Renewal timing alone (N8 or N8R without a Yellow or Red pulse) is not enough.
