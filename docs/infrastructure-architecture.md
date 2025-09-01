# Infrastructure Architecture: AWS External Agent for Bird.com

## Infrastructure Overview

This document details the AWS infrastructure architecture for deploying external agents that maintain full Bird.com API compatibility while providing enhanced multimodal capabilities.

## AWS Account Structure

### Multi-Account Strategy
```
Root Account (Management)
├── Production Account (bird-agent-prod)
├── Staging Account (bird-agent-staging)  
├── Development Account (bird-agent-dev)
├── Security Account (bird-agent-security)
└── Logging Account (bird-agent-logging)
```

### Account Responsibilities
- **Production**: Live agent services and production workloads
- **Staging**: Pre-production testing and validation
- **Development**: Development and testing environment
- **Security**: Centralized security monitoring and compliance
- **Logging**: Centralized log aggregation and analysis

## Network Architecture

### VPC Design

```yaml
VPC Configuration:
  CIDR: 10.0.0.0/16
  DNS Resolution: Enabled
  DNS Hostnames: Enabled
  
Availability Zones: 3 (us-east-1a, us-east-1b, us-east-1c)

Subnets:
  Public Subnets:
    - 10.0.1.0/24 (AZ-a) - NAT Gateway, ALB
    - 10.0.2.0/24 (AZ-b) - NAT Gateway, ALB  
    - 10.0.3.0/24 (AZ-c) - NAT Gateway, ALB
  
  Private App Subnets:
    - 10.0.11.0/24 (AZ-a) - ECS Services
    - 10.0.12.0/24 (AZ-b) - ECS Services
    - 10.0.13.0/24 (AZ-c) - ECS Services
  
  Private Data Subnets:
    - 10.0.21.0/24 (AZ-a) - RDS, ElastiCache
    - 10.0.22.0/24 (AZ-b) - RDS, ElastiCache
    - 10.0.23.0/24 (AZ-c) - RDS, ElastiCache
```

### Network Security

#### Security Groups
```yaml
API Gateway Security Group (sg-api-gateway):
  Inbound:
    - Port 443 (HTTPS) from 0.0.0.0/0
    - Port 80 (HTTP) from 0.0.0.0/0 (redirect to 443)
  Outbound:
    - All traffic to ALB Security Group

Application Load Balancer Security Group (sg-alb):
  Inbound:
    - Port 443 from API Gateway SG
    - Port 80 from API Gateway SG
  Outbound:
    - Port 8080 to ECS Services SG

ECS Services Security Group (sg-ecs):
  Inbound:
    - Port 8080 from ALB SG
    - Port 8081 from ALB SG (health checks)
  Outbound:
    - Port 443 to Internet (AWS API calls)
    - Port 5432 to Database SG
    - Port 6379 to Cache SG

Database Security Group (sg-database):
  Inbound:
    - Port 5432 from ECS Services SG
    - Port 5432 from Lambda SG
  Outbound:
    - None (no outbound rules needed)

Cache Security Group (sg-cache):
  Inbound:
    - Port 6379 from ECS Services SG
    - Port 6379 from Lambda SG
  Outbound:
    - None (no outbound rules needed)

Lambda Security Group (sg-lambda):
  Inbound:
    - None (Lambda functions don't accept inbound connections)
  Outbound:
    - Port 443 to Internet (AWS API calls)
    - Port 5432 to Database SG
    - Port 6379 to Cache SG
```

#### Network ACLs
```yaml
Public Subnet NACL:
  Inbound:
    100: Allow HTTP (80) from 0.0.0.0/0
    110: Allow HTTPS (443) from 0.0.0.0/0
    120: Allow SSH (22) from Management IP
    130: Allow Ephemeral Ports (1024-65535) from 0.0.0.0/0
  Outbound:
    100: Allow all traffic to 0.0.0.0/0

Private App Subnet NACL:
  Inbound:
    100: Allow all traffic from 10.0.0.0/16
    110: Allow HTTPS (443) from 0.0.0.0/0
  Outbound:
    100: Allow all traffic to 0.0.0.0/0

Private Data Subnet NACL:
  Inbound:
    100: Allow all traffic from 10.0.0.0/16
  Outbound:
    100: Allow all traffic to 10.0.0.0/16
```

