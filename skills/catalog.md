# Agent Skills Catalog

This catalog defines the curriculum of skills available to the Conductor agent.

## Universal Skills
These skills are always recommended for every project.

### commit
- **Description**: Generate a conventional commit message from staged changes
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/commit/SKILL.md
- **Always Recommend**: `true`

### pr-description
- **Description**: Write a PR title and description from branch diff
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/pr-description/SKILL.md
- **Always Recommend**: `true`

### code-review
- **Description**: Structured code review with severity levels
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/code-review/SKILL.md
- **Always Recommend**: `true`

### changelog
- **Description**: Generate a CHANGELOG entry from recent commits
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/changelog/SKILL.md
- **Always Recommend**: `true`

### write-tests
- **Description**: Generate unit/integration tests for a file or function
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/write-tests/SKILL.md
- **Always Recommend**: `true`

### fix-failing-tests
- **Description**: Diagnose and fix failing tests
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/fix-failing-tests/SKILL.md
- **Always Recommend**: `true`

### document
- **Description**: Add docstrings or JSDoc to selected code
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/document/SKILL.md
- **Always Recommend**: `true`

### readme-update
- **Description**: Update README to reflect recent changes
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/readme-update/SKILL.md
- **Always Recommend**: `true`

### security-review
- **Description**: OWASP-focused security review
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/security-review/SKILL.md
- **Always Recommend**: `true`

### dependency-audit
- **Description**: Identify outdated or vulnerable dependencies
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/dependency-audit/SKILL.md
- **Always Recommend**: `true`

---

## GCP Skills
Skills specialized for Google Cloud Platform development.

### gcp-deploy
- **Description**: Deploy to Cloud Run, GKE, or App Engine
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-deploy/SKILL.md
- **Detection Signals**:
    - **Files**: `app.yaml`, `cloudbuild.yaml`, `Dockerfile`
    - **Dependencies**: `@google-cloud/`, `google-cloud-`
    - **Keywords**: `GCP`, `Google Cloud`, `Cloud Run`, `App Engine`

### gcp-cloudbuild
- **Description**: Generate or update Cloud Build pipelines
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-cloudbuild/SKILL.md
- **Detection Signals**:
    - **Files**: `cloudbuild.yaml`
    - **Keywords**: `Cloud Build`, `CI/CD`

### gcp-terraform
- **Description**: Generate GCP Terraform resource configs
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-terraform/SKILL.md
- **Detection Signals**:
    - **Files**: `*.tf`
    - **Keywords**: `Terraform`, `IaC`

### gcp-iam
- **Description**: Review and generate IAM policies (least-privilege)
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-iam/SKILL.md
- **Detection Signals**:
    - **Keywords**: `IAM`, `Permissions`

### gcp-monitoring
- **Description**: Set up Cloud Monitoring alerts and dashboards
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-monitoring/SKILL.md
- **Detection Signals**:
    - **Keywords**: `Monitoring`, `Alerts`, `Observability`

### gcp-pubsub
- **Description**: Design Pub/Sub schemas and generate client code
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-pubsub/SKILL.md
- **Detection Signals**:
    - **Keywords**: `Pub/Sub`, `Messaging`

### gcp-firestore
- **Description**: Design Firestore schemas and optimize queries
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-firestore/SKILL.md
- **Detection Signals**:
    - **Keywords**: `Firestore`, `NoSQL`

### gcp-bigquery
- **Description**: Generate and optimize BigQuery schemas and SQL
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-bigquery/SKILL.md
- **Detection Signals**:
    - **Keywords**: `BigQuery`, `Data Warehouse`

### gcp-secret-manager
- **Description**: Migrate secrets to Secret Manager
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-secret-manager/SKILL.md
- **Detection Signals**:
    - **Keywords**: `Secret Manager`, `Secrets`
