# 🔧 API Reference: Bird.com Hybrid AI Agent System

## Overview

This API reference covers all the components of the Bird.com Hybrid AI Agent System, including webhook endpoints, Lambda function interfaces, and integration patterns.

---

## 🔗 Webhook Endpoints

### Primary Webhook Endpoint

**Endpoint:** `POST /webhook`  
**Purpose:** Receive incoming messages from Bird.com platform  
**Authentication:** HMAC-SHA256 signature verification

#### Request Format

```json
{
  "conversation_id": "conv_123456789",
  "user_id": "user_abc123",
  "message": {
    "type": "text|image|voice|document",
    "content": "Message content",
    "media_url": "https://example.com/media.jpg",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "context": {
    "channel": "whatsapp",
    "user_metadata": {
      "name": "María González",
      "phone": "+5215551234567"
    }
  }
}
```

#### Response Format

```json
{
  "success": true,
  "conversation_id": "conv_123456789",
  "classification": {
    "intent": "MAINTENANCE|LEASING|PAYMENTS|AMENITIES|OTHERS",
    "confidence": 0.95,
    "routing_recommendation": "agent_name"
  },
  "processing_time_ms": 450,
  "media_processed": false
}
```

#### Error Responses

```json
{
  "error": {
    "code": "INVALID_SIGNATURE|PROCESSING_ERROR|RATE_LIMIT",
    "message": "Detailed error description",
    "request_id": "req_123456789"
  }
}
```

---

## 🧠 Claude Integration API

### Intent Classification

**Function:** `classify_intent`  
**Purpose:** Classify user message intent using Claude

#### Input Parameters

```python
{
    "message": "User message text",
    "context": ConversationContext,  # Optional
    "confidence_threshold": 0.8      # Optional, default 0.8
}
```

#### Response Format

```python
{
    "intent": "MAINTENANCE",
    "confidence": 0.92,
    "entities": {
        "urgency": "high",
        "property": "josefa",
        "issue_type": "plumbing"
    },
    "routing_recommendation": "maintenance-agent",
    "reasoning": "Message contains urgent maintenance keywords",
    "processing_time_ms": 350
}
```

### Response Generation

**Function:** `generate_response`  
**Purpose:** Generate conversational response using Claude

#### Input Parameters

```python
{
    "message": "User message",
    "context": ConversationContext,
    "response_type": "informational|action_oriented|empathetic"
}
```

#### Response Format

```python
{
    "response": "Generated response text",
    "voice_brand_included": true,
    "call_to_action": "¿Te gustaría agendar un tour?",
    "escalation_suggested": false,
    "confidence_score": 0.88
}
```

### Multimodal Processing

**Function:** `process_multimodal_content`  
**Purpose:** Process images, voice, and documents with Claude

#### Input Parameters

```python
{
    "content": "Text accompanying media",
    "media_type": "image|audio|document",
    "media_data": "base64_encoded_content",
    "analysis_type": "property_comparison|document_extraction|voice_transcription"
}
```

#### Response Format

```python
{
    "analysis": "Detailed analysis of media content",
    "extracted_data": {
        "key_points": ["Point 1", "Point 2"],
        "entities": {"property": "apartment", "condition": "good"}
    },
    "recommendations": ["Recommendation 1", "Recommendation 2"],
    "processing_time_ms": 1200
}
```

---

## 📱 WhatsApp Business API Integration

### Send Text Message

**Function:** `send_text_message`  
**Purpose:** Send text message via WhatsApp Business API

#### Parameters

```python
{
    "to": "+5215551234567",
    "text": "Message content",
    "reply_to": "message_id_to_reply_to"  # Optional
}
```

#### Response