### Internet Connectivity

#### NAT Gateway Configuration
```yaml
NAT Gateways:
  - Subnet: Public-AZ-a (10.0.1.0/24)
    Elastic IP: eipalloc-nat-a
    
  - Subnet: Public-AZ-b (10.0.2.0/24) 
    Elastic IP: eipalloc-nat-b
    
  - Subnet: Public-AZ-c (10.0.3.0/24)
    Elastic IP: eipalloc-nat-c

Route Tables:
  Public Route Table:
    - 10.0.0.0/16 -> Local
    - 0.0.0.0/0 -> Internet Gateway
  
  Private App Route Table (AZ-a):
    - 10.0.0.0/16 -> Local
    - 0.0.0.0/0 -> NAT Gateway (AZ-a)
  
  Private Data Route Table:
    - 10.0.0.0/16 -> Local
    - No internet access
```

## Compute Infrastructure

### ECS Cluster Configuration

```yaml
ECS Cluster: bird-agent-cluster
Capacity Provider Strategy:
  - FARGATE (70% weight)
  - FARGATE_SPOT (30% weight)

Service Configuration:
  Conversation Manager:
    Task Definition: conversation-manager:latest
    Desired Count: 3
    Min Capacity: 2
    Max Capacity: 20
    CPU: 1024 (1 vCPU)
    Memory: 2048 MB
    
    Auto Scaling:
      Target CPU: 70%
      Target Memory: 80%
      Scale Out Cooldown: 300s
      Scale In Cooldown: 900s
    
    Load Balancer:
      Target Group: conversation-manager-tg
      Health Check: /health
      Health Check Interval: 30s
      Healthy Threshold: 2
      Unhealthy Threshold: 3

  Multimodal Processor:
    Task Definition: multimodal-processor:latest
    Desired Count: 2
    Min Capacity: 1
    Max Capacity: 10
    CPU: 2048 (2 vCPU)
    Memory: 4096 MB
    GPU: 1 (if available)
    
    Auto Scaling:
      Target CPU: 80%
      Target Memory: 85%
      Custom Metric: Queue Depth
```

### Lambda Functions Infrastructure

```yaml
Event Processor Function:
  Runtime: python3.11
  Architecture: x86_64
  Memory: 1024 MB
  Timeout: 15 minutes
  Reserved Concurrency: 100
  Environment Variables:
    - DYNAMODB_TABLE: agent-events
    - SNS_TOPIC: arn:aws:sns:region:account:notifications
  
  VPC Configuration:
    Subnets: [Private App Subnets]
    Security Groups: [Lambda SG]
  
  Dead Letter Queue:
    SQS Queue: event-processor-dlq
    Max Receive Count: 3

Multimodal Analysis Function:
  Runtime: python3.11
  Architecture: x86_64
  Memory: 3008 MB
  Timeout: 5 minutes
  Reserved Concurrency: 50
  Provisioned Concurrency: 10
  
  Layers:
    - AWS Lambda Powertools Python
    - OpenCV Python Layer
    - Custom AI Models Layer
  
  Environment Variables:
    - BEDROCK_REGION: us-east-1
    - S3_BUCKET: agent-media-bucket
    - MODEL_CACHE: /tmp/models
```

## Storage Architecture

### S3 Storage Design

```yaml
Buckets:
  agent-media-bucket:
    Purpose: Multimodal content storage
    Encryption: AES-256 (SSE-S3)
    Versioning: Enabled
    Lifecycle Policy:
      - Delete incomplete uploads after 7 days
      - Transition to IA after 30 days
      - Transition to Glacier after 90 days
      - Delete after 365 days
    
    Folders:
      - images/
      - audio/
      - documents/
      - processed/
      - temp/ (7-day retention)

  agent-logs-bucket:
    Purpose: Application and access logs
    Encryption: AES-256 (SSE-S3)
    Lifecycle Policy:
      - Transition to IA after 30 days
      - Transition to Glacier after 180 days
      - Delete after 2555 days (7 years)
    
  agent-config-bucket:
    Purpose: Configuration and deployment artifacts
    Encryption: KMS
    Versioning: Enabled
    MFA Delete: Enabled
```

