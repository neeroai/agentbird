# Implementation Guide: AWS External Agent for Bird.com

## Prerequisites

### AWS Account Setup
- AWS Account with appropriate permissions
- AWS CLI configured with administrator access
- Terraform or AWS CDK installed
- Docker installed for container builds
- kubectl configured for EKS management

### Bird.com Platform Requirements
- Active Bird.com AI Employee subscription
- API access credentials
- Webhook configuration permissions
- Understanding of current agent workflows

### Development Environment
```bash
# Required tools installation
curl -sL https://github.com/aws/aws-cli/releases/latest/download/awscli-exe-linux-x86_64.zip -o awscli.zip
sudo apt install unzip
unzip awscli.zip && sudo ./aws/install

# Terraform installation
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip && sudo mv terraform /usr/local/bin/

# Docker installation
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# kubectl installation
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

## Phase 1: Foundation Infrastructure

### Step 1: VPC and Networking Setup

Create the base infrastructure using Terraform:

```hcl
# infrastructure/vpc.tf
resource "aws_vpc" "agent_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "bird-agent-vpc"
    Environment = var.environment
  }
}

resource "aws_internet_gateway" "agent_igw" {
  vpc_id = aws_vpc.agent_vpc.id
  
  tags = {
    Name = "bird-agent-igw"
  }
}

resource "aws_subnet" "public" {
  count             = 3
  vpc_id            = aws_vpc.agent_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  map_public_ip_on_launch = true
  
  tags = {
    Name = "bird-agent-public-${count.index + 1}"
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.agent_vpc.id
  cidr_block        = "10.0.${count.index + 11}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name = "bird-agent-private-${count.index + 1}"
    Type = "private"
  }
}

resource "aws_nat_gateway" "agent_nat" {
  count         = 3
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  depends_on = [aws_internet_gateway.agent_igw]
  
  tags = {
    Name = "bird-agent-nat-${count.index + 1}"
  }
}
```

### Step 2: Security Groups Configuration

```hcl
# infrastructure/security_groups.tf
resource "aws_security_group" "api_gateway" {
  name_prefix = "bird-agent-api-gateway-"
  vpc_id      = aws_vpc.agent_vpc.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "bird-agent-api-gateway-sg"
  }
}

resource "aws_security_group" "ecs_services" {
  name_prefix = "bird-agent-ecs-"
  vpc_id      = aws_vpc.agent_vpc.id

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.api_gateway.id]
  }

  ingress {
    from_port       = 8081
    to_port         = 8081
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "bird-agent-ecs-sg"
  }
}
```

### Step 3: Database Setup

```hcl
# infrastructure/databases.tf
resource "aws_db_subnet_group" "agent_db_subnet_group" {
  name       = "bird-agent-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "Bird Agent DB subnet group"
  }
}

resource "aws_rds_cluster" "agent_aurora" {
  cluster_identifier     = "bird-agent-aurora"
  engine                 = "aurora-postgresql"
  engine_version         = "15.4"
  database_name          = "agentdb"
  master_username        = var.db_username
  master_password        = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.agent_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.database.id]
  
  backup_retention_period = 7
  preferred_backup_window = "03:00-04:00"
  storage_encrypted       = true
  
  tags = {
    Name = "bird-agent-aurora"
  }
}

resource "aws_dynamodb_table" "sessions" {
  name           = "agent-sessions"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "sessionId"
  range_key      = "timestamp"
  stream_enabled = true
  
  attribute {
    name = "sessionId"
    type = "S"
  }
  
  attribute {
    name = "timestamp"
    type = "S"
  }
  
  attribute {
    name = "userId"
    type = "S"
  }
  
  global_secondary_index {
    name     = "UserIndex"
    hash_key = "userId"
  }
  
  tags = {
    Name = "agent-sessions"
  }
}
```

### Step 4: Deploy Infrastructure

```bash
# Initialize and deploy base infrastructure
cd infrastructure
terraform init
terraform plan -var-file="production.tfvars"
terraform apply -var-file="production.tfvars"

# Save outputs for next phase
terraform output -json > ../outputs/infrastructure.json
```

## Phase 2: Container Services Deployment

### Step 1: Build Container Images

#### Conversation Manager Service
```dockerfile
# services/conversation-manager/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "src.main:app"]
```

```python
# services/conversation-manager/src/main.py
from flask import Flask, request, jsonify
import os
import boto3
from redis import Redis
import json
import logging

app = Flask(__name__)

