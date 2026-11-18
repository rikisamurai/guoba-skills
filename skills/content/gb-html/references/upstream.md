# Upstream provenance

- Project: https://github.com/QingYunA/answer-me-with-html
- Version: 0.6.1
- Commit: 9908ace6ee9254d51cb88e3b6db93738f2a90b53 (tag v0.6.1)
- License: MIT; see ../LICENSE and ../THIRD_PARTY_LICENSES.md. Bundled Bangers font: SIL OFL 1.1, see ../licenses/OFL-Bangers.txt.
- Bundled CLI SHA-256: `bb80c3af0d0dacf86f8b4b6f357efc8fe438129cce8d1c222182161d0184484b`.

The CLI, the video reference and the font license are copied without changes. Local changes are limited to the `gb-html` name (including the skill-directory names in SKILL.md's host-path list), manual-only invocation on Claude and Codex, removal of proactive/always-on guidance, and update instructions pointing to guoba-skills. All runtime features and defaults, including version checks, theme downloads, voice providers, file handling and browser opening, remain upstream behavior.

To upgrade, review the new upstream commit, copy its skill resources, reapply these instruction changes, refresh this version/hash and dependency licenses, and validate the repository and isolated runtime. Do not edit or rebuild the bundled CLI as part of this port.