```python
{
    "message_id": "msg_123456789",
    "status": "sent",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### Send Interactive Message

**Function:** `send_interactive_list`  
**Purpose:** Send interactive list message

#### Parameters

```python
{
    "to": "+5215551234567",
    "header_text": "Propiedades Disponibles",
    "body_text": "Selecciona una propiedad:",
    "footer_text": "Powered by UrbanHub",
    "button_text": "Ver Opciones",
    "sections": [
        {
            "title": "Zona Premium",
            "rows": [
                {
                    "id": "josefa",
                    "title": "Josefa",
                    "description": "$20,200 - $32,600 MXN - Reforma"
                }
            ]
        }
    ]
}
```

### Send Template Message

**Function:** `send_template_message`  
**Purpose:** Send pre-approved template message

#### Parameters

```python
{
    "to": "+5215551234567",
    "template_name": "urbanhub_welcome",
    "parameters": ["María"]  # Template variables
}
```

---

## 🗄️ Data Storage APIs

### DynamoDB Operations

#### Conversation Context Storage

**Table:** `UrbanHub-{Environment}-Conversations`

**Item Structure:**
```python
{
    "conversation_id": "conv_123456789",
    "user_id": "user_abc123",
    "messages": [
        {
            "role": "user|assistant",
            "content": "Message content",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    ],
    "user_preferences": {
        "budget_max": 30000,
        "property_interests": ["josefa", "ines"],
        "pet_owner": true
    },
    "conversation_summary": "Brief summary of conversation",
    "total_tokens_used": 1250,
    "last_updated": "2024-01-15T10:30:00Z",
    "ttl": 1674648600  # 30 days from creation
}
```

#### Analysis Results Storage

**Table:** `UrbanHub-{Environment}-Analysis`

**Item Structure:**
```python
{
    "conversation_id": "conv_123456789",
    "analysis_timestamp": "2024-01-15T10:30:00Z",
    "intent_analysis": {
        "intent": "MAINTENANCE",
        "confidence": 0.92,
        "entities": {...},
        "routing_decision": "maintenance-agent"
    },
    "processing_metadata": {
        "claude_model": "claude-3-5-sonnet-20241022",
        "processing_time_ms": 350,
        "tokens_used": 125
    }
}
```

### S3 Storage Operations

#### Media Storage

**Bucket:** `urbanhub-{environment}-media-storage`

**Object Structure:**
```
media/
├── {conversation_id}/
│   ├── {timestamp}.jpg     # Images
│   ├── {timestamp}.ogg     # Voice messages
│   └── {timestamp}.pdf     # Documents
```

**Metadata:**
```python
{
    "Content-Type": "image/jpeg|audio/ogg|application/pdf",
    "x-amz-meta-conversation-id": "conv_123456789",
    "x-amz-meta-upload-timestamp": "2024-01-15T10:30:00Z",
    "x-amz-meta-processed": "true|false"
}
```

---

## ⚡ EventBridge Integration

### Event Publishing

**Event Bus:** `UrbanHub-{Environment}-EventBus`

#### Agent Routing Event

**Event Pattern:**
```json
{
    "source": ["urbanhub.bird.webhook"],
    "detail-type": ["Agent Routing Required"],
    "detail": {
        "conversation_id": "conv_123456789",
        "routing_decision": {
            "target_agent": "maintenance-agent",
            "priority": "high|medium|low",
            "context_summary": "Brief context for receiving agent"
        },
        "user_metadata": {
            "phone": "+5215551234567",
            "name": "María González"
        }
    }
}
```

#### Processing Complete Event

**Event Pattern:**
```json
{
    "source": ["urbanhub.agent.processing"],
    "detail-type": ["Processing Complete"],
    "detail": {
        "conversation_id": "conv_123456789",
        "agent_name": "conversation-ai",
        "processing_result": {
            "success": true,
            "response_generated": true,
            "escalation_required": false
        },
        "metrics": {
            "processing_time_ms": 1200,
            "tokens_used": 250
        }
    }
}
```

---

## 🔒 Security & Authentication

### HMAC Signature Verification

**Purpose:** Verify webhook authenticity from Bird.com

#### Implementation

```python
import hmac
import hashlib

def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Remove 'sha256=' prefix if present
    if signature.startswith('sha256='):
        signature = signature[7:]
    
    return hmac.compare_digest(expected_signature, signature)
```

### API Key Management

**Anthropic Claude API:**
```python
# Stored in AWS Systems Manager Parameter Store
PARAMETER_NAME = "/urbanhub/prod/anthropic-api-key"

import boto3
ssm = boto3.client('ssm')
response = ssm.get_parameter(Name=PARAMETER_NAME, WithDecryption=True)
api_key = response['Parameter']['Value']
```

**WhatsApp Business API:**
```python
# Stored in AWS Secrets Manager
SECRET_NAME = "urbanhub/prod/whatsapp-credentials"

import boto3
secrets_client = boto3.client('secretsmanager')
response = secrets_client.get_secret_value(SecretId=SECRET_NAME)
credentials = json.loads(response['SecretString'])
```

---

## 📊 Monitoring & Metrics APIs

### CloudWatch Custom Metrics

#### Publishing Metrics

```python
import boto3
cloudwatch = boto3.client('cloudwatch')

# Publish custom metric
cloudwatch.put_metric_data(
    Namespace='UrbanHub/BirdIntegration',
    MetricData=[
        {
            'MetricName': 'IntentClassificationAccuracy',
            'Value': 0.95,
            'Unit': 'Percent',
            'Dimensions': [
                {
                    'Name': 'Agent',
                    'Value': 'orchestrator'
                }
            ]
        }
    ]
)
```

#### Key Metrics to Track

```yaml
Performance Metrics:
  - WebhookProcessingTime (Milliseconds)
  - ClaudeAPILatency (Milliseconds)
  - ContextRetrievalTime (Milliseconds)
  - ResponseGenerationTime (Milliseconds)

Business Metrics:
  - IntentClassificationAccuracy (Percent)
  - ConversationResolutionRate (Percent)
  - UserSatisfactionScore (Count)
  - VoiceBrandMentionRate (Percent)

Technical Metrics:
  - WebhookErrorRate (Percent)
  - ClaudeAPIErrorRate (Percent)
  - DynamoDBThrottling (Count)
  - LambdaColdStarts (Count)
```

---

## 🧪 Testing APIs

### Integration Test Helpers

#### Mock Webhook Request

```python
def create_test_webhook_request(message: str, message_type: str = "text"):
    return {
        "conversation_id": f"test_{int(time.time())}",
        "user_id": "test_user_123",
        "message": {
            "type": message_type,
            "content": message,
            "timestamp": datetime.now().isoformat()
        },
        "context": {
            "channel": "whatsapp",
            "user_metadata": {
                "name": "Test User",
                "phone": "+5215551234567"
            }
        }
    }
```

#### Test Response Validation

```python
def validate_webhook_response(response: dict) -> bool:
    required_fields = ['success', 'conversation_id', 'classification']
    
    if not all(field in response for field in required_fields):
        return False
    
    classification = response['classification']
    valid_intents = ['MAINTENANCE', 'LEASING', 'PAYMENTS', 'AMENITIES', 'OTHERS']
    
    return (
        classification['intent'] in valid_intents and
        0 <= classification['confidence'] <= 1 and
        'routing_recommendation' in classification
    )
```

---

## 📈 Rate Limits & Quotas

### Service Limits

#### Claude API
```yaml
Rate Limits:
  - Requests per minute: 4000
  - Tokens per minute: 40000
  - Concurrent requests: 100

Quotas:
  - Monthly token limit: Variable by plan
  - Context window: 200k tokens
  - Max output tokens: 4096
```

#### WhatsApp Business API
```yaml
Rate Limits:
  - Messages per second: 80
  - Messages per day: 100k (varies by plan)
  - Template messages: 1000/day (before approval)

Quotas:
  - Media upload size: 100MB
  - Message length: 4096 characters
```

#### AWS Services
```yaml
Lambda:
  - Concurrent executions: 10000 (default limit)
  - Memory: 128MB - 10240MB
  - Timeout: 15 minutes max

DynamoDB:
  - Read/Write capacity: Configurable
  - Item size: 400KB max
  - Table size: Unlimited

S3:
  - Request rate: 3500 PUT/COPY/POST/DELETE per prefix
  - GET requests: 5500 per prefix
  - Object size: 5TB max
```

---

## 🔧 Error Handling Patterns

### Standard Error Response Format

```python
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": {
            "field": "specific_field_with_error",
            "value": "problematic_value",
            "expected": "expected_format_or_value"
        },
        "request_id": "req_123456789",
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

