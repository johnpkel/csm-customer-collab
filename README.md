# CSM customer collaboration skill

A Claude skill for Contentstack Customer Success Managers. Say **"help me with [customer]"** and Claude:

1. pulls the evidence (Salesforce, product and Lytics usage, the Health Index, Gong) and shows positive and negative
   signals;
2. calls each use case Strong, Weak or Unknown, with the number and source behind each call;
3. asks you a few questions, one at a time, about value, the next best action, and where the customer is heading;
4. names the gap to DXP and the next step across it, unless the account is at risk, where recovery comes first;
5. gives you 4–5 discovery questions for your next customer meeting, and offers a one-page meeting brief, talk track
   or email draft;
6. saves a dated brief on your machine. Nothing is written to Salesforce or any shared system.

## Install

### Claude Desktop or claude.ai (most CSMs)
1. Open **Customize › Plugins › Add › Add marketplace**.
2. Paste this repo's link: `https://github.com/johnpkel/csm-customer-collab`
3. Install the **csm-customer-collab** plugin from that marketplace.

No GitHub account is needed: the repo is public.

**Alternative (skill upload):** download `csm-customer-collab.zip` from this repo's
[latest release](https://github.com/johnpkel/csm-customer-collab/releases/latest), then go to
**Customize › Skills › + › Create skill › Upload a skill** and upload the zip as it is (don't unzip it).

### Claude Code
```bash
claude plugin marketplace add johnpkel/csm-customer-collab
```
```bash
claude plugin install csm-customer-collab@csm-skills
```

## Use it
1. Turn on the **Salesforce** and **Snowflake** connectors in Claude. Without them the skill still runs, but it marks
   what it can't see as Unknown and leans on your answers.
2. In Claude Desktop, choose a working folder (for example `Documents/CSM`). Briefs are saved there, under
   `Customer Briefs/<Customer>/`. Without a working folder they go to `~/Documents/Customer Briefs/`.
3. Say **"help me with <customer>"**, "collaborate with me on <customer>" or "prep me for <customer>".

## If you are Claude
A user gave you this link and asked you to install the skill. What you can do depends on where you are running:
- **Claude Code with a shell:** run the two `claude plugin` commands under "Claude Code" above, then tell the user
  to start a new session (or run `/reload-plugins`) and say "help me with <customer>".
- **Claude Desktop, Cowork or claude.ai:** you can't install plugins yourself. Give the user the three steps under
  "Claude Desktop or claude.ai" above, with this repo's link to paste.

Don't copy the skill's text into the chat as a substitute for installing it: it only triggers on "help me with
[customer]" once installed.

## Maintainers
- The skill lives in `skills/csm-customer-collab/`; the plugin and marketplace manifests are in `.claude-plugin/`.
- Test: `python3 -m unittest -v tests.test_skill` (stdlib only). Build the upload zip with `./scripts/package.sh`,
  which runs the tests first and writes `dist/csm-customer-collab.zip`.
- To release a change, bump `version` in `.claude-plugin/plugin.json`, then attach the new zip to a GitHub release.
  Plugin installs update from the repo; zip uploads must be re-uploaded.
- Keep customer names and customer data out of this repo: it's public. The customer-name check reads a local-only
  `tests/banned-names.txt` (git-ignored).
