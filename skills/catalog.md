# Agent Skills Catalog

This catalog defines the curriculum of skills available to the Conductor extension.

<!-- ## Universal Skills
These skills are always recommended for every project.

### commit
- **Description**: Generate a conventional commit message from staged changes
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/commit/
- **Always Recommend**: `true`
- **Party**: 1p

### pr-description
- **Description**: Write a PR title and description from branch diff
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/pr-description/
- **Always Recommend**: `true`
- **Party**: 1p

### code-review
- **Description**: Structured code review with severity levels
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/code-review/
- **Always Recommend**: `true`
- **Party**: 1p

### changelog
- **Description**: Generate a CHANGELOG entry from recent commits
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/changelog/
- **Always Recommend**: `true`
- **Party**: 1p

### write-tests
- **Description**: Generate unit/integration tests for a file or function
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/write-tests/
- **Always Recommend**: `true`
- **Party**: 1p

### fix-failing-tests
- **Description**: Diagnose and fix failing tests
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/fix-failing-tests/
- **Always Recommend**: `true`
- **Party**: 1p

### document
- **Description**: Add docstrings or JSDoc to selected code
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/document/
- **Always Recommend**: `true`
- **Party**: 1p

### readme-update
- **Description**: Update README to reflect recent changes
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/readme-update/
- **Always Recommend**: `true`
- **Party**: 1p

### security-review
- **Description**: OWASP-focused security review
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/security-review/
- **Always Recommend**: `true`
- **Party**: 1p

### dependency-audit
- **Description**: Identify outdated or vulnerable dependencies
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/dependency-audit/
- **Always Recommend**: `true`
- **Party**: 1p

--- -->

<!-- ## GCP Skills
Skills specialized for Google Cloud Platform development.

### gcp-deploy
- **Description**: Deploy to Cloud Run, GKE, or App Engine
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-deploy/
- **Party**: 1p
- **Detection Signals**:
    - **Files**: `app.yaml`, `cloudbuild.yaml`, `Dockerfile`
    - **Dependencies**: `@google-cloud/`, `google-cloud-`
    - **Keywords**: `GCP`, `Google Cloud`, `Cloud Run`, `App Engine`

### gcp-cloudbuild
- **Description**: Generate or update Cloud Build pipelines
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-cloudbuild/
- **Party**: 1p
- **Detection Signals**:
    - **Files**: `cloudbuild.yaml`
    - **Keywords**: `Cloud Build`, `CI/CD`

### gcp-terraform
- **Description**: Generate GCP Terraform resource configs
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-terraform/
- **Party**: 1p
- **Detection Signals**:
    - **Files**: `*.tf`
    - **Keywords**: `Terraform`, `IaC`

### gcp-iam
- **Description**: Review and generate IAM policies (least-privilege)
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-iam/
- **Party**: 1p
- **Detection Signals**:
    - **Keywords**: `IAM`, `Permissions`

### gcp-monitoring
- **Description**: Set up Cloud Monitoring alerts and dashboards
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-monitoring/
- **Party**: 1p
- **Detection Signals**:
    - **Keywords**: `Monitoring`, `Alerts`, `Observability`

### gcp-pubsub
- **Description**: Design Pub/Sub schemas and generate client code
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-pubsub/
- **Party**: 1p
- **Detection Signals**:
    - **Keywords**: `Pub/Sub`, `Messaging`

### gcp-firestore
- **Description**: Design Firestore schemas and optimize queries
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-firestore/
- **Party**: 1p
- **Detection Signals**:
    - **Keywords**: `Firestore`, `NoSQL`

### gcp-bigquery
- **Description**: Generate and optimize BigQuery schemas and SQL
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-bigquery/
- **Party**: 1p
- **Detection Signals**:
    - **Keywords**: `BigQuery`, `Data Warehouse`

### gcp-secret-manager
- **Description**: Migrate secrets to Secret Manager
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/conductor/main/skills/gcp-secret-manager/
- **Party**: 1p
- **Detection Signals**:
    - **Keywords**: `Secret Manager`, `Secrets`

--- -->

## GCP OWASP Top 10 Skills
Skills focused on auditing and remediating OWASP Top 10 vulnerabilities on Google Cloud Platform.

### gcp-broken-access-control
- **Description**: Audit and remediate broken access control vulnerabilities
- **URL**: https://raw.githubusercontent.com/hminooei/gcp-owasp-top10-skills/main/skills/gcp-broken-access-control/
- **Party**: 3p
- **Commit SHA**: 38789fb168ca741b9cc907e9f156405f9cb6c9df
- **Detection Signals**:
    - **Files**: `*.tf`, `iam.tf`
    - **Keywords**: `OWASP`, `Security`, `Cloud Asset Inventory`, `IAM`, `Load Balancing`