# Configuration
REDIS_HOST = os.getenv('REDIS_CLUSTER_ENDPOINT')
BIRD_API_KEY = os.getenv('BIRD_API_KEY')
AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

# Initialize services
redis_client = Redis(host=REDIS_HOST, port=6379, decode_responses=True)
bedrock_client = boto3.client('bedrock-runtime', region_name=AWS_REGION)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "conversation-manager"})

@app.route('/process', methods=['POST'])
def process_message():
    try:
        data = request.get_json()
        
        # Validate Bird.com format
        if not validate_bird_format(data):
            return jsonify({"error": "Invalid request format"}), 400
        
        # Extract session information
        session_id = data.get('context', {}).get('sessionId')
        message_content = data.get('content', {})
        
        # Process based on content type
        if message_content.get('type') == 'text':
            response = process_text_message(data)
        elif message_content.get('type') in ['image', 'audio', 'document']:
            response = process_multimodal_message(data)
        else:
            return jsonify({"error": "Unsupported content type"}), 400
        
        # Store session state
        if session_id:
            store_session_state(session_id, data, response)
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({"error": "Internal processing error"}), 500

def validate_bird_format(data):
    required_fields = ['version', 'messageId', 'source', 'content']
    return all(field in data for field in required_fields)

def process_text_message(data):
    content = data['content']['data']
    
    # Call Bedrock for text processing
    response = bedrock_client.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": content}
            ]
        })
    )
    
    result = json.loads(response['body'].read())
    
    return {
        "version": "1.0",
        "messageId": data['messageId'],
        "timestamp": data['timestamp'],
        "status": "success",
        "response": {
            "type": "text",
            "content": result['content'][0]['text'],
            "metadata": {
                "confidence": 0.95,
                "processingTime": "150",
                "source": "aws-enhanced"
            }
        }
    }

def process_multimodal_message(data):
    # Route to multimodal processor service
    import requests
    
    response = requests.post(
        'http://multimodal-processor:8080/process',
        json=data,
        timeout=30
    )
    
    return response.json()

def store_session_state(session_id, request_data, response_data):
    session_key = f"session:{session_id}"
    session_data = {
        "last_request": request_data,
        "last_response": response_data,
        "updated_at": request_data['timestamp']
    }
    redis_client.hset(session_key, mapping=session_data)
    redis_client.expire(session_key, 3600)  # 1 hour expiration

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
```

#### Multimodal Processor Service
```dockerfile
# services/multimodal-processor/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY models/ ./models/

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "300", "src.main:app"]
```

```python
# services/multimodal-processor/src/main.py
import boto3
import json
import base64
from flask import Flask, request, jsonify
import cv2
import numpy as np
from PIL import Image
import io
import logging

app = Flask(__name__)

# AWS service clients
rekognition = boto3.client('rekognition')
transcribe = boto3.client('transcribe')
textract = boto3.client('textract')
s3 = boto3.client('s3')

S3_BUCKET = os.getenv('S3_BUCKET', 'agent-media-bucket')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "multimodal-processor"})

@app.route('/process', methods=['POST'])
def process_multimodal():
    try:
        data = request.get_json()
        content = data.get('content', {})
        content_type = content.get('type')
        
        if content_type == 'image':
            return process_image(data)
        elif content_type == 'audio':
            return process_audio(data)
        elif content_type == 'document':
            return process_document(data)
        else:
            return jsonify({"error": f"Unsupported content type: {content_type}"}), 400
    
    except Exception as e:
        logger.error(f"Multimodal processing error: {str(e)}")
        return jsonify({"error": "Multimodal processing failed"}), 500

def process_image(data):
    content = data['content']
    
    if content['data'].startswith('http'):
        # Process image URL
        image_bytes = download_image(content['data'])
    else:
        # Process base64 image
        image_bytes = base64.b64decode(content['data'])
    
    # Upload to S3 for processing
    key = f"images/{data['messageId']}.jpg"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=image_bytes)
    
    # Analyze with Rekognition
    rekognition_response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': S3_BUCKET,
                'Name': key
            }
        },
        MaxLabels=10,
        MinConfidence=80
    )
    
    # Extract text with Textract if needed
    textract_response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': S3_BUCKET,
                'Name': key
            }
        }
    )
    
    # Process results
    labels = [label['Name'] for label in rekognition_response['Labels']]
    extracted_text = extract_text_from_textract(textract_response)
    
    analysis_result = {
        "labels": labels,
        "extracted_text": extracted_text,
        "confidence": rekognition_response['Labels'][0]['Confidence'] if labels else 0
    }
    
    return {
        "version": "1.0",
        "messageId": data['messageId'],
        "timestamp": data['timestamp'],
        "status": "success",
        "response": {
            "type": "text",
            "content": generate_image_summary(analysis_result),
            "metadata": {
                "confidence": analysis_result["confidence"] / 100,
                "processingTime": "2500",
                "source": "aws-enhanced",
                "analysis": analysis_result
            }
        }
    }

