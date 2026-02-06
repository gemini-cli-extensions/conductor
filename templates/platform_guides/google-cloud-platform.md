# Google Cloud Platform (GCP) Best Practices

This document outlines the recommended best practices for developing and deploying applications on Google Cloud Platform (GCP).

## 1. IAM & Security
- **Principle of Least Privilege**: Grant only the permissions necessary for a resource to function. Use predefined roles carefully; prefer custom roles for granular control.
- **Proactive Definition**:
    - Explicitly list required APIs and IAM roles in your documentation or Infrastructure as Code (IaC).
    - Do not rely on "discovery via failure" for permissions.
- **Service Accounts**:
    - Use separate service accounts for different services (e.g., `frontend-sa`, `backend-sa`).
    - Avoid using the default Compute Engine service account.
    - **Pre-deployment Check**: Verify that your Service Account has the necessary permissions *before* starting a deployment to prevent partial failures.
    - Limit service key creation and rotation; prefer Workload Identity Federation for external access.
- **Secret Management**:
    - Never hardcode secrets in code or configuration files.
    - Use **Secret Manager** to store API keys, passwords, and certificates.
    - Access secrets at runtime via the client library or environment variables injected by the platform.

## 2. Resource Management
- **Hierarchy**: Organize resources using the Organization > Folder > Project hierarchy.
    - Use Folders to group projects by department (e.g., `Engineering`, `Sales`) or environment (e.g., `Production`, `Non-Production`).
- **APIs**:
    - Explicitly enable and manage required Google Cloud APIs using Terraform/IaC to ensure consistency across environments.
- **Labeling**: Apply consistent labels to all resources for cost tracking and filtering.
    - Recommended labels: `environment` (dev, stage, prod), `service` (api, worker), `owner` (team-name).
- **Regions & Zones**:
    - Deploy resources across multiple zones within a region for high availability.
    - Use multi-region buckets for critical data that requires geo-redundancy.

## 3. Infrastructure as Code (Terraform)
- **Validation**:
    - Always run `terraform validate` to check for syntax errors and internal consistency before finalizing code.
    - Implement CI/CD checks to enforce `terraform fmt` and `terraform validate` runs.
- **State Management**:
    - Use a **Remote Backend** (e.g., GCS bucket) for state storage with locking enabled to prevent race conditions.
    - Encrypt state files and restrict access permissions.
- **Modularization**:
    - Break down complex infrastructure into reusable **Modules**.
    - Use directory structure to separate environments (e.g., `envs/prod`, `envs/dev`) while reusing modules.

## 4. Networking
- **VPC Design**:
    - Use **Custom Mode** VPC networks to have full control over IP ranges.
    - Avoid overlapping IP ranges between VPCs if VPC Peering or VPNs are anticipated.
    - Use **Private Google Access** to allow VMs without public IPs to reach Google APIs.
- **Security**:
    - Use **Firewall Rules** (or Policies) to strictly control ingress and egress traffic.
    - Minimize the use of external IP addresses; use Cloud NAT for outbound internet access from private instances.

## 5. Compute
- **Selection Criteria**:
    - **Cloud Run**: Best for stateless HTTP containers, event-driven functions, and rapid scaling (Serverless).
    - **GKE (Google Kubernetes Engine)**: Best for complex microservices architectures, stateful workloads, and needing full control over the cluster.
        - Use **Autopilot** mode for reduced operational overhead unless specific node configuration is required.
    - **Compute Engine (GCE)**: Best for legacy applications, specific kernel requirements, or databases not supported by managed services.

## 6. Storage
- **Cloud Storage (GCS)**:
    - Enable **Object Versioning** to protect against accidental overwrites or deletions.
    - Use **Lifecycle Policies** to automatically move old data to cheaper storage classes (e.g., Nearline, Coldline).
    - Ensure buckets are private by default; use specialized IAM bindings for public access if absolutely necessary.
- **Managed Databases**:
    - Prefer managed services like **Cloud SQL** (PostgreSQL/MySQL) or **Firestore** (NoSQL) over self-hosted databases on GCE.
    - Enable automated backups and high availability (HA) for production databases.

## 7. Observability
- **Logging**:
    - Use **Cloud Logging** (formerly Stackdriver).
    - Emit **Structured Logging** (JSON format) to enable rich filtering and analysis.
- **Monitoring & Alerting**:
    - Monitor specific metrics using **Cloud Monitoring**.
    - Set up alerts for critical usage thresholds (e.g., CPU, Memory, 5xx error rates) and budget spending.
    - Implement Health Checks for all services.