### Database Infrastructure

#### RDS Aurora PostgreSQL

```yaml
Aurora Cluster Configuration:
  Engine: aurora-postgresql
  Version: 15.4
  Instance Class: r6g.large
  Multi-AZ: true
  
  Writer Instance:
    Instance: aurora-writer
    AZ: us-east-1a
    
  Reader Instances:
    - Instance: aurora-reader-1
      AZ: us-east-1b
    - Instance: aurora-reader-2  
      AZ: us-east-1c
  
  Auto Scaling:
    Min Capacity: 1 reader
    Max Capacity: 5 readers
    Target CPU: 70%
    Scale In Cooldown: 15 minutes
    Scale Out Cooldown: 5 minutes
  
  Backup Configuration:
    Backup Retention: 7 days
    Backup Window: 03:00-04:00 UTC
    Maintenance Window: Sun 04:00-05:00 UTC
    
  Performance Insights: Enabled
  Enhanced Monitoring: Enabled (60s granularity)
  
  Security:
    Encryption at Rest: Enabled (KMS)
    Encryption in Transit: Required
    IAM Database Authentication: Enabled
    
Database Schema:
  Primary Database: agentdb
  
  Tables:
    - agent_configurations
    - performance_metrics  
    - conversation_sessions
    - user_profiles
    - audit_logs
```

#### DynamoDB Tables

```yaml
Sessions Table:
  Table Name: agent-sessions
  Billing Mode: On-Demand
  
  Key Schema:
    Partition Key: sessionId (String)
    Sort Key: timestamp (String)
  
  Global Secondary Indexes:
    UserIndex:
      Partition Key: userId (String)
      Projection: ALL
    
  Stream: Enabled (NEW_AND_OLD_IMAGES)
  Point-in-Time Recovery: Enabled
  Encryption: AWS Managed KMS
  
  Item TTL: 30 days (ttl attribute)

Events Table:
  Table Name: agent-events
  Billing Mode: On-Demand
  
  Key Schema:
    Partition Key: eventId (String)
    
  Global Secondary Indexes:
    TimestampIndex:
      Partition Key: date (String)
      Sort Key: timestamp (String)
      
    TypeIndex:
      Partition Key: eventType (String)
      Sort Key: timestamp (String)
  
  Stream: Enabled
  Point-in-Time Recovery: Enabled
  
Configurations Table:
  Table Name: agent-configurations
  Billing Mode: Provisioned
  
  Read Capacity: 10 RCU
  Write Capacity: 5 WCU
  
  Auto Scaling:
    Target Utilization: 70%
    Min Capacity: 5 RCU/WCU
    Max Capacity: 200 RCU/WCU
```

#### ElastiCache Redis

```yaml
Redis Cluster Configuration:
  Engine: redis
  Version: 7.0
  Node Type: cache.r6g.large
  
  Replication Group:
    Num Cache Clusters: 3
    Multi-AZ: Enabled
    Automatic Failover: Enabled
    
  Subnet Group: agent-cache-subnet-group
  Subnets: [Private Data Subnets]
  Security Groups: [Cache SG]
  
  Backup Configuration:
    Snapshot Retention: 5 days
    Snapshot Window: 05:00-06:00 UTC
    
  Maintenance Window: Sun 06:00-07:00 UTC
  
  Security:
    Encryption at Rest: Enabled
    Encryption in Transit: Enabled
    Auth Token: Enabled
    
Parameter Group Configuration:
  maxmemory-policy: allkeys-lru
  timeout: 300
  tcp-keepalive: 300
```

## API Gateway Infrastructure

### REST API Configuration

```yaml
API Gateway: bird-agent-api
Type: REST API
Endpoint Type: Regional

Stage Configuration:
  Stage Name: prod
  Deployment: Automatic
  
  Variables:
    - backend_url: https://agent-alb.us-east-1.elb.amazonaws.com
    - api_version: v1
    - environment: production

Throttling:
  Burst Limit: 5000 requests
  Rate Limit: 2000 requests/second
  
Request Validation:
  Validate Request Body: true
  Validate Request Parameters: true
  Validate Query String: true

Method Configuration:
  POST /api/v1/agents/process:
    Authorization: AWS_IAM
    Request Timeout: 29 seconds
    Integration Timeout: 29 seconds
    
    Request Models:
      application/json: BirdAgentRequest
      
    Response Models:
      200: BirdAgentResponse
      400: ErrorResponse
      500: ErrorResponse
```

