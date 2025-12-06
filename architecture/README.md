                       ┌─────────────────────────┐
                       │    Amazon EventBridge    │
                       │  (Cron - every 30 mins)  │
                       └──────────────┬───────────┘
                                      │ Triggers
                                      ▼
                         ┌─────────────────────────┐
                         │      AWS Lambda         │
                         │     (CloudSweep.py)     │
                         └──────────────┬──────────┘
                                        │
      ┌─────────────────────────────────────────────────────────────────┐
      │                         Cleanup Logic                            │
      │─────────────────────────────────────────────────────────────────│
      │ 1. Describe EC2 Instances → Check age → Delete stale            │
      │ 2. Describe EBS Volumes (unattached) → Delete                   │
      │ 3. Describe Snapshots → Delete old ones                         │
      │ 4. Describe AMIs → Deregister unused → Delete snapshots         │
      │ 5. Describe Elastic IPs (unassociated) → Release                │
      └─────────────────────────────────────────────────────────────────┘
                                        │
                     ┌──────────────────┴───────────────────┐
                     │                                      │
                     ▼                                      ▼
       ┌─────────────────────────┐               ┌─────────────────────────┐
       │   Amazon SNS Topic      │               │     CloudWatch Logs     │
       │  (Cleanup Notifications)│               │ (Execution Log, Errors) │
       └──────────────┬──────────┘               └─────────────────────────┘
                      │
                      ▼
          ┌──────────────────────┐
          │ Email / Slack Alerts │
          └──────────────────────┘


       ┌─────────────────────────────────────────────────────────────────┐
       │                    Terraform Infrastructure                     │
       │─────────────────────────────────────────────────────────────────│
       │ • S3 Backend + DynamoDB Lock                                   │
       │ • IAM Roles + Least Privilege Policies                         │
       │ • Lambda Deployment + ZIP Upload                               │
       │ • EventBridge Scheduler                                        │
       │ • SNS Topic Subscription                                       │
       └─────────────────────────────────────────────────────────────────┘


Title: CloudSweep – AWS Resource Cleanup Automation

Components:
1. EventBridge (Scheduled Rule: every 30 minutes)
2. Lambda Function (Python – cronda.py)
3. Cleanup Logic:
   - EC2 Instance Cleanup
   - Unattached EBS Volume Cleanup
   - Old EBS Snapshot Cleanup
   - Unused AMI Cleanup (Deregister + delete snapshot)
   - Unassociated Elastic IP Cleanup
4. SNS Topic (Email/Slack Alerts)
5. CloudWatch Logs (Execution logs and errors)
6. Terraform Infrastructure Layer:
   - S3 backend for state storage
   - DynamoDB table for state locking
   - IAM roles & policies
   - Lambda deployment
   - SNS topic + subscription
   - EventBridge schedule

Flow:
EventBridge → Lambda → Cleanup Logic → SNS Notifications + CloudWatch Logs
Terraform provisions everything.

Theme:
AWS official icons, blue/orange color scheme