### Common Error Codes

```yaml
Authentication Errors:
  - INVALID_SIGNATURE: Webhook signature verification failed
  - EXPIRED_TOKEN: API token has expired
  - INSUFFICIENT_PERMISSIONS: Missing required permissions

Processing Errors:
  - PROCESSING_TIMEOUT: Request processing exceeded timeout
  - CLAUDE_API_ERROR: Error calling Claude API
  - CONTEXT_RETRIEVAL_FAILED: Failed to retrieve conversation context

Business Logic Errors:
  - INTENT_CLASSIFICATION_FAILED: Could not classify user intent
  - INVALID_ROUTING_TARGET: Specified agent not available
  - CONVERSATION_NOT_FOUND: Conversation ID not found

Rate Limiting:
  - RATE_LIMIT_EXCEEDED: Too many requests
  - QUOTA_EXCEEDED: Monthly/daily quota exceeded
```

### Retry Patterns

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type((ConnectionError, TimeoutError))
)
async def call_external_api(url, payload):
    # Implementation here
    pass
```

---

## 📝 SDK Examples

### Python SDK Usage

```python
from bird_hybrid_agent import HybridAIClient

# Initialize client
client = HybridAIClient(
    webhook_url="https://api.example.com/webhook",
    claude_api_key="your-claude-key",
    whatsapp_token="your-whatsapp-token"
)

# Process incoming message
result = await client.process_message(
    conversation_id="conv_123",
    message="Hola, necesito ayuda con mi departamento",
    user_metadata={"name": "María", "phone": "+5215551234567"}
)

print(f"Intent: {result.classification.intent}")
print(f"Response: {result.ai_response}")
```

### JavaScript SDK Usage

```javascript
import { HybridAIClient } from '@urbanhub/bird-hybrid-agent';

const client = new HybridAIClient({
  webhookUrl: 'https://api.example.com/webhook',
  claudeApiKey: 'your-claude-key',
  whatsappToken: 'your-whatsapp-token'
});

// Process message
const result = await client.processMessage({
  conversationId: 'conv_123',
  message: 'Hola, necesito ayuda con mi departamento',
  userMetadata: { name: 'María', phone: '+5215551234567' }
});

console.log(`Intent: ${result.classification.intent}`);
console.log(`Response: ${result.aiResponse}`);
```

---

This API reference provides comprehensive coverage of all system components. For implementation details, refer to the source code in the respective directories.