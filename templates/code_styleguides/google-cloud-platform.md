# Google Cloud Platform (GCP) Best Practices

This document outlines the recommended best practices for developing and deploying applications on Google Cloud Platform (GCP).

## 1. IAM & Security
- **Principle of Least Privilege**: Grant only the permissions necessary for a resource to function. Use predefined roles carefully; prefer custom roles for granular control.
- **Service Accounts**:
    - Use separate service accounts for different services (e.g., `frontend-sa`, `backend-sa`).
    - Avoid using the default Compute Engine service account.
    - Limit service key creation and rotation; prefer Workload Identity Federation for external access.
- **Secret Management**:
    - Never hardcode secrets in code or configuration files.
    - Use **Secret Manager** to store API keys, passwords, and certificates.
    - Access secrets at runtime via the client library or environment variables injected by the platform.

## 2. Resource Management
- **Hierarchy**: Organize resources using the Organization > Folder > Project hierarchy.
    - Use Folders to group projects by department (e.g., `Engineering`, `Sales`) or environment (e.g., `Production`, `Non-Production`).
- **Labeling**: Apply consistent labels to all resources for cost tracking and filtering.
    - Recommended labels: `environment` (dev, stage, prod), `service` (api, worker), `owner` (team-name).
- **Regions & Zones**:
    - Deploy resources across multiple zones within a region for high availability.
    - Use multi-region buckets for critical data that requires geo-redundancy.

## 3. Networking
- **VPC Design**:
    - Use **Custom Mode** VPC networks to have full control over IP ranges.
    - Avoid overlapping IP ranges between VPCs if VPC Peering or VPNs are anticipated.
    - Use **Private Google Access** to allow VMs without public IPs to reach Google APIs.
- **Security**:
    - Use **Firewall Rules** (or Policies) to strictly control ingress and egress traffic.
    - Minimize the use of external IP addresses; use Cloud NAT for outbound internet access from private instances.

## 4. Compute
- **Selection Criteria**:
    - **Cloud Run**: Best for stateless HTTP containers, event-driven functions, and rapid scaling (Serverless).
    - **GKE (Google Kubernetes Engine)**: Best for complex microservices architectures, stateful workloads, and needing full control over the cluster.
        - Use **Autopilot** mode for reduced operational overhead unless specific node configuration is required.
    - **Compute Engine (GCE)**: Best for legacy applications, specific kernel requirements, or databases not supported by managed services.

## 5. Storage
- **Cloud Storage (GCS)**:
    - Enable **Object Versioning** to protect against accidental overwrites or deletions.
    - Use **Lifecycle Policies** to automatically move old data to cheaper storage classes (e.g., Nearline, Coldline).
    - Ensure buckets are private by default; use specialized IAM bindings for public access if absolutely necessary.
- **Managed Databases**:
    - Prefer managed services like **Cloud SQL** (PostgreSQL/MySQL) or **Firestore** (NoSQL) over self-hosted databases on GCE.
    - Enable automated backups and high availability (HA) for production databases.

## 6. Observability
- **Logging**:
    - Use **Cloud Logging** (formerly Stackdriver).
    - Emit **Structured Logging** (JSON format) to enable rich filtering and analysis.
- **Monitoring & Alerting**:
    - specific metrics using **Cloud Monitoring**.
    - Set up alerts for critical usage thresholds (e.g., CPU, Memory, 5xx error rates) and budget spending.
    - Implement Health Checks for all services.
