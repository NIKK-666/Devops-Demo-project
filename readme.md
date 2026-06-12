# End-to-End DevSecOps Pipeline with GitOps & Live Monitoring

An enterprise-grade, fully automated DevSecOps continuous integration and continuous delivery (CI/CD) pipeline. This repository orchestrates the containerization, shift-left security verification, declarative deployment, and live instrumentation of a Python Flask application into a local Kubernetes (Minikube) cluster.

## 🏗️ Pipeline Architecture & Workflow

The architecture is built upon a zero-trust continuous delivery lifecycle using a strict shift-left security strategy combined with declarative GitOps operations:

1. **Code Commit / Pull Request**: Developers push updates to the GitHub repository, initiating the GitHub Actions CI workflows.
2. **Shift-Left Security & Quality Gates**: The codebase is evaluated simultaneously across 4 parallel validation checkers:
   * **Gitleaks**: Parses full historical deep branches to detect high-risk exposed application string constants, tokens, or credentials.
   * **Semgrep**: Leverages Automated AST pattern matching to identify systemic code vulnerabilities (SAST) like code injections or dangerous library inclusions.
   * **SonarQube Cloud**: Enforces structural maintainability tolerances, code duplicates, and holistic code-health metrics.
   * **Trivy**: Evaluates the target container layer definitions against public vulnerability tracking data, systematically blocking builds reporting `HIGH` or `CRITICAL` issues.
3. **Artifact Management**: Upon passing all 4 quality gates, a hardened Docker image is compiled via a multi-stage workflow and pushed to Docker Hub.
4. **GitOps Continuous Deployment**: `ArgoCD` automatically senses updates inside the infrastructure repository manifests, triggering a sync operation to the `Minikube` cluster with automated drift pruning and self-healing.
5. **Cloud-Native Observability**: A continuous metrics-scraping stack (`Prometheus` + `Grafana`) monitors cluster health and application metrics, backed by automated anomaly alerting via custom `PrometheusRule` objects.

---

## 🛠️ Tech Stack & Ecosystem

* **Application Framework:** Python, Flask, Prometheus Client Library
* **CI/CD & Automation:** GitHub Actions, Helm v3
* **Security & Quality Engines:** Gitleaks, Semgrep, SonarQube Cloud, Trivy
* **Containerization:** Docker (Multi-stage builds, Non-root execution safety)
* **Orchestration & Infrastructure:** Kubernetes (Minikube), Helm v3
* **Continuous Deployment:** ArgoCD (GitOps model)
* **Monitoring & Alerting:** Prometheus, Grafana, Custom PrometheusRule Alerts

---

## 🚀 Key Implementation Details

### 1. Hardened Container Architecture (`Dockerfile`)
The application is built using a secure multi-stage approach to eliminate build tools from the final runtime image, minimizing the attack surface:
* **Stage 1 (Builder):** Pulls a Python slim base, isolates dependencies, and compiles requirements under a strict local prefix context.
* **Stage 2 (Runtime):** Utilizes a hardened layer, provisions a dedicated non-root execution user (`appuser` with UID `10001`), copies only production runtimes, and drops standard system privileges.

### 2. Declarative GitOps Integration (`ArgoCD`)
Continuous deployment bypasses traditional push-based mechanisms. ArgoCD follows a pull-based model:
* Monitors the declarative Kubernetes manifests (Deployments, Services, Ingress).
* Detects any drift caused by manual mutations within the cluster and applies automated self-healing.
* Employs automated sync policies and pruning to ensure that the live state exactly reflects the git repository.

### 3. Observability, Instrumentation & Proactive Alerting
* **Application Metrics:** The Flask service initializes explicit `Counter` and `Histogram` metrics to track HTTP method performance metadata natively via a `/metrics` scrapable route.
* **Infrastructure Observability:** Pre-configured Grafana dashboards aggregate active memory profiles, pod availability matrices, and request throughput.
* **Incident Response Alerts:** Deployed a custom declarative `PrometheusRule` designed to capture pod thrashing or frequent crash loops. If threshold margins are compromised, an alert fires instantly in the monitoring panel to facilitate immediate triage.

---

## 🔧 Deployment Steps

1. **Initialize Cluster:** Start your local environment using `minikube start`.
2. **Install GitOps Operator:** Deploy ArgoCD via Helm or official manifests into an `argocd` namespace.
3. **Deploy Observability Stack:** Use Helm v3 to install the `kube-prometheus-stack` to provision Prometheus and Grafana instances.
4. **Configure Argo Application:** Apply your custom ArgoCD application manifest pointing to your infrastructure path to initialize tracking and deployment automation.
