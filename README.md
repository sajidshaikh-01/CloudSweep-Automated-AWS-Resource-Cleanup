# 🧹 CloudSweep – Automated AWS Resource Cleanup (Serverless)

CloudSweep is a **serverless, multi-account cloud cleanup automation tool** designed to reduce AWS cost by identifying and deleting unused or stale cloud resources.  
It uses AWS Lambda, EventBridge, SNS, and Terraform to create a fully automated, scalable, and production-ready cleanup system.

---

# 🚀 Features

### 🔍 Resource Scanning
CloudSweep automatically scans:

- 🖥 **EC2 instances** older than a threshold  
- 💽 **Unattached EBS volumes**  
- 📸 **Aged EBS snapshots**  
- 🖼 **Unused AMIs**  
- 🌐 **Unassociated Elastic IPs**

---

## ⚠️ Safe-Delete Workflow
- `DRY_RUN=true` → only reports actions (no deletion)  
- `DRY_RUN=false` → deletes stale resources  
- Tag-based protection using:  
  - `Environment=production`  
  - `Backup=true`  
  - `DoNotDelete=true`

---

## 🌍 Multi-Account Support
CloudSweep supports **cross-account cleanup** using STS AssumeRole:

- Central Lambda assumes roles into Dev, QA, Staging accounts  
- Scans all accounts using temporary credentials  
- Provides unified cleanup automation for enterprise setups  

---





---

# 📦 Tech Stack

- **AWS Lambda** – Python automation logic  
- **EventBridge** – Scheduled cleanup trigger  
- **SNS** – Email notifications  
- **IAM** – Secure least-privilege roles  
- **Terraform** – Complete IaC deployment  
- **Python + boto3** – AWS automation  

---
Cleanup Targets
---
| Resource      | Action                                |
| ------------- | ------------------------------------- |
| EC2 Instances | Terminate if older than threshold     |
| EBS Volumes   | Delete if unattached                  |
| Snapshots     | Delete if old & not backup-tagged     |
| AMIs          | Deregister + delete backing snapshots |
| Elastic IPs   | Release if unassociated               |


👨‍💻 Author
```
Sajid Shaikh
```
DevOps Engineer & Cloud Automation Enthusiast