### gcp-cryptographic-failures
- **Description**: Audit and remediate cryptographic failures
- **URL**: https://raw.githubusercontent.com/hminooei/gcp-owasp-top10-skills/main/skills/gcp-cryptographic-failures/
- **Party**: 3p
- **Commit SHA**: 38789fb168ca741b9cc907e9f156405f9cb6c9df
- **Detection Signals**:
    - **Files**: `*.tf`
    - **Dependencies**: `@google-cloud/kms`, `@google-cloud/secret-manager`, `google-cloud-kms`, `google-cloud-secret-manager`, `cloud.google.com/go/kms`
    - **Keywords**: `OWASP`, `Security`, `KMS`, `Secret Manager`, `Cloud DLP`

### gcp-injection
- **Description**: Audit and remediate injection vulnerabilities
- **URL**: https://raw.githubusercontent.com/hminooei/gcp-owasp-top10-skills/main/skills/gcp-injection/
- **Party**: 3p
- **Commit SHA**: 38789fb168ca741b9cc907e9f156405f9cb6c9df
- **Detection Signals**:
    - **Files**: `app.yaml`, `Dockerfile`
    - **Dependencies**: `pg`, `mysql`, `sqlite3`, `mssql`
    - **Keywords**: `OWASP`, `Security`, `Web Security Scanner`, `Cloud Armor`, `SQLi`

### gcp-insecure-design
- **Description**: Audit and remediate insecure design flaws
- **URL**: https://raw.githubusercontent.com/hminooei/gcp-owasp-top10-skills/main/skills/gcp-insecure-design/
- **Party**: 3p
- **Commit SHA**: 38789fb168ca741b9cc907e9f156405f9cb6c9df
- **Detection Signals**:
    - **Files**: `*.tf`, `cloudbuild.yaml`
    - **Keywords**: `OWASP`, `Security`, `Apigee`, `Cloud DLP`, `Security Command Center`

### gcp-security-misconfiguration
- **Description**: Audit and remediate security misconfigurations
- **URL**: https://raw.githubusercontent.com/hminooei/gcp-owasp-top10-skills/main/skills/gcp-security-misconfiguration/
- **Party**: 3p
- **Commit SHA**: 38789fb168ca741b9cc907e9f156405f9cb6c9df
- **Detection Signals**:
    - **Files**: `*.tf`, `app.yaml`, `cloudbuild.yaml`, `Dockerfile`
    - **Keywords**: `OWASP`, `Security`, `VPC Firewall`, `Compute Engine`, `Hardening`

### gcp-vulnerable-components
- **Description**: Audit and remediate vulnerable and outdated components
- **URL**: https://raw.githubusercontent.com/hminooei/gcp-owasp-top10-skills/main/skills/gcp-vulnerable-components/
- **Party**: 3p
- **Commit SHA**: 38789fb168ca741b9cc907e9f156405f9cb6c9df
- **Detection Signals**:
    - **Files**: `package.json`, `requirements.txt`, `go.mod`, `pom.xml`, `build.gradle`, `Dockerfile`, `cloudbuild.yaml`
    - **Keywords**: `OWASP`, `Security`, `Artifact Registry`, `GKE`, `Container Analysis`

### gcp-auth-failures
- **Description**: Audit and remediate identification and authentication failures
- **URL**: https://raw.githubusercontent.com/hminooei/gcp-owasp-top10-skills/main/skills/gcp-auth-failures/
- **Party**: 3p
- **Commit SHA**: 38789fb168ca741b9cc907e9f156405f9cb6c9df
- **Detection Signals**:
    - **Files**: `*.tf`, `app.yaml`
    - **Dependencies**: `firebase-admin`, `google-auth-library`, `google-cloud-identity`, `@google-cloud/iap`
    - **Keywords**: `OWASP`, `Security`, `IAP`, `Identity-Aware Proxy`, `Cloud Armor`, `Identity Platform`

### gcp-integrity-failures
- **Description**: Audit and remediate software and data integrity failures
- **URL**: https://raw.githubusercontent.com/hminooei/gcp-owasp-top10-skills/main/skills/gcp-integrity-failures/
- **Party**: 3p
- **Commit SHA**: 38789fb168ca741b9cc907e9f156405f9cb6c9df
- **Detection Signals**:
    - **Files**: `cloudbuild.yaml`, `Dockerfile`, `binauthz.yaml`
    - **Keywords**: `OWASP`, `Security`, `Artifact Registry`, `Cloud Build`, `Binary Authorization`

