import boto3
import os
import datetime
import json

# -----------------------------------------
# Configuration
# -----------------------------------------
THRESHOLD_HOURS = int(os.environ.get("THRESHOLD_HOURS", 3))
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() == "true"
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "")
REGION = os.environ.get("AWS_REGION", "us-east-1")

sns_client = boto3.client("sns")
ec2_client = boto3.client("ec2")


# -----------------------------------------
# Helper Functions
# -----------------------------------------

def notify(message):
    """Send logs + SNS notification"""
    print(message)
    if SNS_TOPIC_ARN:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Cronda Cleanup Notification"
        )

def get_age_hours(creation_time):
    """Calculate resource age in hours"""
    now = datetime.datetime.utcnow().replace(tzinfo=None)
    created = creation_time.replace(tzinfo=None)
    return (now - created).total_seconds() / 3600


# -----------------------------------------
# SCAN — EC2 Instances
# -----------------------------------------

def scan_ec2_instances():
    stale_instances = []
    response = ec2_client.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            launch_time = instance['LaunchTime']
            age_hours = get_age_hours(launch_time)

            # Ignore production resources
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            env = tags.get('Environment', '').lower()

            if env == "production":
                continue

            if age_hours > THRESHOLD_HOURS:
                stale_instances.append({
                    "instance_id": instance_id,
                    "age_hours": age_hours,
                })

    return stale_instances


# -----------------------------------------
# DELETE — EC2 Instances
# -----------------------------------------

def delete_ec2_instance(instance_id):
    if DRY_RUN:
        notify(f"[DRY RUN] Would terminate EC2 instance: {instance_id}")
        return

    ec2_client.terminate_instances(InstanceIds=[instance_id])
    notify(f"Terminated EC2 instance: {instance_id}")


# -----------------------------------------
# SCAN — Unattached EBS Volumes
# -----------------------------------------

def scan_unattached_volumes():
    stale_volumes = []
    response = ec2_client.describe_volumes(
        Filters=[{"Name": "status", "Values": ["available"]}]  # unattached volumes
    )

    for volume in response['Volumes']:
        volume_id = volume['VolumeId']
        create_time = volume['CreateTime']
        age_hours = get_age_hours(create_time)

        if age_hours > THRESHOLD_HOURS:
            stale_volumes.append({
                "volume_id": volume_id,
                "age_hours": age_hours,
            })

    return stale_volumes


# -----------------------------------------
# DELETE — EBS Volumes
# -----------------------------------------

def delete_volume(volume_id):
    if DRY_RUN:
        notify(f"[DRY RUN] Would delete EBS volume: {volume_id}")
        return

    ec2_client.delete_volume(VolumeId=volume_id)
    notify(f"Deleted EBS volume: {volume_id}")


# -----------------------------------------
# SCAN — Unused Snapshots
# -----------------------------------------

def scan_unused_snapshots():
    stale_snapshots = []
    
    response = ec2_client.describe_snapshots(OwnerIds=['self'])

    for snapshot in response['Snapshots']:
        snap_id = snapshot['SnapshotId']
        start_time = snapshot['StartTime']
        age_hours = get_age_hours(start_time)

        # Skip snapshots with tags like Backup=true
        tags = {tag['Key']: tag['Value'] for tag in snapshot.get('Tags', [])}
        if tags.get("Backup", "").lower() == "true":
            continue

        if age_hours > THRESHOLD_HOURS:
            stale_snapshots.append({
                "snapshot_id": snap_id,
                "age_hours": age_hours,
            })

    return stale_snapshots


# -----------------------------------------
# DELETE — Snapshots
# -----------------------------------------

def delete_snapshot(snapshot_id):
    if DRY_RUN:
        notify(f"[DRY RUN] Would delete snapshot: {snapshot_id}")
        return

    ec2_client.delete_snapshot(SnapshotId=snapshot_id)
    notify(f"Deleted snapshot: {snapshot_id}")


# -----------------------------------------
# MAIN HANDLER — ENTRY POINT
# -----------------------------------------

def lambda_handler(event, context):

    notify(f"Cronda execution started. DRY_RUN={DRY_RUN}, Threshold={THRESHOLD_HOURS} hours")

    # -----------------------------
    # EC2 Instance Cleanup
    # -----------------------------
    instances = scan_ec2_instances()
    for inst in instances:
        delete_ec2_instance(inst["instance_id"])

    # -----------------------------
    # EBS Volume Cleanup
    # -----------------------------
    volumes = scan_unattached_volumes()
    for vol in volumes:
        delete_volume(vol["volume_id"])

    # -----------------------------
    # Snapshot Cleanup
    # -----------------------------
    snapshots = scan_unused_snapshots()
    for snap in snapshots:
        delete_snapshot(snap["snapshot_id"])

    notify("Cronda run completed.")
    return {"status": "completed"}