### WAF Configuration

```yaml
Web ACL: bird-agent-waf
Scope: REGIONAL
Associated Resources: [API Gateway]

Rules:
  1. AWS Managed Rule - Core Rule Set (Priority 1)
     Override: None
     Action: Block
     
  2. AWS Managed Rule - Known Bad Inputs (Priority 2)
     Override: None  
     Action: Block
     
  3. Rate Limiting Rule (Priority 10)
     Statement: Rate-based (2000 requests/5min per IP)
     Action: Block
     
  4. Geo Blocking Rule (Priority 20)
     Statement: Geographic match (Block CN, RU, KP)
     Action: Block
     
  5. IP Allowlist Rule (Priority 30)
     Statement: IP set match (Bird.com IPs)
     Action: Allow
     
Default Action: Allow

Logging:
  Log Destination: CloudWatch Logs
  Log Group: /aws/wafv2/bird-agent-waf
  Retention: 30 days
```

## Load Balancer Architecture

### Application Load Balancer

```yaml
ALB Configuration:
  Name: bird-agent-alb
  Scheme: internal
  Type: application
  IP Address Type: ipv4
  
  Subnets: [Private App Subnets]
  Security Groups: [ALB SG]
  
  Listeners:
    HTTPS (443):
      Certificate: ACM Certificate
      SSL Policy: ELBSecurityPolicy-TLS-1-2-2019-07
      
      Rules:
        Default: Forward to conversation-manager-tg
        
        /multimodal/*: Forward to multimodal-processor-tg
        /health: Forward to health-check-tg
        /metrics: Forward to metrics-tg

Target Groups:
  conversation-manager-tg:
    Protocol: HTTP
    Port: 8080
    Health Check:
      Path: /health
      Interval: 30 seconds
      Timeout: 5 seconds
      Healthy Threshold: 2
      Unhealthy Threshold: 3
      Matcher: 200
    
    Stickiness: Disabled
    Deregistration Delay: 30 seconds
    
  multimodal-processor-tg:
    Protocol: HTTP
    Port: 8080
    Health Check:
      Path: /health
      Interval: 30 seconds  
      Timeout: 10 seconds
      Healthy Threshold: 2
      Unhealthy Threshold: 2
      Matcher: 200
    
    Stickiness: Disabled
    Deregistration Delay: 60 seconds
```

## Event-Driven Architecture

### EventBridge Configuration

```yaml
Custom Event Bus: bird-agent-events
  
Event Rules:
  agent-message-processing:
    Event Pattern:
      source: ["bird.com"]
      detail-type: ["Message Received"]
    Targets:
      - Lambda: event-processor
      - SQS: message-processing-queue
      
  multimodal-content-analysis:
    Event Pattern:
      source: ["agent.multimodal"]
      detail-type: ["Content Analysis Required"]
    Targets:
      - Step Functions: multimodal-analysis-workflow
      
  performance-metrics:
    Event Pattern:
      source: ["agent.metrics"]
    Targets:
      - CloudWatch: Custom Metrics
      - Kinesis: analytics-stream

Archive Configuration:
  Name: agent-events-archive
  Retention: 30 days
  Archive Pattern:
    source: ["bird.com", "agent.*"]
```

### SQS Queues

```yaml
Message Processing Queue:
  Name: message-processing-queue
  Visibility Timeout: 60 seconds
  Message Retention: 14 days
  Max Receive Count: 3
  
  Dead Letter Queue: message-processing-dlq
  Redrive Policy:
    deadLetterTargetArn: arn:aws:sqs:region:account:message-processing-dlq
    maxReceiveCount: 3
  
  Encryption: SQS Managed (SSE-SQS)
  
Multimodal Processing Queue:
  Name: multimodal-processing-queue
  Visibility Timeout: 300 seconds (5 minutes)
  Message Retention: 14 days
  Max Receive Count: 2
  
  FIFO: true
  Content Based Deduplication: true
  
High Priority Queue:
  Name: high-priority-processing-queue.fifo
  Visibility Timeout: 30 seconds
  Message Retention: 7 days
  
  FIFO: true
  Content Based Deduplication: true
  Message Group ID: priority-group
```

