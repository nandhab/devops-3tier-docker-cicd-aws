# 🚀 Full DevOps Project Plan: 3-Tier Architecture (AWS Free Tier Compatible, Fully Dockerized)

## ⬆️ Overview

A complete DevOps project using a **3-tier architecture**, fully compatible with AWS Free Tier and **containerized using Docker**:

* **Frontend**: Angular or NGINX hosted inside a Docker container
* **Backend**: Python API (based on Flask or FastAPI) in a Docker container
* **Database**: MySQL/PostgreSQL containerized and managed via Docker Compose

All services run on a single EC2 instance (t2.micro), orchestrated with Docker Compose.
Includes robust **CI/CD pipelines** using both **GitHub Actions** and **Jenkins**.

---

## 📆 Week-by-Week Breakdown

### ✅ Week 1: App Development & Containerization

* **Deliverables**:

  * Angular frontend (or NGINX static site)
  * Python REST API (Flask or FastAPI)
  * MySQL or PostgreSQL in Docker
  * Dockerfile and `docker-compose.yml` for all services
  * GitHub repository
* **Expected Outcome**:

  * Full app runs locally using Docker Compose
  * GitHub version control setup
* **Folder Structure**:

```bash
devops-project/
├── frontend-angular/
│   ├── Dockerfile
├── backend-flask/
│   ├── Dockerfile
│   └── app.py
├── database/
│   └── init.sql
├── docker-compose.yml
├── README.md
```

* **Tools**: Angular or NGINX, Flask or FastAPI, MySQL/PostgreSQL, Docker, Docker Compose, Git, GitHub

---

### ✅ Week 2: Infrastructure Setup with Terraform + Manual Docker Deployment

* **Deliverables**:

  * Terraform scripts for:

    * EC2 (Free Tier: t2.micro)
    * Basic IAM setup (Free Tier)
  * Manually SSH into EC2
  * Install Docker & Docker Compose manually
  * Run the `docker-compose.yml` to validate VM setup
* **Expected Outcome**:

  * Free Tier EC2 is provisioned and reachable
  * Application stack is successfully deployed manually
* **Folder Structure**:

```bash
terraform/
├── provider.tf
├── ec2.tf
├── variables.tf
├── outputs.tf
```

* **Tools**: Terraform, AWS EC2 (t2.micro), IAM, Docker CLI, SSH

---

### ✅ Week 3: Configuration & Deployment with Ansible

* **Deliverables**:

  * Ansible playbook for EC2 provisioning:

    * Install Docker and Docker Compose
    * Clone the app repo
    * Use Docker Compose to deploy all services (frontend, backend, DB)
* **Expected Outcome**:

  * All app components deployed via containers on EC2 instance
* **Folder Structure**:

```bash
ansible/
├── inventory.ini
├── site.yml
└── roles/
    ├── docker/tasks/main.yml
    └── app/tasks/main.yml
```

* **Tools**: Ansible, Docker, Docker Compose

---

### ✅ Week 4: CI/CD with GitHub Actions + Jenkins

* **Deliverables**:

  * GitHub Actions workflows:

    * Build and test Docker images
    * Deploy updated containers to EC2 via SSH
  * Jenkins installed on EC2 as an alternative CI server
  * Sample Jenkins pipeline (pipeline as code)
  * CI/CD dashboard and status badges in README
* **Expected Outcome**:

  * Both GitHub Actions and Jenkins demonstrate CI/CD capabilities
  * Builds are triggered automatically on push
* **Folder Structure**:

```bash
.github/
└── workflows/
    ├── deploy-frontend.yml
    └── deploy-backend.yml
jenkins/
└── Jenkinsfile
```

* **Tools**: GitHub Actions, Jenkins, AWS CLI, SSH, Docker

---

### ✅ Week 5: SSL, Monitoring, Documentation & Project Finalization

