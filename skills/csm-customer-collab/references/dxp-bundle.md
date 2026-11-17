# DXP bundle: what it contains and how to find the gap

DXP is the full Contentstack bundle. The skill's job is to name the gap between what the customer owns and DXP, and
the next step across it. It never prices that step: Sales and Deal Desk do pricing.

## Editions
| Edition | CPQ product code | Notes |
|---|---|---|
| EDGE X1 DXP | `DXP_TIER_X1` / `DXP_TIER_X1_BUNDLE` | Entry tier. Component list: verify in CPQ. |
| EDGE X3 DXP | `DXP_TIER_X3` / `DXP_TIER_X3_BUNDLE` | Required components below (from the CPQ bundle options). |
| EDGE X5 DXP | `DXP_TIER_X5` / `DXP_TIER_X5_BUNDLE` | Top tier. Component list: verify in CPQ. |
| Grow DXP Edition | n/a | Verify components in CPQ. |
| Scale DXP Edition | n/a | Step up from Grow. |

Edition step-ups run **EDGE X1 → EDGE X3 → EDGE X5** and **Grow DXP → Scale DXP**.

## Required components (EDGE X3 DXP bundle)
| Component | Line-item families that show ownership | Use cases |
|---|---|---|
| CMS (stacks, entries, content types, languages, roles, users, branches, storage, bandwidth, developer stacks) | Stacks, Content Entries, Content Types, Languages, Roles, Branches, Storage, Bandwidth, API Calls | UC1, UC2 |
| Launch (hosting + projects) | Launch | UC3 |
| Automate (25,000 executions) | Automate | UC4 |
| Brand Kit | Brand Kit | UC5 |
| Personalize Engine | Personalize | UC6, UC7 |
| Journey Orchestrations (included) | Journey Orchestrations, or Lytics / Data Cloud lines | UC10 |
| Data Cloud data retention (12 months) | Lytics / Data Cloud / Real-Time CDP lines, or Inbound Events (M) (event volume is only sold with Data Cloud) | UC8, UC9, UC11 |
| SSO / SCIM | Security Bundle | none |
| 24/7 support | Support | none |

A customer with a **DXP edition line item** owns all of its required components, even with no separate line for
each. A customer with the **component lines** but no edition line owns those components only.

## Optional add-ons
- **Inbound Events (M)**: Data Cloud event volume.
- **AI Credits**: for Brand Kit and AI features.
- **Agent OS BYOK**: Agent OS with the customer's own model key.
- Lytics setup services.

## Archetypes (`Customer_Designation__c`)
- **Content Cloud**: CMS, perhaps Launch and Automate. The usual gap is Personalize and Data Cloud.
- **Lytics CDP Only**: Data Cloud only. The next DXP step is **Personalize**: it puts the audiences they already
  build to work on their own site, whatever CMS they run. The full CMS platform is the step after that, a longer
  conversation, so name it under "where from here", not as the next step.
- **Content + Data Cloud**: closest to DXP. The gap is usually components owned but unused, or one missing piece.

## Gap order: what to recommend first
1. **Adoption first.** Components they own but don't use (no usage, or a Weak call). Fixing these comes before any
   sale, because an idle component is a renewal risk, not an upsell. Adoption work is the next best action; the DXP
   step is then named as "<step>, once <the weak use case> is Strong", not dropped.
2. **Add-ons.** Inbound Events, AI Credits, Agent OS BYOK, where usage shows the need (for example, events near the
   contracted volume, or heavy AI use).
3. **Edition step-up.** X1 → X3 → X5, or Grow → Scale, once the owned components are Strong.

For customers who don't own DXP, the **next DXP step** follows from their strongest use case. Examples:
- A strong unified profile with no Personalize: Personalize is the step.
- Strong content operations with no Launch: Launch is the step.
- Strong Personalize with no Data Cloud: Data Cloud is the step (real profiles behind the variants).

Never name Flows or Journey Orchestrations as the next DXP step: Flows is a preview, enabled on request. Mention it
only if the CSM confirms it's enabled on the account.

## Red health overrides the gap order
If the account is at risk per the red rule in `signals.md`, there is **no DXP step this round**. The next best action is value recovery on what they already own; name the DXP step only as "later, once
<the weak use case> is fixed".