### Step Functions

```yaml
Multimodal Analysis Workflow:
  State Machine: multimodal-analysis-sm
  Type: EXPRESS
  
  States:
    ContentClassification:
      Type: Task
      Resource: arn:aws:lambda:region:account:function:content-classifier
      
    ParallelProcessing:
      Type: Parallel
      Branches:
        - ImageAnalysis:
            Type: Task
            Resource: arn:aws:lambda:region:account:function:image-analyzer
        - TextExtraction:
            Type: Task  
            Resource: arn:aws:lambda:region:account:function:text-extractor
        - MetadataEnrichment:
            Type: Task
            Resource: arn:aws:lambda:region:account:function:metadata-enricher
            
    ResultsAggregation:
      Type: Task
      Resource: arn:aws:lambda:region:account:function:results-aggregator
      
    NotificationDelivery:
      Type: Task
      Resource: arn:aws:sns:region:account:processing-complete
      End: true
  
  Logging:
    Level: ALL
    Include Execution Data: true
    Destinations:
      - CloudWatch Log Group: /aws/stepfunctions/multimodal-analysis
```

## Monitoring and Observability Infrastructure

### CloudWatch Configuration

```yaml
Log Groups:
  /aws/ecs/bird-agent-cluster:
    Retention: 30 days
    
  /aws/lambda/event-processor:
    Retention: 14 days
    
  /aws/apigateway/bird-agent-api:
    Retention: 30 days
    
  /aws/stepfunctions/multimodal-analysis:
    Retention: 7 days

Custom Metrics Namespace: BirdAgent

Dashboards:
  BirdAgent-Overview:
    Widgets: 
      - API Gateway request count and latency
      - ECS service CPU and memory utilization
      - Lambda function invocations and errors
      - Database connections and query performance
      
  BirdAgent-Performance:
    Widgets:
      - Response time percentiles
      - Throughput metrics
      - Error rates by service
      - Cost analysis
      
  BirdAgent-Infrastructure:
    Widgets:
      - VPC flow logs summary
      - NAT Gateway bandwidth
      - Load balancer metrics
      - Auto scaling activities
```

### Alarms Configuration

```yaml
Critical Alarms:
  HighErrorRate:
    Metric: AWS/ApiGateway 4XXError + 5XXError
    Threshold: > 5%
    Period: 5 minutes
    Evaluation Periods: 2
    Actions: [SNS Topic: critical-alerts, Auto Scaling]
    
  HighLatency:
    Metric: AWS/ApiGateway Latency
    Threshold: > 10 seconds (P95)
    Period: 5 minutes
    Evaluation Periods: 2
    Actions: [SNS Topic: critical-alerts]
    
  DatabaseConnectionFailure:
    Metric: AWS/RDS DatabaseConnections
    Threshold: < 1
    Period: 1 minute
    Evaluation Periods: 3
    Actions: [SNS Topic: critical-alerts, Restart RDS]

Warning Alarms:
  HighCPUUtilization:
    Metric: AWS/ECS CPUUtilization
    Threshold: > 80%
    Period: 10 minutes
    Evaluation Periods: 2
    Actions: [SNS Topic: warning-alerts]
    
  HighMemoryUtilization:
    Metric: AWS/ECS MemoryUtilization  
    Threshold: > 85%
    Period: 10 minutes
    Evaluation Periods: 2
    Actions: [SNS Topic: warning-alerts]
    
  DiskSpaceUsage:
    Metric: AWS/RDS FreeStorageSpace
    Threshold: < 20%
    Period: 5 minutes
    Evaluation Periods: 1
    Actions: [SNS Topic: warning-alerts]
```

## Security Infrastructure

### IAM Roles and Policies

