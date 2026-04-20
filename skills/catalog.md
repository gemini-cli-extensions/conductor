# Agent Skills Catalog

This catalog defines the curriculum of skills available to the Conductor extension.

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

## CI/CD Skills
Skills for designing, building, and managing CI/CD pipelines and infrastructure on Google Cloud.

### google-cicd-release-orchestration
- **Description**: Manage the entire lifecycle of Google Cloud Deploy, from designing and creating delivery pipelines to managing releases and debugging failures.
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/cicd/main/skills/google-cicd-release-orchestration/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `gcloud`
    - **Keywords**: `Cloud Deploy`, `delivery pipeline`, `clouddeploy.yaml`, `canary deployment`, `blue-green deployment`, `automatic rollback`

### google-cicd-deploy
- **Description**: Assistant for deploying applications to Google Cloud, supporting Static Sites (GCS), Cloud Run (Buildpacks or Images), and Google Kubernetes Engine (GKE).
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/cicd/main/skills/google-cicd-deploy/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `gcloud`
    - **Keywords**: `Cloud Run`, `GCS`,'GKE', `Static Site`, `Deployment`, `Google Cloud`

### google-cicd-pipeline-design
- **Description**: Assistant for designing, building, and managing CI/CD pipelines on Google Cloud, focusing on architectural design and implementation planning.
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/cicd/main/skills/google-cicd-pipeline-design/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `gcloud`
    - **Keywords**: `CI/CD`, `Pipeline Design`, `Google Cloud`, `Architectural Design`, `cloudbuild.yaml`, `Cloud Build`, `Artifact Registry`, `Cloud Deploy`

### google-cicd-terraform
- **Description**: Use Terraform to provision Google Cloud resources (GKE, Cloud Run, Cloud SQL) with standard GCS backend state management and IAM least-privilege.
- **URL**: https://raw.githubusercontent.com/gemini-cli-extensions/cicd/main/skills/google-cicd-terraform/
- **Party**: 1p
- **Detection Signals**:
    - **Dependencies**: `terraform`, `gcloud`
    - **Keywords**: `Terraform`, `GCP`, `GCS Backend`, `Infrastructure as Code`, `IaC`
