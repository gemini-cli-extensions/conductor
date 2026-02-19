---
skills:
  # Always Recommended
  - name: commit
    description: Generate a conventional commit message from staged changes
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/commit/SKILL.md
    alwaysRecommend: true
  - name: pr-description
    description: Write a PR title and description from branch diff
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/pr-description/SKILL.md
    alwaysRecommend: true
  - name: code-review
    description: Structured code review with severity levels
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/code-review/SKILL.md
    alwaysRecommend: true
  - name: changelog
    description: Generate a CHANGELOG entry from recent commits
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/changelog/SKILL.md
    alwaysRecommend: true
  - name: write-tests
    description: Generate unit/integration tests for a file or function
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/write-tests/SKILL.md
    alwaysRecommend: true
  - name: fix-failing-tests
    description: Diagnose and fix failing tests
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/fix-failing-tests/SKILL.md
    alwaysRecommend: true
  - name: document
    description: Add docstrings or JSDoc to selected code
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/document/SKILL.md
    alwaysRecommend: true
  - name: readme-update
    description: Update README to reflect recent changes
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/readme-update/SKILL.md
    alwaysRecommend: true
  - name: security-review
    description: OWASP-focused security review
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/security-review/SKILL.md
    alwaysRecommend: true
  - name: dependency-audit
    description: Identify outdated or vulnerable dependencies
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/dependency-audit/SKILL.md
    alwaysRecommend: true

  # GCP Skills
  - name: gcp-deploy
    description: Deploy to Cloud Run, GKE, or App Engine
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-deploy/SKILL.md
    detectSignals:
      files:
        - app.yaml
        - cloudbuild.yaml
        - Dockerfile
      dependencies:
        - "@google-cloud/"
        - "google-cloud-"
      keywords:
        - "GCP"
        - "Google Cloud"
        - "Cloud Run"
        - "App Engine"
  - name: gcp-cloudbuild
    description: Generate or update Cloud Build pipelines
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-cloudbuild/SKILL.md
    detectSignals:
      files:
        - cloudbuild.yaml
      keywords:
        - "Cloud Build"
        - "CI/CD"
  - name: gcp-terraform
    description: Generate GCP Terraform resource configs
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-terraform/SKILL.md
    detectSignals:
      files:
        - "*.tf"
      keywords:
        - "Terraform"
        - "IaC"
  - name: gcp-iam
    description: Review and generate IAM policies (least-privilege)
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-iam/SKILL.md
    detectSignals:
      keywords:
        - "IAM"
        - "Permissions"
  - name: gcp-monitoring
    description: Set up Cloud Monitoring alerts and dashboards
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-monitoring/SKILL.md
    detectSignals:
      keywords:
        - "Monitoring"
        - "Alerts"
        - "Observability"
  - name: gcp-pubsub
    description: Design Pub/Sub schemas and generate client code
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-pubsub/SKILL.md
    detectSignals:
      keywords:
        - "Pub/Sub"
        - "Messaging"
  - name: gcp-firestore
    description: Design Firestore schemas and optimize queries
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-firestore/SKILL.md
    detectSignals:
      keywords:
        - "Firestore"
        - "NoSQL"
  - name: gcp-bigquery
    description: Generate and optimize BigQuery schemas and SQL
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-bigquery/SKILL.md
    detectSignals:
      keywords:
        - "BigQuery"
        - "Data Warehouse"
  - name: gcp-secret-manager
    description: Migrate secrets to Secret Manager
    url: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-secret-manager/SKILL.md
    detectSignals:
      keywords:
        - "Secret Manager"
        - "Secrets"
---
