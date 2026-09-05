#!/usr/bin/env python3
"""Tests for validate_content.py: each breaks one thing and expects the checker to notice.

    python3 scripts/test_validate_content.py    # also runs on every pull request
"""
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".

import copy
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml  # noqa: E402

import validate_content as vc  # noqa: E402

REAL_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ValidatorTestCase(unittest.TestCase):
    """Each test works on a throwaway copy of the repo data."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        shutil.copytree(os.path.join(REAL_REPO, "_data"), os.path.join(self.tmp, "_data"))
        shutil.copytree(os.path.join(REAL_REPO, ".github", "ISSUE_TEMPLATE"),
                        os.path.join(self.tmp, ".github", "ISSUE_TEMPLATE"))
        os.makedirs(os.path.join(self.tmp, "scripts"), exist_ok=True)
        shutil.copy(os.path.join(REAL_REPO, "scripts", "issue_to_change.py"),
                    os.path.join(self.tmp, "scripts", "issue_to_change.py"))
        # Symlinked: assets/ is large and only listed.
        os.symlink(os.path.join(REAL_REPO, "assets"), os.path.join(self.tmp, "assets"))
        # review.yml can point at root pages (portal.md).
        for name in os.listdir(REAL_REPO):
            if name.endswith((".md", ".html")) and os.path.isfile(os.path.join(REAL_REPO, name)):
                os.symlink(os.path.join(REAL_REPO, name), os.path.join(self.tmp, name))
        os.symlink(os.path.join(REAL_REPO, "_guide"), os.path.join(self.tmp, "_guide"))
        self._saved = (vc.REPO_ROOT, vc.DATA_DIR, vc.FORMS_DIR)
        vc.REPO_ROOT = self.tmp
        vc.DATA_DIR = os.path.join(self.tmp, "_data")
        vc.FORMS_DIR = os.path.join(self.tmp, ".github", "ISSUE_TEMPLATE")

    def tearDown(self):
        vc.REPO_ROOT, vc.DATA_DIR, vc.FORMS_DIR = self._saved
        shutil.rmtree(self.tmp, ignore_errors=True)

    # Helpers
    def read(self, name):
        with open(os.path.join(vc.DATA_DIR, name), encoding="utf-8") as fh:
            return yaml.safe_load(fh)

    def write(self, name, data):
        with open(os.path.join(vc.DATA_DIR, name), "w", encoding="utf-8") as fh:
            yaml.safe_dump(data, fh, allow_unicode=True)

    def run_check(self, check):
        return list(check())

    def assertFlags(self, check, needle):
        """The check flags a problem mentioning `needle`."""
        problems = self.run_check(check)
        blob = " ".join(f"{p.where} {p.what}" for p in problems).lower()
        self.assertTrue(
            needle.lower() in blob,
            f"Expected a problem mentioning {needle!r}, got: "
            + (blob[:400] or "(no problems at all)"),
        )

    def assertClean(self, check):
        problems = [p for p in self.run_check(check) if not p.warning]
        self.assertEqual(problems, [], f"Unexpected problems: {[p.what for p in problems]}")

    # Real content passes
    def test_real_content_is_clean(self):
        """A noisy checker gets ignored."""
        for check in vc.CHECKS:
            self.assertClean(check)

    # Each check fires
    def test_broken_yaml_is_caught(self):
        with open(os.path.join(vc.DATA_DIR, "people.yml"), "w", encoding="utf-8") as fh:
            fh.write("groups:\n  - id: pi\n\ttitle: tab indented\n")
        self.assertFlags(vc.check_yaml_parses, "people.yml")

    def test_project_lead_must_exist(self):
        research = self.read("research.yml")
        research["projects"][0]["lead"] = "Someone Not In The Lab"
        self.write("research.yml", research)
        self.assertFlags(vc.check_research, "Someone Not In The Lab")

    def test_project_theme_must_exist(self):
        research = self.read("research.yml")
        research["projects"][0]["theme"] = "no-such-theme"
        self.write("research.yml", research)
        self.assertFlags(vc.check_research, "no-such-theme")

    def test_project_paper_doi_must_exist(self):
        research = self.read("research.yml")
        research["projects"][0]["papers"] = ["10.9999/not-a-real-doi"]
        self.write("research.yml", research)
        self.assertFlags(vc.check_research, "10.9999/not-a-real-doi")

    def test_duplicate_person_is_caught(self):
        people = self.read("people.yml")
        first = copy.deepcopy(people["groups"][0]["members"][0])
        people["groups"][1]["members"].append(first)
        self.write("people.yml", people)
        self.assertFlags(vc.check_people, "listed twice")

    def test_alumnus_without_a_start_year_is_caught(self):
        """No `start:`, no row in the alumni table."""
        people = self.read("people.yml")
        people["alumni"]["members"][0].pop("start", None)
        self.write("people.yml", people)
        self.assertFlags(vc.check_alumni, "start")

    def test_person_in_both_a_group_and_alumni_is_caught(self):
        people = self.read("people.yml")
        leaver = copy.deepcopy(people["alumni"]["members"][0])
        people["groups"][1]["members"].append(leaver)
        self.write("people.yml", people)
        self.assertFlags(vc.check_alumni, "alumni AND")

    def test_alumni_names_count_as_known_people(self):
        """Moving someone to alumni must not make their projects and news look like typos."""
        people = self.read("people.yml")
        names = vc.people_names(people)
        for alumnus in people["alumni"]["members"]:
            self.assertIn(alumnus["name"], names)
            for alias in alumnus.get("aliases") or []:
                self.assertIn(alias, names)

    def test_missing_person_photo_is_caught(self):
        people = self.read("people.yml")
        people["groups"][0]["members"][0]["photo"] = "/assets/img/people/nobody.jpg"
        self.write("people.yml", people)
        self.assertFlags(vc.check_people, "nobody.jpg")

    def test_malformed_orcid_is_caught(self):
        people = self.read("people.yml")
        people["groups"][0]["members"][0]["orcid"] = "https://orcid.org/0000-0002-2830-0844"
        self.write("people.yml", people)
        self.assertFlags(vc.check_people, "orcid")

    def test_pub_links_doi_must_match_a_paper(self):
        links = self.read("pub_links.yml")
        links[0]["doi"] = "10.9999/orphaned"
        self.write("pub_links.yml", links)
        self.assertFlags(vc.check_pub_links, "10.9999/orphaned")

    def test_press_doi_must_match_a_paper(self):
        press = self.read("press.yml")
        press[0]["items"][0]["doi"] = "10.9999/orphaned-press"
        self.write("press.yml", press)
        self.assertFlags(vc.check_press, "10.9999/orphaned-press")

    def test_two_featured_facilities_is_caught(self):
        facilities = self.read("facilities.yml")
        for facility in facilities:
            facility["featured"] = True
        self.write("facilities.yml", facilities)
        self.assertFlags(vc.check_facilities, "featured")

    def test_facility_photo_without_alt_text_is_caught(self):
        facilities = self.read("facilities.yml")
        target = next(f for f in facilities if f.get("photo"))
        target.pop("photo_alt", None)
        self.write("facilities.yml", facilities)
        self.assertFlags(vc.check_facilities, "photo_alt")

    def test_unknown_news_type_is_caught(self):
        updates = self.read("updates.yml")
        updates[0]["events"][0]["type"] = "gossip"
        self.write("updates.yml", updates)
        self.assertFlags(vc.check_updates, "gossip")

    def test_bad_news_date_format_is_caught(self):
        updates = self.read("updates.yml")
        updates[0]["events"][0]["date"] = "2026-07-01"
        self.write("updates.yml", updates)
        self.assertFlags(vc.check_updates, "2026-07-01")

    def test_issue_form_and_script_news_types_must_agree(self):
        path = os.path.join(vc.FORMS_DIR, "add-news.yml")
        with open(path, encoding="utf-8") as fh:
            form = yaml.safe_load(fh)
        for field in form["body"]:
            if field.get("id") == "type":
                field["attributes"]["options"].append("rumour")
        with open(path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(form, fh, allow_unicode=True)
        self.assertFlags(vc.check_updates, "rumour")

    def test_issue_form_role_without_a_mapping_is_caught(self):
        path = os.path.join(vc.FORMS_DIR, "add-person.yml")
        with open(path, encoding="utf-8") as fh:
            form = yaml.safe_load(fh)
        for field in form["body"]:
            if field.get("id") == "role":
                field["attributes"]["options"].append("Lab Mascot")
        with open(path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(form, fh, allow_unicode=True)
        self.assertFlags(vc.check_person_roles_match_form, "lab mascot")

    def test_quoted_boolean_in_openings_is_caught(self):
        openings = self.read("openings.yml")
        openings["graduate"]["open"] = "true"   # string, not boolean
        self.write("openings.yml", openings)
        self.assertFlags(vc.check_openings, "graduate.open")

    def test_duplicate_doi_across_publication_files_is_caught(self):
        pubs = self.read("publications.yml")
        manual = self.read("publications_manual.yml")
        duplicate = next(p for p in pubs if p.get("doi"))
        manual["conference"].append({
            "title": duplicate["title"], "authors": "Someone",
            "year": duplicate.get("year", 2026), "type": "conference",
            "doi": duplicate["doi"],
        })
        self.write("publications_manual.yml", manual)
        self.assertFlags(vc.check_publications, "appears twice")

    def test_bad_publication_date_is_caught(self):
        pubs = self.read("publications.yml")
        pubs[0]["date"] = "24 July 2026"
        self.write("publications.yml", pubs)
        self.assertFlags(vc.check_publications, "24 july 2026")

    def test_review_list_pointing_at_a_missing_file_is_caught(self):
        review = self.read("review.yml")
        review["items"][0]["file"] = "_data/deleted-long-ago.yml"
        self.write("review.yml", review)
        self.assertFlags(vc.check_review_list, "deleted-long-ago")

    def test_review_item_without_a_date_is_caught(self):
        review = self.read("review.yml")
        review["items"][0].pop("last_reviewed", None)
        self.write("review.yml", review)
        self.assertFlags(vc.check_review_list, "last_reviewed")

    # DOI normalisation
    def test_doi_forms_are_treated_as_equal(self):
        """publications.yml has full URLs, pub_links.yml bare DOIs; a mismatch hides every extra."""
        self.assertEqual(
            vc.norm_doi("https://doi.org/10.1098/rsif.2025.1082"),
            vc.norm_doi("10.1098/RSIF.2025.1082"),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
