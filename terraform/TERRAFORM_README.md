# 🚀 AWS EC2 Terraform Project

Provision an AWS EC2 instance with:

✅ Security group allowing ports 22, 8080, 8000  
✅ User-data installing Git, Docker, Docker Compose  

---

## 📖 Table of Contents

1. [📌 Terraform Basics and Modules](#terraform-basics-and-modules)  
2. [📌 High-Level Plan of Modules Used Here](#high-level-plan-of-modules-used-here)  
3. [📌 Explanation of the Terraform Configuration](#explanation-of-the-terraform-configuration)  
4. [📌 Prerequisites](#prerequisites)  
5. [📌 How to Deploy](#how-to-deploy)  

---

## 📌 Terraform Basics and Modules

**Terraform** is an Infrastructure as Code (IaC) tool that lets you declare cloud infrastructure in `.tf` files and provision it automatically.  

- **Resources** are the actual things you want (EC2, S3, etc.).  
- **Providers** tell Terraform which cloud to use (AWS, Azure, etc.).  
- **Modules** are reusable, logical groupings of resources (like functions in code).  

> *In this simple project we don't use separate modules, but the design is modular in that each .tf file separates concerns.*

---

## 📌 High-Level Plan of Modules Used Here

This project is structured in *logical modules* (not separate Terraform modules, but separated files for clarity):

```
├── provider.tf → AWS provider configuration
├── variables.tf → Input variables
├── ec2.tf → Resources (EC2 instance, security group)
├── outputs.tf → Outputs (public IP, instance ID)
```


If you wanted to, you could later refactor this into true Terraform modules (e.g. a separate EC2 module).  

---

## 📌 Explanation of the Terraform Configuration

### 1️⃣ `provider.tf`
- Configures the AWS provider with a specified region.

---

### 2️⃣ `variables.tf`
- Defines input variables:
  - `region`: AWS region to deploy to.
  - `instance_type`: Type of EC2 instance.
  - `key_name`: Existing EC2 Key Pair for SSH access.

---

### 3️⃣ `ec2.tf`
- **Data Source**:
  - Fetches the latest Amazon Linux 2 AMI.
- **Security Group**:
  - Allows inbound on ports 22 (SSH), 8080, and 8000.
  - Allows all outbound.
- **EC2 Instance**:
  - Uses the selected AMI.
  - Attaches the security group.
  - Sets up user data script that:
    - Updates packages.
    - Installs Git.
    - Installs Docker, starts and enables the service.
    - Installs Docker Compose.

---

### 4️⃣ `outputs.tf`
- Prints:
  - EC2 Instance ID
  - EC2 Public IP

---

## 📌 Prerequisites

✅ **AWS Account**  
✅ **AWS Access Key & Secret Key**  
✅ **Existing EC2 Key Pair in AWS**
- Needed to SSH into the instance.
- Find it in AWS EC2 Console → Key Pairs.

✅ **Terraform installed**
- [Install Terraform](https://developer.hashicorp.com/terraform/downloads)

✅ **AWS CLI installed and configured (recommended)**
- [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Configure credentials:

```
aws configure
```

This sets:
AWS Access Key ID
AWS Secret Access Key
Default region

## 📌 How to Deploy

### 1️⃣ Clone or download this repo

```
git clone <repo-url>
cd <project-folder>
```

### 2️⃣ Initialize Terraform

```
terraform init
```
Downloads AWS provider plugins.

### 3️⃣ Plan (Optional but recommended)

```
terraform plan -var="key_name=YOUR_KEY_PAIR_NAME"
```
Shows what Terraform will do.

### 4️⃣ Apply
Approve when prompted. Your EC2 instance will launch.
```
terraform apply -var="key_name=YOUR_KEY_PAIR_NAME"
```

Outputs will show:
```
Instance ID
Public IP
```

### 5️⃣ Connect
SSH into your instance using the Key Pair you specified:

```
ssh -i /path/to/YOUR_KEY_PAIR.pem ec2-user@<Public IP>
```

## ✅ Notes
The instance runs Amazon Linux 2.

User-data installs:
- Git
- Docker
- Docker Compose

## 🧩 Example Usage
```
terraform apply -var="key_name=my-existing-keypair"
```

Output:
```
instance_id = "i-xxxxxxxxxxxxxxxxx"
instance_public_ip = "3.88.xxx.xxx"
```

SSH:

```
ssh -i my-existing-keypair.pem ec2-user@3.88.xxx.xxx
```

## ⚠️ Clean-up
To avoid charges:

```
terraform destroy -var="key_name=YOUR_KEY_PAIR_NAME"
```