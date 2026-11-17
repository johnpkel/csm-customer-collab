"""Structural and rule checks for the csm-customer-collab skill. Stdlib only: python3 -m unittest -v"""
import re
import subprocess
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "csm-customer-collab"
SKILL_FILES = ("SKILL.md", "references/use-cases.md", "references/signals.md", "references/dxp-bundle.md",
               "references/data-traps.md", "assets/brief-template.md", "assets/meeting-brief.html")


def read(rel: str) -> str:
    return (SKILL_DIR / rel).read_text(encoding="utf-8")


def flat(rel: str) -> str:
    """The file with all whitespace runs collapsed, so wrapped prose matches one-line patterns."""
    return re.sub(r"\s+", " ", read(rel))


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def skill_texts():
    for p in SKILL_DIR.rglob("*"):
        if p.is_file() and p.name != ".DS_Store":
            yield p, p.read_text(encoding="utf-8")


class SkillStructure(unittest.TestCase):
    def test_frontmatter(self):
        fm = frontmatter(read("SKILL.md"))
        self.assertEqual(fm.get("name"), "csm-customer-collab")
        self.assertLessEqual(len(fm["description"]), 1024)
        for phrase in ("help me with", "collaborate with me on"):
            self.assertIn(phrase, fm["description"].lower())

    def test_all_files_exist_and_are_linked(self):
        body = read("SKILL.md")
        for rel in SKILL_FILES[1:]:
            self.assertTrue((SKILL_DIR / rel).stat().st_size > 0, rel)
            self.assertIn(rel, body)

    def test_no_hardcoded_tool_ids(self):
        for p, text in skill_texts():
            self.assertNotIn("mcp__", text, p.name)

    def test_no_customer_names(self):
        names_file = ROOT / "tests" / "banned-names.txt"
        if not names_file.exists():
            self.skipTest("tests/banned-names.txt not present (it is local-only)")
        names = [n.strip() for n in names_file.read_text().splitlines() if n.strip()]
        banned = re.compile("|".join(re.escape(n) for n in names), re.I)
        for p, text in skill_texts():
            self.assertIsNone(banned.search(text), p.name)


class References(unittest.TestCase):
    def test_catalogue_has_eleven_use_cases_mapped_to_components(self):
        uc = read("references/use-cases.md")
        self.assertEqual(len(re.findall(r"^## UC(\d+) — ", uc, re.M)), 11)
        for name in ("Content operations at scale", "Omnichannel delivery", "Front-end hosting",
                     "Workflow automation", "On-brand AI content", "Real-time personalization",
                     "Experimentation", "Unified customer profile", "Audience activation",
                     "Journey orchestration", "Behavioral and predictive insight"):
            self.assertIn(name, uc)

    def test_data_backed_use_cases_have_written_tests(self):
        uc = read("references/use-cases.md")
        for n in (1, 2, 3, 4, 8, 9, 10, 11):
            section = re.search(rf"^## UC{n} — .*?(?=^## UC|\Z)", uc, re.M | re.S).group(0)
            for label in ("**Strong**", "**Weak**", "**Unknown**"):
                self.assertIn(label, section, f"UC{n} missing {label}")

    def test_interview_only_use_cases_say_per_csm(self):
        uc = read("references/use-cases.md")
        for n in (5, 6, 7):
            section = re.search(rf"^## UC{n} — .*?(?=^## UC|\Z)", uc, re.M | re.S).group(0)
            self.assertIn("per CSM", section, f"UC{n}")

    def test_unknown_is_never_weak(self):
        self.assertRegex(read("references/use-cases.md"), r"(?i)missing (data|source).*Unknown.*never.*Weak")

    def test_dxp_bundle(self):
        d = read("references/dxp-bundle.md")
        for s in ("EDGE X1", "EDGE X3", "EDGE X5", "Grow DXP", "Scale DXP", "Launch", "Personalize",
                  "Automate", "Brand Kit", "Journey Orchestrations", "Inbound Events", "AI Credits", "Agent OS BYOK"):
            self.assertIn(s, d)
        self.assertRegex(d, r"(?is)adoption.*add-on.*edition")
        self.assertRegex(d, r"(?i)red health|renewal at risk")

    def test_dont_claim_verbatim(self):
        t = read("references/data-traps.md")
        for line in ("That Lytics is an AI decisioning engine today",
                     "That ad audiences update instantly, or that match rates are guaranteed.",
                     "That Flows is generally available: it's a preview, enabled on request.",
                     "Any roadmap or GA date."):
            self.assertIn(line, t)

    def test_signals_cover_every_source(self):
        s = read("references/signals.md")
        for src in ("Salesforce", "Lytics usage", "CMS usage", "Health Index", "Gong"):
            self.assertIn(src, s)
        self.assertIn("## Positive", s)
        self.assertIn("## Negative", s)


