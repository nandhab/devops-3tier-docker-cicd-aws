# 🚀 Ansible-Based EC2 Deployment

This project automates the provisioning and deployment of a containerized full-stack application on an EC2 instance using Ansible, Docker, and Docker Compose.

---

## 📁 Project Structure

```
ansible/
├── inventory.ini                   # EC2 host information
├── site.yml                        # Master playbook
└── roles/
├── docker/                         # Installs Docker & Compose
│ └── tasks/main.yml
└── app/                            # Clones repo and deploys app
  └── tasks/main.yml
```


---

## 🧰 Tools Used

- Ansible
- Amazon EC2 (Amazon Linux 2)
- Docker
- Docker Compose (via Python module)
- Git

---

## ⚙️ Prerequisites

- A running EC2 instance (Amazon Linux 2)
- SSH access with a private key (`.pem`)
- Control machine with Ansible installed (e.g., WSL, Linux, or macOS)
- Public IP of your EC2 instance
- Application repository with a valid `docker-compose.yml`

---

## 🔧 Setup Instructions

```
1. Edit `inventory.ini`  
   Add your EC2 instance IP and SSH key path.

2. Edit `site.yml`  
   Define roles to run in order: `docker`, then `app`.

3. Configure `docker/tasks/main.yml`  
   Install and configure Docker, pip, and Python modules required by Ansible.

4. Configure `app/tasks/main.yml`  
   Clone your app's Git repo and deploy using Docker Compose.

5. Install Ansible collection (on control machine):
   ansible-galaxy collection install community.docker
```

🚀 Deployment
Run the Ansible playbook from the ansible/ directory:

```
ansible-playbook -i inventory.ini site.yml
```

📡 Verifying Deployment
SSH into your EC2 instance:

```
ssh -i ~/.ssh/your-key.pem ec2-user@<EC2_PUBLIC_IP>
```

Then check running containers:

```
docker ps
```


