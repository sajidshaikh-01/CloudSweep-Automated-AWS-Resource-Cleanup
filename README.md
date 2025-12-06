# 🧹 CloudSweep – Automated AWS Resource Cleanup (Serverless)

CloudSweep – AWS Cleanup Automation (Lambda • Terraform • Python • Cross-Account)

Developed a serverless automation tool that scans and deletes stale AWS resources across multiple AWS accounts using a centralized Lambda with STS AssumeRole. Cleanup includes EC2 instances, unattached EBS volumes, old snapshots, unused AMIs, and unassociated Elastic IPs. Implemented dry-run mode, SNS alerts, CloudWatch logging, and IAM least-privilege roles. All infrastructure was provisioned with Terraform using S3 + DynamoDB backend.
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

