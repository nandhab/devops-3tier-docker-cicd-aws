# 🚀 GitHub Actions CI/CD for 3-Tier Docker App

This repository uses **GitHub Actions** to implement a CI/CD pipeline for deploying a Dockerized 3-tier web application (frontend, backend, and PostgreSQL database) to a remote server (e.g., AWS EC2).

The automation is defined in:

```
.github/workflows/deploy-3tier-app.yml
```

---

## 📌 Purpose

The GitHub Actions workflow automates the following:

- Cloning the latest code from GitHub
- Building Docker images for the frontend and backend services
- Connecting via SSH to a remote server (e.g., AWS EC2)
- Pulling updated code and restarting the application using Docker Compose

---

## ⚙️ Workflow Trigger

This workflow is triggered on every:

- `push` to the branch
- `pull_request` to the branch

This ensures that all updates are automatically built and deployed when merged to the main line.

---

## 🔄 Workflow Overview

The file: `.github/workflows/deploy-3tier-app.yml` contains the following steps:

### 1. **Checkout Code**

```yaml
- uses: actions/checkout@v3
```

Clones the contents of the repository into the GitHub Actions runner.

---

### 2. **Set Up Docker Build Environment**

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v2
```

Enables advanced Docker builds using BuildKit, useful for multi-architecture or cache-optimized builds.

---

### 3. **Authenticate with Remote Server**

```yaml
- name: Set up SSH
  uses: webfactory/ssh-agent@v0.5.4
```

Uses SSH keys stored in repository secrets (e.g., `EC2_KEY`) to connect securely to your remote server (e.g., AWS EC2).

---

### 4. **Deploy to Remote Host via SSH**

```yaml
- name: Deploy app to EC2
  run: |
    ssh -o StrictHostKeyChecking=no ec2-user@$EC2_HOST << 'EOF'
      cd /home/ec2-user/devops-3tier-docker-cicd-aws
      git pull origin main
      docker-compose down
      docker-compose up --build -d
    EOF
```

Runs a remote script over SSH that:

- Pulls the latest source code
- Stops running containers
- Rebuilds and restarts the app stack using Docker Compose

---

## 🔐 Required GitHub Secrets

To enable secure deployment, the following secrets must be configured in your GitHub repository:

| Secret Name | Description                              |
|-------------|------------------------------------------|
| `EC2_HOST`  | Public IP or DNS of your EC2/server      |
| `EC2_USER`  | EC2 Instance Username                    |
| `EC2_KEY`   | Private key used to SSH into your server |


---

## 📁 Deployment Target

By default, the workflow expects your target server (e.g., AWS EC2) to:

- Have Docker and Docker Compose installed
- Be accessible via SSH
- Have the repository cloned in `/home/ec2-user/devops-3tier-docker-cicd-aws`

---

## ✅ Summary

- ✅ CI/CD is handled entirely through GitHub Actions
- ✅ No manual steps are required to deploy after pushing to `main`
- ✅ All application tiers (frontend, backend, DB) are managed via Docker Compose
- ✅ Secure and automated delivery to a remote server