class Flow(unittest.TestCase):
    def body(self):
        text = read("SKILL.md")
        return text.split("---", 2)[2] if text.startswith("---") else text

    def test_steps_in_order(self):
        b = self.body()
        marks = ["Resolve the account", "What I found", "Signals", "Use cases", "Interview",
                 "Synthesis", "Discovery questions", "artifact", "Save"]
        pos = [b.find(m) for m in marks]
        self.assertTrue(all(p >= 0 for p in pos), dict(zip(marks, pos)))
        self.assertEqual(pos, sorted(pos), dict(zip(marks, pos)))

    def test_four_interview_areas(self):
        b = self.body().lower()
        for a in ("strong or weak", "value", "next best action", "where the customer and"):
            self.assertIn(a, b)
        self.assertIn("one question at a time", b)
        self.assertIn("skip", b)

    def test_guardrails(self):
        b = self.body()
        self.assertRegex(b, r"(?i)earn the right")
        self.assertRegex(b, r"(?i)never.*(publish|upload)")
        self.assertRegex(b, r"(?i)no pricing|never.*pric")
        self.assertRegex(b, r"(?i)several (accounts )?match")
        self.assertRegex(b, r"(?i)unavailable|not connected")
        self.assertIn('/ \\ : * ? " < > |', b)
        self.assertRegex(b, r"(?is)newest.*brief.*what changed")
        self.assertIn("-2", b)
        self.assertIn("4–5", b)

    def test_save_paths(self):
        b = self.body()
        self.assertIn("Customer Briefs/<Customer>/<YYYY-MM-DD>-brief.md", b)
        self.assertIn("~/Documents/Customer Briefs/", b)


SECTIONS = ["Signals", "Use cases", "Value delivered", "DXP gap", "Next best action",
            "Where from here", "Discovery questions", "Sources"]


class Assets(unittest.TestCase):
    def test_template_sections(self):
        t = read("assets/brief-template.md")
        for s in SECTIONS:
            self.assertIn(f"## {s}", t)
        for ph in ("{{customer}}", "{{date}}", "{{csm}}"):
            self.assertIn(ph, t)
        self.assertIn("Changes since last brief", t)

    def test_html_is_self_contained_and_printable(self):
        h = read("assets/meeting-brief.html")
        self.assertNotRegex(h, r"<script[^>]+src=")
        self.assertNotRegex(h, r"https?://(?!fonts\.googleapis\.com|fonts\.gstatic\.com)")
        self.assertIn("@media print", h)
        self.assertIn("@page", h)
        for s in ("Signals", "Use cases", "Next best action", "Discovery questions"):
            self.assertIn(s, h)
        self.assertIn("#AC75FF", h.upper())
        self.assertIn("{{customer}}", h)