def process_audio(data):
    # Implementation for audio processing using Transcribe
    content = data['content']
    
    # Upload audio to S3
    if content['data'].startswith('http'):
        audio_bytes = download_audio(content['data'])
    else:
        audio_bytes = base64.b64decode(content['data'])
    
    key = f"audio/{data['messageId']}.wav"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=audio_bytes)
    
    # Start transcription job
    job_name = f"transcribe-{data['messageId']}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f's3://{S3_BUCKET}/{key}'},
        MediaFormat='wav',
        LanguageCode='es-ES'
    )
    
    # Wait for completion (in production, use async processing)
    import time
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(2)
    
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcript = download_transcript(transcript_uri)
        
        return {
            "version": "1.0",
            "messageId": data['messageId'],
            "timestamp": data['timestamp'],
            "status": "success",
            "response": {
                "type": "text",
                "content": transcript,
                "metadata": {
                    "confidence": 0.9,
                    "processingTime": "5000",
                    "source": "aws-enhanced"
                }
            }
        }
    else:
        return jsonify({"error": "Audio transcription failed"}), 500

def generate_image_summary(analysis_result):
    labels_text = ", ".join(analysis_result["labels"][:5])
    extracted_text = analysis_result["extracted_text"]
    
    summary = f"Imagen detectada con elementos: {labels_text}."
    if extracted_text:
        summary += f" Texto extraído: {extracted_text}"
    
    return summary

