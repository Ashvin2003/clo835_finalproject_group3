# CLO835 Terraform Infrastructure Deployment

This repository provisions AWS infrastructure for the CLO835 project and deploys Dockerized web and database containers to EC2 using Terraform and GitHub Actions. The project is done by Group 3 and the members are:

- Ashvin Ravi
- Wanigamuni Senindu Kithmal Mendis
- Jasleen Kour Dhir

---

## 📂 Clone the Repository
```bash
git clone <your-repo-url>
cd clo835-ashvinravi-terraformcode
```

---

## 🔑 Generate SSH Keys
Create SSH keys for EC2 access inside the `instances` directory:
```bash
cd instances
ssh-keygen -t rsa -b 2048 -f clo835_key
```

---

## 🛠️ Install Terraform
Run the following commands to install Terraform on Amazon Linux 2:
```bash
sudo yum update -y
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum install -y terraform
terraform -version
```

---

## 🌐 Deploy Networking Module
Initialize and apply the networking resources:
```bash
cd networking
terraform init
terraform validate
terraform plan
terraform apply
```

---

## 💻 Deploy Instances Module
Initialize and apply the EC2 instances and related resources:
```bash
cd instances
terraform init
terraform validate
terraform plan
terraform apply
```

---

## ✅ Verify AWS Resources
After applying both modules, confirm that the VPC, subnets, security groups, and EC2 instances have been created in the AWS Management Console.

---

## 🔐 Configure GitHub Secrets
Update the repository secrets to match your active AWS session and infrastructure:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_SESSION_TOKEN
- AWS_ACCOUNT_ID
- EC2_PUBLIC_DNS
- EC2_PUBLIC_IP
- ECR_MYSQL_REPO (URI of the MySQL ECR repo)
- ECR_WEB_REPO (URI of the Web App ECR repo)
- SSH_PRIVATE_KEY (contents of clo835_key)

---

## 🚀 Run the GitHub Action
Trigger the **Build, Push to ECR, Deploy to EC2** workflow from the **Actions** tab in GitHub.

---

## 🔍 Expected Outcome
- The GitHub Action will build Docker images, push them to ECR, and deploy containers to EC2.
- For unit testing, access the web application in a browser at:

```
http://<EC2_PUBLIC_IP>:8080
```

📌 **Note:** Port `8080` is the port exposed by the web application container.