* **Deliverables**:

  * NGINX reverse proxy container configuration
  * SSL/TLS encryption using Let’s Encrypt (Certbot deployed in Docker)
  * Prometheus and Grafana (in Docker containers)
  * Final README and architecture diagram
  * GitHub repo badges for CI, license, and version
* **Expected Outcome**:

  * HTTPS-secured app
  * Lightweight container-based monitoring + documentation
  * Portfolio-ready project with full updates and documentation
* **Folder Structure**:

```bash
ansible/roles/nginx/templates/
└── site.conf.j2
monitoring/
├── prometheus.yml
└── docker-compose-monitoring.yml
architecture.png
README.md
```

* **Tools**: Certbot (Docker), NGINX (Docker), Prometheus, Grafana, Docker Compose, Markdown

---

### ✅ Week 6: Kubernetes and Helm Charts (Local Testing)

* **Deliverables**:

  * Helm charts for frontend, backend, and DB
  * Minikube or kind used to test Kubernetes deployment locally
  * Optional: transition `docker-compose` services to Kubernetes manifests
* **Expected Outcome**:

  * 3-tier app is deployable and testable on a local Kubernetes cluster
* **Folder Structure**:

```bash
k8s/
├── helm/
│   ├── frontend/
│   ├── backend/
│   └── database/
└── manifests/
    └── all-services.yaml
```

* **Tools**: Kubernetes, Helm, Minikube/kind, kubectl

---

## 🧾 Summary Table

| Week | Focus                               | Tools/Tech                                              | Outcomes                                      |
| ---- | ----------------------------------- | ------------------------------------------------------- | --------------------------------------------- |
| 1    | App + Docker                        | Angular/NGINX, Flask or FastAPI, MySQL/Postgres, Docker | Fully containerized 3-tier app locally        |
| 2    | Terraform Infra + Manual Docker     | Terraform, EC2 (t2.micro), IAM, Docker CLI, SSH         | EC2 up, Docker stack deployed manually        |
| 3    | Ansible Deployment                  | Ansible, Docker Compose                                 | App deployed automatically via Ansible        |
| 4    | CI/CD with GitHub Actions + Jenkins | GitHub Actions, Jenkins, SSH, Docker                    | Automated deployment pipelines working        |
| 5    | SSL + Monitoring + Docs             | Certbot, NGINX, Prometheus, Grafana, Docker, Markdown   | Secure, monitored app with documentation      |
| 6    | Kubernetes + Helm (Local)           | Kubernetes, Helm, Minikube/kind                         | App deployable/testable via Helm on local K8s |

---

📁 Final Project Directory Structure

```bash
devops-3tier-docker-cicd-aws/
├── frontend-angular/           # Angular or static NGINX frontend
│   └── Dockerfile
├── backend-python/             # Flask or FastAPI backend
│   ├── Dockerfile
│   └── app.py
├── database/                   # Database initialization
│   └── init.sql
├── docker-compose.yml          # Compose file for all services
├── terraform/                  # Infrastructure as Code
│   ├── provider.tf
│   ├── ec2.tf
│   ├── variables.tf
│   └── outputs.tf
├── ansible/                    # Configuration management
│   ├── inventory.ini
│   ├── site.yml
│   └── roles/
│       ├── docker/tasks/main.yml
│       ├── app/tasks/main.yml
│       └── nginx/templates/site.conf.j2
├── .github/                    # GitHub Actions workflows
│   └── workflows/
│       ├── deploy-frontend.yml
│       └── deploy-backend.yml
├── jenkins/                    # Jenkins CI pipeline
│   └── Jenkinsfile
├── monitoring/                 # Prometheus and Grafana setup
│   ├── prometheus.yml
│   └── docker-compose-monitoring.yml
├── k8s/                        # Kubernetes and Helm setup
│   ├── helm/
│   │   ├── frontend/
│   │   ├── backend/
│   │   └── database/
│   └── manifests/all-services.yaml
├── architecture.png            # Architecture diagram
└── README.md                   # Project documentation
```

🎉 Happy Learning! 🚀

