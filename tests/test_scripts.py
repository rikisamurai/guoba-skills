import importlib.util
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script(filename):
    path = REPO_ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def seed_scaffold(root):
    (root / "README.md").write_text(
        "# Test Skills\n\n"
        "<!-- skills-index:start -->\n"
        "_No skills yet._\n"
        "<!-- skills-index:end -->\n",
        encoding="utf-8",
    )
    for path in [
        "templates",
        "skills/automation",
        ".agents/skills",
        ".claude/skills",
    ]:
        (root / path).mkdir(parents=True, exist_ok=True)
    (root / "templates/SKILL.template.md").write_text(
        "---\n"
        "name: {{name}}\n"
        "description: {{description}}\n"
        "---\n\n"
        "# {{title}}\n\n"
        "## Instructions\n\n"
        "Write the repeatable workflow here.\n",
        encoding="utf-8",
    )
    (root / "templates/SKILL.with-references.template.md").write_text(
        "---\n"
        "name: {{name}}\n"
        "description: {{description}}\n"
        "---\n\n"
        "# {{title}}\n\n"
        "## References\n\n"
        "Load files from `references/` only when needed.\n",
        encoding="utf-8",
    )


class SkillScriptTests(unittest.TestCase):
    def test_refresh_index_groups_skills_by_domain(self):
        refresh_index = load_script("refresh_index.py")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            skill_dir = root / "skills/automation/example-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: example-skill\n"
                "description: Example trigger text\n"
                "---\n\n"
                "# Example Skill\n",
                encoding="utf-8",
            )

            refresh_index.refresh_index(root)

            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("### automation", readme)
            self.assertIn(
                "- [example-skill](skills/automation/example-skill/) - Example trigger text",
                readme,
            )

    def test_refresh_index_supports_folded_yaml_descriptions(self):
        refresh_index = load_script("refresh_index.py")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            skill_dir = root / "skills/automation/folded-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: folded-skill\n"
                "description: >\n"
                "  First line of trigger text.\n"
                "  Second line continues it.\n"
                "metadata:\n"
                "  author: upstream\n"
                "---\n\n"
                "# Folded Skill\n",
                encoding="utf-8",
            )

            refresh_index.refresh_index(root)

            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn(
                "- [folded-skill](skills/automation/folded-skill/) - First line of trigger text. Second line continues it.",
                readme,
            )

    def test_new_skill_creates_skill_metadata_links_and_index(self):
        new_skill = load_script("new_skill.py")
        validate_repo = load_script("validate_repo.py")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)

            created = new_skill.create_skill(
                root=root,
                name="example-skill",
                domain="automation",
                description="Example trigger text",
                with_references=True,
                resources=("scripts", "assets"),
                dry_run=False,
            )

            skill_dir = root / "skills/automation/example-skill"
            self.assertEqual(created, skill_dir)
            self.assertTrue((skill_dir / "SKILL.md").is_file())
            self.assertTrue((skill_dir / "references").is_dir())
            self.assertTrue((skill_dir / "scripts").is_dir())
            self.assertTrue((skill_dir / "assets").is_dir())
            self.assertFalse((skill_dir / "agents").exists())

            for discovery in [".agents/skills", ".claude/skills"]:
                link = root / discovery / "example-skill"
                self.assertTrue(link.is_symlink(), discovery)
                self.assertEqual(link.resolve(), skill_dir.resolve())
            self.assertFalse((root / ".agent/skills/example-skill").exists())

            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("[example-skill](skills/automation/example-skill/)", readme)
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                self.assertEqual(validate_repo.validate_repo(root), 0)

    def test_new_skill_dry_run_leaves_filesystem_unchanged(self):
        new_skill = load_script("new_skill.py")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)

            with redirect_stdout(StringIO()):
                result = new_skill.create_skill(
                    root=root,
                    name="dry-run-skill",
                    domain="automation",
                    description="Dry run trigger text",
                    with_references=False,
                    resources=(),
                    dry_run=True,
                )

            self.assertEqual(result, root / "skills/automation/dry-run-skill")
            self.assertFalse((root / "skills/automation/dry-run-skill").exists())
            self.assertFalse((root / ".agents/skills/dry-run-skill").exists())
            self.assertFalse((root / ".agent/skills/dry-run-skill").exists())

    def test_new_skill_rolls_back_when_discovery_link_fails(self):
        new_skill = load_script("new_skill.py")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            original_readme = (root / "README.md").read_text(encoding="utf-8")

            with patch.object(
                new_skill,
                "create_relative_symlink",
                side_effect=PermissionError("blocked"),
            ):
                with self.assertRaises(PermissionError):
                    new_skill.create_skill(
                        root=root,
                        name="rollback-skill",
                        domain="automation",
                        description="Rollback trigger text",
                        with_references=True,
                        resources=("scripts",),
                        dry_run=False,
                    )

            self.assertFalse((root / "skills/automation/rollback-skill").exists())
            self.assertFalse((root / ".agents/skills/rollback-skill").exists())
            self.assertEqual(
                (root / "README.md").read_text(encoding="utf-8"),
                original_readme,
            )

    def test_validate_repo_rejects_mismatched_frontmatter_name(self):
        validate_repo = load_script("validate_repo.py")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            skill_dir = root / "skills/automation/example-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: wrong-name\n"
                "description: Example trigger text\n"
                "---\n\n"
                "# Example Skill\n",
                encoding="utf-8",
            )

            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_parse_frontmatter_strips_double_quoted_value(self):
        refresh_index = load_script("refresh_index.py")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(
                '---\n'
                'name: example\n'
                'description: "Quoted trigger"\n'
                '---\n\n'
                '# Body\n',
                encoding="utf-8",
            )
            self.assertEqual(
                refresh_index.parse_frontmatter(path)["description"],
                "Quoted trigger",
            )

    def test_parse_frontmatter_strips_single_quoted_value(self):
        refresh_index = load_script("refresh_index.py")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(
                "---\n"
                "name: example\n"
                "description: 'Single quoted'\n"
                "---\n\n"
                "# Body\n",
                encoding="utf-8",
            )
            self.assertEqual(
                refresh_index.parse_frontmatter(path)["description"],
                "Single quoted",
            )

    def test_new_skill_rejects_non_kebab_name(self):
        new_skill = load_script("new_skill.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            with self.assertRaises(ValueError):
                new_skill.create_skill(
                    root=root,
                    name="Bad_Name",
                    domain="automation",
                    description="x",
                )

    def test_new_skill_rejects_non_kebab_domain(self):
        new_skill = load_script("new_skill.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            with self.assertRaises(ValueError):
                new_skill.create_skill(
                    root=root,
                    name="ok-name",
                    domain="Bad_Domain",
                    description="x",
                )

    def test_new_skill_rejects_unknown_domain(self):
        new_skill = load_script("new_skill.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            with self.assertRaises(FileNotFoundError):
                new_skill.create_skill(
                    root=root,
                    name="ok-name",
                    domain="missing-domain",
                    description="x",
                )

    def test_new_skill_rejects_existing_skill(self):
        new_skill = load_script("new_skill.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            (root / "skills/automation/dup-skill").mkdir(parents=True)
            with self.assertRaises(FileExistsError):
                new_skill.create_skill(
                    root=root,
                    name="dup-skill",
                    domain="automation",
                    description="x",
                )

    def test_new_skill_rejects_unknown_resources(self):
        new_skill = load_script("new_skill.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            with self.assertRaises(ValueError):
                new_skill.create_skill(
                    root=root,
                    name="ok-name",
                    domain="automation",
                    description="x",
                    resources=("unknown-dir",),
                )

    def _seed_valid_skill(self, root: Path, name: str = "ok-skill") -> Path:
        new_skill = load_script("new_skill.py")
        return new_skill.create_skill(
            root=root,
            name=name,
            domain="automation",
            description="Trigger text",
        )

    def test_validate_repo_rejects_missing_description(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            skill_dir = root / "skills/automation/example-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: example-skill\n"
                "description:\n"
                "---\n\n"
                "# Example\n",
                encoding="utf-8",
            )
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_validate_repo_rejects_non_kebab_folder_name(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            skill_dir = root / "skills/automation/Bad_Name"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: Bad_Name\n"
                "description: trigger\n"
                "---\n\n"
                "# Body\n",
                encoding="utf-8",
            )
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_validate_repo_rejects_non_kebab_domain(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            skill_dir = root / "skills/Bad_Domain/ok-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: ok-skill\n"
                "description: trigger\n"
                "---\n\n"
                "# Body\n",
                encoding="utf-8",
            )
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_validate_repo_rejects_missing_discovery_symlink(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            self._seed_valid_skill(root)
            (root / ".claude/skills/ok-skill").unlink()
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_validate_repo_rejects_wrong_symlink_target(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            self._seed_valid_skill(root)
            decoy = root / "skills/automation/decoy"
            decoy.mkdir()
            link = root / ".claude/skills/ok-skill"
            link.unlink()
            link.symlink_to(decoy, target_is_directory=True)
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_validate_repo_rejects_orphan_discovery_symlink(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            self._seed_valid_skill(root)
            ghost = root / ".claude/skills/ghost-skill"
            ghost.symlink_to(
                root / "skills/automation/ok-skill",
                target_is_directory=True,
            )
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_validate_repo_rejects_non_symlink_discovery_entry(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            self._seed_valid_skill(root)
            (root / ".claude/skills/stray-file").write_text("x", encoding="utf-8")
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_validate_repo_rejects_missing_discovery_dir(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            self._seed_valid_skill(root)
            shutil.rmtree(root / ".claude/skills")
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_validate_repo_rejects_stale_readme_index(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            self._seed_valid_skill(root)
            readme = root / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8").replace(
                    "ok-skill", "renamed-skill"
                ),
                encoding="utf-8",
            )
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_validate_repo_rejects_readme_missing_markers(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            self._seed_valid_skill(root)
            (root / "README.md").write_text("# No markers here\n", encoding="utf-8")
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)

    def test_validate_repo_rejects_missing_readme(self):
        validate_repo = load_script("validate_repo.py")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed_scaffold(root)
            self._seed_valid_skill(root)
            (root / "README.md").unlink()
            with redirect_stderr(StringIO()):
                self.assertNotEqual(validate_repo.validate_repo(root), 0)


if __name__ == "__main__":
    unittest.main()