class Package(unittest.TestCase):
    def test_zip_contains_exactly_the_skill(self):
        out = subprocess.run(["bash", str(ROOT / "scripts" / "package.sh"), "--no-tests"],
                             cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        z = ROOT / "dist" / "csm-customer-collab.zip"
        with zipfile.ZipFile(z) as zf:
            files = sorted(n for n in zf.namelist() if not n.endswith("/"))
        self.assertEqual(files, sorted(f"csm-customer-collab/{f}" for f in SKILL_FILES))


class DryRunFixes(unittest.TestCase):
    """Each test pins a finding from the 16 Nov dry runs (three real accounts plus edge cases)."""

    def test_brief_lookup_matches_same_day_reruns(self):          # bug: *-brief.md missed -brief-2.md
        b = read("SKILL.md")
        self.assertIn("*-brief*.md", b)
        self.assertNotRegex(b, r"`\*-brief\.md`")
        self.assertRegex(b, r"(?i)both .*folders|either location")

    def test_p7_is_not_a_renewal_uplift(self):                    # P7 fired on renewal priced above ARR
        s = read("references/signals.md")
        self.assertNotIn("amount above current ARR", s)
        self.assertIn("RNW", s)

    def test_line_items_include_product_code(self):               # editions only identifiable by code
        self.assertIn("Product2.ProductCode", read("references/signals.md"))

    def test_ownership_rules_are_explicit(self):                  # "has it" ambiguous; UC5–7 when not owned
        b = read("SKILL.md")
        self.assertRegex(b, r"(?i)usage without a line item")
        self.assertRegex(b, r"(?i)not owned.*DXP gap")
        self.assertRegex(b, r"(?i)ParentId")

    def test_lytics_only_next_step_is_single(self):               # two rules gave two answers
        d = read("references/dxp-bundle.md")
        line = next(l for l in d.splitlines() if "**Lytics CDP Only**" in l)
        self.assertIn("Personalize", line)

    def test_inbound_events_shows_data_cloud_ownership(self):
        d = read("references/dxp-bundle.md")
        row = next(l for l in d.splitlines() if l.startswith("| Data Cloud"))
        self.assertIn("Inbound Events", row)

    def test_uc8_windows_and_zero_profiles(self):
        uc = read("references/use-cases.md")
        self.assertIn("0 known profiles", uc)
        self.assertRegex(uc, r"(?i)last 2 complete months")

    def test_n5_covers_near_idle(self):
        self.assertRegex(flat("references/signals.md"), r"(?i)N5.*below .*Weak line")

    def test_skipped_question_in_synthesis(self):
        self.assertRegex(read("SKILL.md"), r"(?i)skipped.*inferred")

    def test_folder_name_edge_cases(self):
        b = read("SKILL.md")
        self.assertRegex(b, r"(?i)collapse repeated dashes")
        self.assertRegex(b, r"(?i)empty.*Account Id")

    def test_soql_name_safety(self):
        b = read("SKILL.md")
        self.assertIn("O\\'Brien", b)                                # SOQL escapes with a backslash
        self.assertNotIn("O''Brien", b)
        self.assertRegex(b, r"(?i)10 rows.*more")

    def test_customer_facing_artifacts_have_no_commercials(self):
        self.assertRegex(read("SKILL.md"), r"(?i)email draft.*no (ARR|opportunit)")

    def test_case_stability_trap(self):
        self.assertRegex(read("references/data-traps.md"), r"(?i)case.stability")


class FinalReviewFixes(unittest.TestCase):
    """Each test pins an Important finding from the final review or the second dry run on the same account."""

    def test_soql_wildcards_escaped(self):
        self.assertIn("\\%", read("SKILL.md"))

    def test_no_salesforce_id_means_name_match_labelled(self):
        self.assertRegex(flat("references/signals.md"), r"(?i)no Account Id.*matched by name")

    def test_red_rule_reapplied_after_interview(self):
        b = read("SKILL.md")
        self.assertRegex(b, r"(?i)apply the red rule again")
        self.assertRegex(b, r"(?i)CSM.*renewal (risk|is at risk)")

    def test_unscored_health_blocks_dxp_step(self):
        self.assertRegex(flat("references/signals.md"), r"(?i)health is Unknown.*ask the CSM")

    def test_dxp_bundle_defers_to_single_red_rule(self):
        d = read("references/dxp-bundle.md")
        self.assertIn("red rule in `signals.md`", d)
        self.assertNotIn("health in the bottom 10%", d)

    def test_never_published_as_artifact(self):
        self.assertRegex(read("SKILL.md"), r"(?i)never .*Artifact")

    def test_artifacts_never_overwritten(self):
        self.assertRegex(read("SKILL.md"), r"(?i)artifact files? (follow|use|get) the same .*suffix")

    def test_zero_flows_is_unknown_and_flows_never_the_step(self):
        uc = flat("references/use-cases.md")
        sec = re.search(r"## UC10 — .*?(?=## UC11|\Z)", uc).group(0)
        self.assertRegex(sec, r"(?i)0 flows.*Unknown")
        self.assertRegex(flat("references/dxp-bundle.md"), r"(?i)never name (Flows|Journey Orchestrations)")

    def test_at_risk_talk_track_asks_for_recovery(self):
        self.assertRegex(flat("SKILL.md"), r"(?i)at risk.*the ask is")

    def test_usage_means_activity(self):
        self.assertRegex(read("SKILL.md"), r"(?i)usage means activity")

    def test_adoption_is_the_action_not_the_dxp_step(self):
        self.assertRegex(flat("references/dxp-bundle.md"), r"(?i)adoption .*next best action.*DXP step")

    def test_n5_counts_included_components(self):
        self.assertRegex(read("references/signals.md"), r"(?i)N5.*\n?.*included")


if __name__ == "__main__":
    unittest.main()


class PublicPlugin(unittest.TestCase):
    """The public repo is a Claude plugin marketplace: paste the URL into Add marketplace, or run two commands."""
    REPO = "johnpkel/csm-customer-collab"

    def test_marketplace_manifest(self):
        import json
        m = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        self.assertTrue(m["name"] and m["owner"]["name"])
        self.assertEqual([p["name"] for p in m["plugins"]], ["csm-customer-collab"])
        self.assertEqual(m["plugins"][0]["source"], "./")

    def test_plugin_manifest(self):
        import json
        p = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(p["name"], "csm-customer-collab")
        self.assertRegex(p["version"], r"^\d+\.\d+\.\d+$")

    def test_skill_sits_where_plugins_look(self):
        self.assertEqual(SKILL_DIR, ROOT / "skills" / "csm-customer-collab")
        self.assertEqual(frontmatter(read("SKILL.md"))["name"], SKILL_DIR.name)
        self.assertFalse((ROOT / "SKILL.md").exists())

    def test_readme_gives_every_install_route(self):
        r = re.sub(r"\s+", " ", (ROOT / "README.md").read_text())
        self.assertIn("Add marketplace", r)
        self.assertIn(f"claude plugin marketplace add {self.REPO}", r)
        m = __import__("json").loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        self.assertIn(f"claude plugin install csm-customer-collab@{m['name']}", r)
        self.assertIn("If you are Claude", r)

    def test_no_internal_build_notes_in_public_repo(self):
        self.assertFalse((ROOT / "docs").exists())
        self.assertFalse((ROOT / "skill").exists())

    def test_no_customer_names_anywhere(self):
        # The names live in an untracked local file so the public repo never lists them.
        names_file = ROOT / "tests" / "banned-names.txt"
        if not names_file.exists():
            self.skipTest("tests/banned-names.txt not present (it is local-only)")
        names = [n.strip() for n in names_file.read_text().splitlines() if n.strip()]
        banned = re.compile("|".join(re.escape(n) for n in names), re.I)
        tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
        for rel in tracked:
            if rel == "tests/banned-names.txt" or rel.endswith(".zip"):
                continue
            text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
            self.assertIsNone(banned.search(text), rel)