def extract_text_from_textract(response):
    text_blocks = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text_blocks.append(block['Text'])
    return " ".join(text_blocks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
```

### Step 2: Deploy ECS Services

```yaml
# deployment/ecs-cluster.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: bird-agents

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: conversation-manager
  namespace: bird-agents
spec:
  replicas: 3
  selector:
    matchLabels:
      app: conversation-manager
  template:
    metadata:
      labels:
        app: conversation-manager
    spec:
      containers:
      - name: conversation-manager
        image: your-registry/conversation-manager:latest
        ports:
        - containerPort: 8080
        env:
        - name: REDIS_CLUSTER_ENDPOINT
          value: "your-redis-endpoint"
        - name: BIRD_API_KEY
          valueFrom:
            secretKeyRef:
              name: bird-secrets
              key: api-key
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10

---
apiVersion: v1
kind: Service
metadata:
  name: conversation-manager-service
  namespace: bird-agents
spec:
  selector:
    app: conversation-manager
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

## Phase 3: API Gateway Configuration

### Step 1: Create API Gateway

```python
# deployment/api_gateway_setup.py
import boto3
import json

def create_api_gateway():
    client = boto3.client('apigateway')
    
    # Create REST API
    api = client.create_rest_api(
        name='bird-agent-api',
        description='API Gateway for Bird.com Agent Integration',
        endpointConfiguration={
            'types': ['REGIONAL']
        }
    )
    
    api_id = api['id']
    
    # Get root resource
    resources = client.get_resources(restApiId=api_id)
    root_id = resources['items'][0]['id']
    
    # Create /api resource
    api_resource = client.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='api'
    )
    
    # Create /v1 resource
    v1_resource = client.create_resource(
        restApiId=api_id,
        parentId=api_resource['id'],
        pathPart='v1'
    )
    
    # Create /agents resource
    agents_resource = client.create_resource(
        restApiId=api_id,
        parentId=v1_resource['id'],
        pathPart='agents'
    )
    
    # Create /process resource
    process_resource = client.create_resource(
        restApiId=api_id,
        parentId=agents_resource['id'],
        pathPart='process'
    )
    
    # Create POST method for /process
    client.put_method(
        restApiId=api_id,
        resourceId=process_resource['id'],
        httpMethod='POST',
        authorizationType='AWS_IAM',
        requestParameters={}
    )
    
    # Set up integration with ALB
    integration_uri = f"http://your-alb-endpoint.us-east-1.elb.amazonaws.com/process"
    
    client.put_integration(
        restApiId=api_id,
        resourceId=process_resource['id'],
        httpMethod='POST',
        type='HTTP_PROXY',
        integrationHttpMethod='POST',
        uri=integration_uri,
        requestParameters={
            'integration.request.header.Authorization': 'context.authorizer.token'
        }
    )
    
    # Deploy API
    client.create_deployment(
        restApiId=api_id,
        stageName='prod',
        description='Production deployment'
    )
    
    return api_id

if __name__ == '__main__':
    api_id = create_api_gateway()
    print(f"API Gateway created with ID: {api_id}")
```

### Step 2: Configure WAF and Security

```json
{
  "Name": "bird-agent-waf",
  "Scope": "REGIONAL",
  "DefaultAction": {
    "Allow": {}
  },
  "Rules": [
    {
      "Name": "RateLimitRule",
      "Priority": 1,
      "Statement": {
        "RateBasedStatement": {
          "Limit": 2000,
          "AggregateKeyType": "IP"
        }
      },
      "Action": {
        "Block": {}
      }
    },
    {
      "Name": "GeoBlockRule",
      "Priority": 2,
      "Statement": {
        "GeoMatchStatement": {
          "CountryCodes": ["CN", "RU", "KP"]
        }
      },
      "Action": {
        "Block": {}
      }
    }
  ]
}
```

## Phase 4: Lambda Functions Deployment

### Event Processor Lambda

```python
# lambdas/event_processor/handler.py
import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
events_table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    try:
        # Process EventBridge event
        detail = event.get('detail', {})
        source = event.get('source', '')
        
        # Store event in DynamoDB
        event_item = {
            'eventId': context.aws_request_id,
            'timestamp': datetime.utcnow().isoformat(),
            'source': source,
            'eventType': detail.get('eventType', 'unknown'),
            'data': json.dumps(detail),
            'processed': False
        }
        
        events_table.put_item(Item=event_item)
        
        # Route to appropriate processor
        if detail.get('contentType') in ['image', 'audio', 'document']:
            return process_multimodal_event(detail)
        else:
            return process_text_event(detail)
            
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def process_multimodal_event(detail):
    # Trigger Step Function for complex processing
    step_functions = boto3.client('stepfunctions')
    
    step_functions.start_execution(
        stateMachineArn=os.environ['STEP_FUNCTION_ARN'],
        input=json.dumps(detail)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'processing'})
    }

def process_text_event(detail):
    # Direct processing for simple text events
    return {
        'statusCode': 200,
        'body': json.dumps({'status': 'completed'})
    }
```

### Deployment Script

```bash
#!/bin/bash
# deployment/deploy_lambdas.sh

# Build and deploy event processor
cd lambdas/event_processor
zip -r event_processor.zip .
aws lambda create-function \
  --function-name bird-agent-event-processor \
  --runtime python3.11 \
  --role arn:aws:iam::account:role/lambda-execution-role \
  --handler handler.lambda_handler \
  --zip-file fileb://event_processor.zip \
  --timeout 300 \
  --memory-size 1024 \
  --environment Variables="{DYNAMODB_TABLE=agent-events}"

# Build and deploy multimodal analysis
cd ../multimodal_analysis
zip -r multimodal_analysis.zip .
aws lambda create-function \
  --function-name bird-agent-multimodal-analysis \
  --runtime python3.11 \
  --role arn:aws:iam::account:role/lambda-execution-role \
  --handler handler.lambda_handler \
  --zip-file fileb://multimodal_analysis.zip \
  --timeout 300 \
  --memory-size 3008

echo "Lambda functions deployed successfully"
```

## Testing and Validation

### Integration Tests

```python
# tests/integration/test_api_flow.py
import requests
import json
import base64
import time
import pytest

API_ENDPOINT = "https://your-api-gateway.execute-api.us-east-1.amazonaws.com/prod"
API_KEY = "your-api-key"

class TestBirdAgentIntegration:
    
    def test_text_processing(self):
        payload = {
            "version": "1.0",
            "messageId": "test-123",
            "timestamp": "2024-01-15T10:30:00Z",
            "source": {
                "platform": "bird.com",
                "channel": "sms",
                "userId": "user-456"
            },
            "content": {
                "type": "text",
                "data": "Hola, necesito ayuda con mi cuenta",
                "metadata": {
                    "language": "es",
                    "contentType": "text/plain"
                }
            },
            "context": {
                "sessionId": "session-789",
                "conversationHistory": [],
                "userProfile": {},
                "preferences": {}
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        response = requests.post(
            f"{API_ENDPOINT}/api/v1/agents/process",
            json=payload,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert data["response"]["type"] == "text"
        assert len(data["response"]["content"]) > 0
        
    def test_image_processing(self):
        # Test with a sample image
        with open("tests/fixtures/sample_image.jpg", "rb") as f:
            image_data = base64.b64encode(f.read()).decode()
        
        payload = {
            "version": "1.0",
            "messageId": "test-image-123",
            "timestamp": "2024-01-15T10:30:00Z",
            "source": {
                "platform": "bird.com",
                "channel": "whatsapp",
                "userId": "user-456"
            },
            "content": {
                "type": "image",
                "data": image_data,
                "metadata": {
                    "contentType": "image/jpeg",
                    "size": "156784"
                }
            },
            "context": {
                "sessionId": "session-789"
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        response = requests.post(
            f"{API_ENDPOINT}/api/v1/agents/process",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert "analysis" in data["response"]["metadata"]
        
    def test_performance_benchmark(self):
        # Test concurrent requests
        import concurrent.futures
        import time
        
        def make_request():
            start_time = time.time()
            response = self.test_text_processing()
            end_time = time.time()
            return end_time - start_time
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            response_times = [future.result() for future in futures]
        
        avg_response_time = sum(response_times) / len(response_times)
        p95_response_time = sorted(response_times)[int(0.95 * len(response_times))]
        
        assert avg_response_time < 1.0  # Average under 1 second
        assert p95_response_time < 2.0  # P95 under 2 seconds

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Load Testing

```bash
# tests/load/load_test.sh
#!/bin/bash

echo "Starting load test for Bird Agent API"

# Install k6 if not present
if ! command -v k6 &> /dev/null; then
    echo "Installing k6..."
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
    echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
    sudo apt-get update
    sudo apt-get install k6
fi

# Run load test
k6 run --vus 50 --duration 5m tests/load/load_test.js

echo "Load test completed"
```

```javascript
// tests/load/load_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 50 },
    { duration: '2m', target: 100 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'],
    http_req_failed: ['rate<0.05'],
  },
};