### gcp-logging-monitoring-failures
- **Description**: Audit and remediate logging and monitoring failures
- **URL**: https://raw.githubusercontent.com/hminooei/gcp-owasp-top10-skills/main/skills/gcp-logging-monitoring-failures/
- **Party**: 3p
- **Commit SHA**: 38789fb168ca741b9cc907e9f156405f9cb6c9df
- **Detection Signals**:
    - **Files**: `*.tf`
    - **Dependencies**: `@google-cloud/logging`, `@google-cloud/monitoring`, `google-cloud-logging`, `cloud.google.com/go/logging`
    - **Keywords**: `OWASP`, `Security`, `Cloud Logging`, `Cloud Monitoring`, `Audit Logs`

### gcp-ssrf
- **Description**: Audit and remediate server-side request forgery (SSRF)
- **URL**: https://raw.githubusercontent.com/hminooei/gcp-owasp-top10-skills/main/skills/gcp-ssrf/
- **Party**: 3p
- **Commit SHA**: 38789fb168ca741b9cc907e9f156405f9cb6c9df
- **Detection Signals**:
    - **Files**: `*.tf`, `app.yaml`
    - **Keywords**: `OWASP`, `Security`, `VPC Service Controls`, `Access Context Manager`, `Egress`

### gcp-apis
- **Description**: Manage and enable Google Cloud Platform APIs
- **URL**: https://source.corp.google.com/piper///depot/google3/experimental/users/zerep/gcp-skills/skills/gcp-apis/
- **Party**: 1p
- **Detection Signals**:
    - **Keywords**: `GCP`, `Google Cloud APIs`, `Enable API`

## Firebase Skills
Skills focused on setting up, managing, and using various Firebase services.

### firebase-ai-logic-basics
- **Description**: Official skill for integrating Firebase AI Logic (Gemini API) into web applications. Covers setup, multimodal inference, structured output, and security.
- **URL**: https://raw.githubusercontent.com/firebase/agent-skills/main/skills/firebase-ai-logic-basics/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `firebase`, `firebase-admin`
    - **Keywords**: `Firebase`, `AI Logic`, `Gemini API`, `GenAI`

### firebase-app-hosting-basics
- **Description**: Deploy and manage web apps with Firebase App Hosting. Use this skill when deploying Next.js/Angular apps with backends.
- **URL**: https://raw.githubusercontent.com/firebase/agent-skills/main/skills/firebase-app-hosting-basics/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `firebase`, `firebase-admin`
    - **Keywords**: `Firebase App Hosting`, `Next.js`, `Angular`

### firebase-auth-basics
- **Description**: Guide for setting up and using Firebase Authentication. Use this skill when the user's app requires user sign-in, user management, or secure data access using auth rules.
- **URL**: https://raw.githubusercontent.com/firebase/agent-skills/main/skills/firebase-auth-basics/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `firebase`, `firebase-admin`
    - **Keywords**: `Firebase Authentication`, `Auth`, `Sign-in`

### firebase-basics
- **Description**: Guide for setting up and using Firebase. Use this skill when the user is getting started with Firebase - setting up local environment, using Firebase for the first time, or adding Firebase to their app.
- **URL**: https://raw.githubusercontent.com/firebase/agent-skills/main/skills/firebase-basics/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `firebase`, `firebase-admin`
    - **Keywords**: `Firebase`, `Setup`

### firebase-data-connect-basics
- **Description**: Build and deploy Firebase Data Connect backends with PostgreSQL. Use for schema design, GraphQL queries/mutations, authorization, and SDK generation for web, Android, iOS, and Flutter apps.
- **URL**: https://raw.githubusercontent.com/firebase/agent-skills/main/skills/firebase-data-connect-basics/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `firebase`, `firebase-admin`
    - **Keywords**: `Firebase Data Connect`, `PostgreSQL`, `GraphQL`

### firebase-firestore-basics
- **Description**: Comprehensive guide for Firestore basics including provisioning, security rules, and SDK usage. Use this skill when the user needs help setting up Firestore, writing security rules, or using the Firestore SDK in their application.
- **URL**: https://raw.githubusercontent.com/firebase/agent-skills/main/skills/firebase-firestore-basics/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `firebase`, `firebase-admin`
    - **Keywords**: `Firestore`, `Database`, `Security Rules`

### firebase-hosting-basics
- **Description**: Skill for working with Firebase Hosting (Classic). Use this when you want to deploy static web apps, Single Page Apps (SPAs), or simple microservices. Do NOT use for Firebase App Hosting.
- **URL**: https://raw.githubusercontent.com/firebase/agent-skills/main/skills/firebase-hosting-basics/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `firebase`, `firebase-admin`
    - **Keywords**: `Firebase Hosting`, `Static Hosting`
