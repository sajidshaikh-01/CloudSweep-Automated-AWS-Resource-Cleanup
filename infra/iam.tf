###############################################
# IAM ROLE FOR LAMBDA EXECUTION
###############################################
resource "aws_iam_role" "cronda_lambda_role" {
  name = "CrondaLambdaExecutionRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}


resource "aws_iam_policy" "cronda_lambda_policy" {
  name        = "CrondaLambdaPolicy"
  description = "Permissions for Lambda to scan and delete EC2, EBS volumes, and snapshots"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [

      # ----------------------------
      # EC2 INSTANCE OPERATIONS
      # ----------------------------
      {
        Effect = "Allow",
        Action = [
          "ec2:DescribeInstances",
          "ec2:TerminateInstances",
          "ec2:DescribeTags"
        ],
        Resource = "*"
      },

      # ----------------------------
      # EBS VOLUME OPERATIONS
      # ----------------------------
      {
        Effect = "Allow",
        Action = [
          "ec2:DescribeVolumes",
          "ec2:DeleteVolume"
        ],
        Resource = "*"
      },

      # ----------------------------
      # SNAPSHOT OPERATIONS
      # ----------------------------
      {
        Effect = "Allow",
        Action = [
          "ec2:DescribeSnapshots",
          "ec2:DeleteSnapshot"
        ],
        Resource = "*"
      },

      # ----------------------------
      # AMI CLEANUP OPERATIONS
      # ----------------------------
      {
        Effect = "Allow",
        Action = [
          "ec2:DescribeImages",
          "ec2:DeregisterImage"
        ],
        Resource = "*"
      },

      # ----------------------------
      # SNS Notifications
      # ----------------------------
      {
        Effect = "Allow",
        Action = [
          "sns:Publish"
        ],
        Resource = "*"
      },

      # ----------------------------
      # CloudWatch Logs
      # ----------------------------
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      },

      # ----------------------------
      # STS AssumeRole (optional)
      # ----------------------------
      {
        Effect = "Allow",
        Action = [
          "sts:AssumeRole"
        ],
        Resource = "*"
      }
    ]
  })
}


###############################################
# ATTACH POLICY TO ROLE
###############################################
resource "aws_iam_role_policy_attachment" "cronda_lambda_policy_attach" {
  role       = aws_iam_role.cronda_lambda_role.name
  policy_arn = aws_iam_policy.cronda_lambda_policy.arn
}
