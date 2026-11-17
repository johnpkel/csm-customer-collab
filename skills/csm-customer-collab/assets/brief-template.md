# {{customer}}: account brief, {{date}}

**CSM:** {{csm}} · **Designation:** {{designation}} · **ARR:** {{arr}} · **Renewal:** {{renewal}} ·
**Pulse:** {{pulse}} · **Health:** {{health}}

> {{at_risk_line}}
<!-- Only if the red rule fired: "At risk: we earn the right before any DXP conversation." Otherwise delete this line. -->

**Changes since last brief:** {{changes}}
<!-- "First brief." on a first run. Otherwise: calls that moved, signals that appeared or cleared, last NBA done or not. -->

## Signals
**Positive**
- {{id}} {{signal}} ({{source}}, {{date}})

**Negative**
- {{id}} {{signal}} ({{source}}, {{date}})

## Use cases
| Use case | Call | Evidence | Source / date | CSM input |
|---|---|---|---|---|
| UC<n> <name> | Strong / Weak / Unknown / Developing | {{numbers}} | {{source, date}} | {{per CSM, or blank}} |

**Not in use (DXP gaps):** {{UC list with components}}

## Value delivered
- **Evidenced:** {{numbers + source}}
- **Claimed (per CSM):** {{what the customer would say}}
- **Missing:** {{what we can't show yet}}

## DXP gap
- **Owns:** {{components}} ({{per Salesforce | per CSM}})
- **Missing:** {{components}}
- **Archetype:** {{Content Cloud | Lytics CDP Only | Content + Data Cloud}}
- **Next DXP step:** {{step and why, or "None this round: earn the right first; later, once <weak use case> is fixed"}}

## Next best action
**{{one action}}**. Owner: {{name or role}}. By: {{date}}.

## Where from here
- **Customer:** {{2–3 lines}}
- **CSM:** {{2–3 lines}}

## Discovery questions
1. {{question, phrased for the customer}}
   *A good answer tells us:* {{what}}
<!-- 4–5 questions in total. -->

## Sources
- {{source}}: {{what was read}}, {{date}}
- Unavailable: {{source}}: {{why}}
- Interview: {{csm}}, {{date}} ({{questions skipped, if any}})