const API_ENDPOINT = 'https://your-api-gateway.execute-api.us-east-1.amazonaws.com/prod';
const API_KEY = 'your-api-key';

export default function() {
  let payload = {
    version: '1.0',
    messageId: `load-test-${__VU}-${__ITER}`,
    timestamp: new Date().toISOString(),
    source: {
      platform: 'bird.com',
      channel: 'sms',
      userId: `user-${__VU}`
    },
    content: {
      type: 'text',
      data: 'Test message for load testing',
      metadata: {
        language: 'es',
        contentType: 'text/plain'
      }
    },
    context: {
      sessionId: `session-${__VU}`,
      conversationHistory: [],
      userProfile: {},
      preferences: {}
    }
  };

  let params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_KEY}`
    },
  };

  let response = http.post(`${API_ENDPOINT}/api/v1/agents/process`, JSON.stringify(payload), params);
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 2s': (r) => r.timings.duration < 2000,
    'has response content': (r) => JSON.parse(r.body).response.content.length > 0,
  });

  sleep(1);
}
```

## Monitoring Setup

### CloudWatch Dashboards

```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/ApiGateway", "Count", "ApiName", "bird-agent-api"],
          [".", "Latency", ".", "."],
          [".", "4XXError", ".", "."],
          [".", "5XXError", ".", "."]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "API Gateway Metrics"
      }
    },
    {
      "type": "metric", 
      "properties": {
        "metrics": [
          ["AWS/ECS", "CPUUtilization", "ServiceName", "conversation-manager"],
          [".", "MemoryUtilization", ".", "."],
          [".", "CPUUtilization", "ServiceName", "multimodal-processor"],
          [".", "MemoryUtilization", ".", "."]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "ECS Service Metrics"
      }
    }
  ]
}
```

### Alerting Configuration

```bash
# monitoring/setup_alerts.sh
#!/bin/bash

# Create SNS topic for alerts
aws sns create-topic --name bird-agent-alerts

# Subscribe email to alerts
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:account:bird-agent-alerts \
  --protocol email \
  --notification-endpoint your-email@domain.com

# Create CloudWatch alarms
aws cloudwatch put-metric-alarm \
  --alarm-name "HighErrorRate" \
  --alarm-description "High error rate detected" \
  --metric-name 4XXError \
  --namespace AWS/ApiGateway \
  --statistic Sum \
  --period 300 \
  --threshold 50 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:us-east-1:account:bird-agent-alerts

echo "Monitoring and alerts configured"
```

This comprehensive implementation guide provides step-by-step instructions for deploying the AWS external agent system while maintaining Bird.com compatibility and implementing all the architectural improvements identified in the technical specifications.