```yaml
ECS Task Execution Role:
  Role Name: BirdAgentECSTaskExecutionRole
  Policies:
    - AmazonECSTaskExecutionRolePolicy
    - Custom ECR Access Policy
    - Custom CloudWatch Logs Policy
  
  Trust Policy:
    Principal: ecs-tasks.amazonaws.com

ECS Task Role:
  Role Name: BirdAgentECSTaskRole
  Policies:
    - Bedrock Invoke Model Policy
    - Rekognition Access Policy
    - S3 Media Bucket Policy
    - DynamoDB Access Policy
    - Secrets Manager Access Policy
  
  Trust Policy:
    Principal: ecs-tasks.amazonaws.com

Lambda Execution Role:
  Role Name: BirdAgentLambdaExecutionRole
  Policies:
    - AWSLambdaVPCAccessExecutionRole
    - Custom DynamoDB Access Policy
    - Custom S3 Access Policy
    - Custom EventBridge Policy
  
  Trust Policy:
    Principal: lambda.amazonaws.com

API Gateway Execution Role:
  Role Name: BirdAgentAPIGatewayExecutionRole
  Policies:
    - Custom CloudWatch Logs Policy
    - Custom Lambda Invoke Policy
  
  Trust Policy:
    Principal: apigateway.amazonaws.com
```

### KMS Key Management

```yaml
KMS Keys:
  bird-agent-rds-key:
    Description: Encryption key for RDS Aurora
    Key Policy: RDS service access + admin access
    Automatic Rotation: Enabled
    
  bird-agent-s3-key:
    Description: Encryption key for S3 buckets
    Key Policy: S3 service access + application access
    Automatic Rotation: Enabled
    
  bird-agent-secrets-key:
    Description: Encryption key for Secrets Manager
    Key Policy: Secrets Manager service + application access
    Automatic Rotation: Enabled
    
Key Aliases:
  - alias/bird-agent/rds
  - alias/bird-agent/s3
  - alias/bird-agent/secrets
```

### Secrets Manager

```yaml
Secrets:
  bird-com-api-credentials:
    Type: API Key
    Rotation: Manual
    Description: Bird.com platform API credentials
    
  database-credentials:
    Type: RDS Credentials
    Rotation: Automatic (30 days)
    Description: Aurora PostgreSQL master credentials
    
  redis-auth-token:
    Type: String
    Rotation: Manual
    Description: ElastiCache Redis authentication token
    
  bedrock-api-keys:
    Type: API Key
    Rotation: Manual
    Description: AWS Bedrock service API keys
```

## Disaster Recovery and Backup

### Multi-Region Setup

```yaml
Primary Region: us-east-1
Secondary Region: us-west-2

Cross-Region Replication:
  S3 Buckets:
    - agent-media-bucket → agent-media-bucket-west
    - agent-config-bucket → agent-config-bucket-west
  
  RDS Aurora:
    - Global Database with read replica in us-west-2
    - Automated backups replicated to us-west-2
  
  DynamoDB:
    - Global Tables enabled for all tables
    - Point-in-time recovery enabled

Route 53 Health Checks:
  Primary Endpoint: api-east.yourdomain.com
  Secondary Endpoint: api-west.yourdomain.com
  
  Failover Policy: Automatic
  Health Check Interval: 30 seconds
  Failure Threshold: 3 consecutive failures
```

### Backup Strategy

```yaml
RDS Aurora Backups:
  Automated Backups: 7 days retention
  Manual Snapshots: Monthly, retained for 1 year
  Cross-Region Snapshots: Weekly to us-west-2
  
S3 Backup:
  Versioning: Enabled on all buckets
  Cross-Region Replication: Enabled
  Lifecycle Management: Archive to Glacier after 90 days
  
DynamoDB Backups:
  Point-in-Time Recovery: Enabled (35 days)
  On-Demand Backups: Weekly
  Cross-Region Backup: Via AWS Backup service
  
Configuration Backups:
  Infrastructure as Code: Stored in Git with versioning
  Application Configurations: Backed up to S3 daily
  Secrets: Replicated across regions automatically
```

This comprehensive infrastructure architecture provides a robust, scalable, and secure foundation for the Bird.com external agent system on AWS, with built-in fault tolerance, monitoring, and disaster recovery capabilities.