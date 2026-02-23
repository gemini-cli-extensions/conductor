# Project Tracks

This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.

---

## [x] Track: Deep Audit & Final Polish

*Link: [./conductor/tracks/audit_polish_20251230/](./conductor/tracks/audit_polish_20251230/)*

---

## [x] Track: Individual Conductor Skills Not Appearing in Codex

*Link: [./conductor/tracks/codex_skills_20251231/](./conductor/tracks/codex_skills_20251231/)*

---

- [x] **Track: Platform Adapter Expansion (Claude, Codex, etc.)**
*Link: [./conductor/tracks/adapter_expansion_20260131/](./conductor/tracks/adapter_expansion_20260131/)*

---

- [x] **Track: Upstream Sync & Cross-Platform Skill Abstraction**
*Link: [./conductor/tracks/archive/upstream_sync_20260131/](./conductor/tracks/archive/upstream_sync_20260131/)*

---

- [x] **Track: Workflow Packaging & Validation Schema (All Tools)**
*Link: [./conductor/tracks/archive/workflow_packaging_20260131/](./conductor/tracks/archive/workflow_packaging_20260131/)*

---

- [x] **Track: Installer UX & Cross-Platform Release**
*Link: [./conductor/tracks/archive/installer_ux_20260131/](./conductor/tracks/archive/installer_ux_20260131/)*

---

- [x] **Track: Antigravity Skills.md Adoption (Exploration)**
*Link: [./conductor/tracks/archive/antigravity_skills_20260131/](./conductor/tracks/archive/antigravity_skills_20260131/)*

---

- [x] **Track: Artifact Drift Prevention & CI Sync**
*Link: [./conductor/tracks/archive/artifact_drift_20260131/](./conductor/tracks/archive/artifact_drift_20260131/)*

---

- [x] **Track: Git-Native Workflow & Multi-VCS Support**
*Link: [./conductor/tracks/archive/git_native_vcs_20260131/](./conductor/tracks/archive/git_native_vcs_20260131/)*

---

- [x] **Track: Context Hygiene & Memory Safety**
*Link: [./conductor/tracks/archive/context_hygiene_20260131/](./conductor/tracks/archive/context_hygiene_20260131/)*

---

- [x] **Track: Setup/NewTrack UX Consistency**
*Link: [./conductor/tracks/archive/setup_newtrack_ux_20260131/](./conductor/tracks/archive/setup_newtrack_20260131/)*

---

- [x] **Track: Release Guidance & Packaging**
*Link: [./conductor/tracks/archive/release_guidance_20260131/](./conductor/tracks/archive/release_guidance_20260131/)*

---

- [x] **Track: AIX and SkillShare Integration**
*Link: [./conductor/archive/aix_skillshare_integration_20260201/](./conductor/archive/aix_skillshare_integration_20260201/)*

---

- [x] **Track: Repository Excellence & Pipeline Hardening**
*Link: [./tracks/repository_excellence_20260210/](./tracks/repository_excellence_20260210/)*

---

- [x] **Track: Universal Installer via Mise**
*Link: [./tracks/universal_installer_20260214/](./tracks/universal_installer_20260214/)*
- **Purpose:** One-click installer for all conductor components using mise
- **Deliverables:** mise.toml, install.sh, install.ps1, conductor_install.py
- **Key Features:** install.cat integration, cross-platform support, automated updates

---

- [x] **Track: Upstream Sync Bot & Issue Triage** [d4ed2c5]
*Link: [./tracks/archive/upstream_sync_bot_20260214/](./tracks/archive/upstream_sync_bot_20260214/)*
- **Purpose:** Automated sync from upstream repos and GitHub issue triage
- **Deliverables:** sync_upstream.py, triage_issues.py, GitHub Actions workflow
- **Key Issues:** #113, #112, #105, #115, #108, #103, #97, #96
- **Note:** Includes repository rename (conductor → conductor-next)
- **Status:** COMPLETE - All 6 phases done
- **Archived:** 2026-02-23

## Active Tracks (Created from Upstream Issues)

- [x] **Track: AskUser tool integration for interactive prompts** [5df9ec2]
  - Priority: P0 (Critical)
  - Source: gemini-cli-extensions/conductor#105
  - Status: COMPLETE - Archived
  - Archived: ./tracks/archive/issue_105_20260223/

- [x] **Track: Auto-create .gitignore for new tracks** [0ca1faf]
  - Priority: P1 (High)
  - Source: gemini-cli-extensions/conductor#113
  - Status: COMPLETE - Archived
  - Archived: ./tracks/archive/issue_113_20260223/

- [~] **Track: Add overwrite confirmation for file operations** (./tracks/issue_112_20260223/)
  - Priority: P1 (High)
  - Source: gemini-cli-extensions/conductor#112
  - Status: IN PROGRESS - Starting Phase 1

- [ ] **Track: Multi-agent support for parallel track execution** (./tracks/issue_115_20260223/)
  - Priority: P1 (High)
  - Source: gemini-cli-extensions/conductor#112

- [ ] **Track: Multi-agent support for parallel track execution** (./tracks/issue_115_20260223/)
  - Priority: P1 (High)
  - Source: gemini-cli-extensions/conductor#115

- [ ] **Track: Improve error messages for track creation failures** (./tracks/issue_108_20260223/)
  - Priority: P2 (Medium)
  - Source: gemini-cli-extensions/conductor#108

- [ ] **Track: Add track dependency visualization** (./tracks/issue_103_20260223/)
  - Priority: P2 (Medium)
  - Source: gemini-cli-extensions/conductor#103

- [ ] **Track: Support for custom track templates** (./tracks/issue_97_20260223/)
  - Priority: P2 (Medium)
  - Source: gemini-cli-extensions/conductor#97

- [ ] **Track: Add track completion checklist** (./tracks/issue_96_20260223/)
  - Priority: P2 (Medium)
  - Source: gemini-cli-extensions/conductor#96

---

- [x] **Track: Documentation Standards & Style Guides** [fb5c64e]
*Link: [./tracks/archive/documentation_standards_20260214/](./tracks/archive/documentation_standards_20260214/)*
- **Purpose:** Define and enforce consistent documentation standards
- **Style guides for:** Markdown, Mermaid, D3.js, DOCX, CSL-JSON
- **CI/CD integration:** Automated doc validation in GitHub Actions
- **Pre-commit hooks:** Automated checking before commits
- **Deliverables:** markdownlint config, validation scripts, workflow updates
- **Archived:** 2026-02-23
