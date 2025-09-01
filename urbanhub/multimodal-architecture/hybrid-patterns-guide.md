# 🔄 Patrones Híbridos Bird.com + AWS - Guía Técnica Avanzada

## 📋 Resumen de Patrones

Esta guía documenta los **patrones híbridos optimizados** para integrar Bird.com con AWS Serverless, basados en investigación de **LangChain**, **AWS Powertools** y mejores prácticas de arquitecturas multimodales.

### 🎯 Principios de los Patrones Híbridos

#### **1. Manual-First Configuration**
- **Bird.com GUI Only**: Configuración 100% manual sin APIs
- **Step-by-Step Workflows**: Procesos documentados paso a paso
- **Native Feature Usage**: Uso exclusivo de funcionalidades nativas
- **Visual Validation**: Validación visual de cada configuración

#### **2. Event-Driven Integration**
- **Webhook-First**: Bird.com como trigger principal
- **Event Streaming**: AWS EventBridge para orquestación
- **Asynchronous Processing**: Procesamiento no bloqueante
- **Real-time Responses**: WebSocket para updates inmediatos

#### **3. Serverless-Native Architecture**
- **Lambda Functions**: Procesamiento específico y escalable
- **Step Functions**: Workflows complejos de múltiples pasos
- **DynamoDB**: Estado conversacional persistente
- **S3**: Almacenamiento multimodal optimizado

## 🔄 Patrón 1: Webhook Enhancement Pattern

### **Descripción**
Bird.com webhook → AWS Lambda → Processing enhancement → Response to Bird.com

### **Implementación**

```python
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.validation import validate
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
import json

# Initialize Powertools
logger = Logger(service="bird-webhook-processor")
tracer = Tracer(service="bird-webhook-processor")
metrics = Metrics(namespace="UrbanHub/BirdIntegration")

@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def bird_webhook_handler(event: dict, context: LambdaContext) -> dict:
    """
    Enhanced webhook handler with AWS Powertools optimization
    Processes Bird.com webhooks with advanced capabilities
    """
    try:
        # Validate webhook payload
        validated_event = validate_bird_webhook(event)
        
        # Extract conversation context
        conversation_context = extract_conversation_context(validated_event)
        
        # Route to appropriate processor based on intent
        processor = select_processor(conversation_context)
        
        # Process with enhanced capabilities
        enhanced_response = processor.process_with_enhancement(
            conversation_context,
            aws_services={
                'bedrock': get_bedrock_client(),
                'textract': get_textract_client(),
                'comprehend': get_comprehend_client()
            }
        )
        
        # Update conversation state
        update_conversation_state(conversation_context.id, enhanced_response)
        
        # Add metrics
        metrics.add_metric("WebhookProcessed", 1, "Count")
        metrics.add_metric("ProcessingLatency", enhanced_response.latency, "Milliseconds")
        
        return format_bird_response(enhanced_response)
        
    except Exception as e:
        logger.error("Webhook processing failed", error=str(e))
        metrics.add_metric("WebhookErrors", 1, "Count")
        return create_error_response(str(e))

def validate_bird_webhook(event):
    """Validate Bird.com webhook payload"""
    schema = {
        "type": "object",
        "required": ["conversation_id", "user_id", "message"],
        "properties": {
            "conversation_id": {"type": "string"},
            "user_id": {"type": "string"}, 
            "message": {
                "type": "object",
                "required": ["text", "timestamp"],
                "properties": {
                    "text": {"type": "string"},
                    "timestamp": {"type": "string"},
                    "attachments": {"type": "array"},
                    "metadata": {"type": "object"}
                }
            }
        }
    }
    
    return validate(event=event, schema=schema)
```

### **Configuración en Bird.com**

#### **Paso 1: Configurar Webhook URL**
```
1. Ir a Settings → Integrations → Webhooks
2. URL: https://your-api-gateway.amazonaws.com/prod/webhook
3. Headers: 
   - Content-Type: application/json
   - X-API-Key: {your-api-key}
   - X-Bird-Signature: {calculated-signature}
4. Events: message.received, conversation.started, conversation.ended
```

#### **Paso 2: Configurar Request Body Template**
```json
{
  "conversation_id": "{{conversation.id}}",
  "user_id": "{{contact.id}}",
  "channel": "{{channel.type}}",
  "timestamp": "{{timestamp}}",
  "message": {
    "text": "{{message.content}}",
    "attachments": [
      {% for attachment in message.attachments %}
      {
        "type": "{{attachment.type}}",
        "url": "{{attachment.url}}",
        "filename": "{{attachment.filename}}"
      }{% unless forloop.last %},{% endunless %}
      {% endfor %}
    ],
    "metadata": {
      "intent": "{{message.intent}}",
      "confidence": {{message.confidence}},
      "language": "{{contact.language | default: 'es'}}"
    }
  },
  "context": {
    "conversation_history": [
      {% for msg in conversation.recent_messages limit:5 %}
      {
        "role": "{{msg.role}}",
        "content": "{{msg.content}}",
        "timestamp": "{{msg.timestamp}}"
      }{% unless forloop.last %},{% endunless %}
      {% endfor %}
    ],
    "user_profile": {
      "name": "{{contact.name}}",
      "phone": "{{contact.phone}}",
      "email": "{{contact.email}}",
      "properties": {
        "property_interest": "{{contact.custom.property_interest}}",
        "budget_range": "{{contact.custom.budget_range}}",
        "preferred_location": "{{contact.custom.preferred_location}}"
      }
    }
  }
}
```

## 🔄 Patrón 2: Multimodal Processing Pattern  

### **Descripción**
Procesamiento unificado de múltiples tipos de entrada con AWS services especializados.

### **Implementación**

```python
class MultimodalProcessor:
    """
    Procesador multimodal usando AWS services
    Implementa patrón de procesamiento unificado
    """
    
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime')
        self.textract = boto3.client('textract') 
        self.comprehend = boto3.client('comprehend')
        self.transcribe = boto3.client('transcribe')
        self.rekognition = boto3.client('rekognition')
        
        self.logger = Logger(service="multimodal-processor")
        self.tracer = Tracer(service="multimodal-processor")
        
    @tracer.capture_method
    def process_unified_input(self, multimodal_data):
        """
        Process multiple input modalities in unified pipeline
        """
        processing_results = {}
        
        # Text processing
        if multimodal_data.text:
            processing_results['text'] = self._process_text(multimodal_data.text)
            
        # Voice processing  
        if multimodal_data.audio_url:
            processing_results['voice'] = self._process_audio(multimodal_data.audio_url)
            
        # Image processing
        if multimodal_data.image_url:
            processing_results['image'] = self._process_image(multimodal_data.image_url)
            
        # Document processing
        if multimodal_data.document_url:
            processing_results['document'] = self._process_document(multimodal_data.document_url)
            
        # Unified understanding
        unified_response = self._create_unified_understanding(processing_results)
        
        return unified_response
        
    def _process_text(self, text):
        """Enhanced text processing with Comprehend + Bedrock"""
        # Sentiment analysis
        sentiment = self.comprehend.detect_sentiment(
            Text=text,
            LanguageCode='es'
        )
        
        # Entity extraction
        entities = self.comprehend.detect_entities(
            Text=text,
            LanguageCode='es'
        )
        
        # Intent enhancement with Bedrock
        bedrock_analysis = self.bedrock.invoke_model(
            modelId='anthropic.claude-v2',
            body=json.dumps({
                'prompt': f"""
                Analiza el siguiente texto de un cliente de bienes raíces:
                "{text}"
                
                Extrae:
                1. Intención principal (leasing, mantenimiento, consulta)
                2. Nivel de urgencia (alto, medio, bajo)
                3. Información específica de propiedad mencionada
                4. Respuesta recomendada
                
                Formato JSON.
                """,
                'max_tokens_to_sample': 300
            })
        )
        
        return {
            'sentiment': sentiment,
            'entities': entities['Entities'],
            'bedrock_analysis': json.loads(bedrock_analysis['body'].read())
        }
        
    def _process_audio(self, audio_url):
        """Voice processing with Transcribe + analysis"""
        # Start transcription job
        job_name = f"transcribe-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        self.transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': audio_url},
            MediaFormat='mp3',
            LanguageCode='es-ES'
        )
        
        # Wait for completion (implement polling)
        transcription_result = self._wait_for_transcription(job_name)
        
        # Enhanced analysis of transcribed text
        if transcription_result:
            text_analysis = self._process_text(transcription_result['text'])
            
            return {
                'transcription': transcription_result,
                'text_analysis': text_analysis,
                'audio_metadata': {
                    'duration': transcription_result.get('duration'),
                    'confidence': transcription_result.get('confidence')
                }
            }
            
    def _process_image(self, image_url):
        """Image processing with Rekognition + Textract"""
        # Download image from S3 
        s3_bucket, s3_key = self._parse_s3_url(image_url)
        
        # Object detection with Rekognition
        objects = self.rekognition.detect_labels(
            Image={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
            MaxLabels=10,
            MinConfidence=80
        )
        
        # Text extraction with Textract (if document/text visible)
        try:
            text_detection = self.textract.detect_document_text(
                Document={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}}
            )
            
            extracted_text = self._extract_text_from_textract(text_detection)
            text_analysis = self._process_text(extracted_text) if extracted_text else None
            
        except Exception as e:
            text_analysis = None
            extracted_text = None
            
        return {
            'objects': objects['Labels'],
            'extracted_text': extracted_text,
            'text_analysis': text_analysis,
            'image_metadata': self._get_image_metadata(s3_bucket, s3_key)
        }
        
    def _process_document(self, document_url):
        """Document processing with Textract + classification"""
        s3_bucket, s3_key = self._parse_s3_url(document_url)
        
        # Extract text and structure
        textract_response = self.textract.analyze_document(
            Document={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
            FeatureTypes=['TABLES', 'FORMS']
        )
        
        # Extract structured data
        extracted_data = self._extract_structured_data(textract_response)
        
        # Document classification
        document_type = self._classify_document(extracted_data['text'])
        
        # Specialized processing based on document type
        if document_type == 'lease_contract':
            analysis = self._analyze_lease_contract(extracted_data)
        elif document_type == 'income_verification':
            analysis = self._analyze_income_document(extracted_data)
        elif document_type == 'identification':
            analysis = self._analyze_identification(extracted_data)
        else:
            analysis = self._analyze_generic_document(extracted_data)
            
        return {
            'document_type': document_type,
            'extracted_data': extracted_data,
            'analysis': analysis
        }
```

## 🔄 Patrón 3: State Management Pattern

### **Descripción** 
Gestión de estado conversacional persistente con DynamoDB + Redis para alta performance.

### **Implementación**

```python
class ConversationStateManager:
    """
    Gestión avanzada de estado conversacional
    DynamoDB para persistencia + Redis para cache
    """
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.redis = redis.Redis.from_url(os.environ.get('REDIS_URL'))
        self.table = self.dynamodb.Table('UrbanHub-ConversationState')
        
        self.logger = Logger(service="state-manager")
        self.tracer = Tracer(service="state-manager")
        
    @tracer.capture_method
    def get_conversation_context(self, conversation_id: str, user_id: str):
        """
        Get complete conversation context with caching
        """
        cache_key = f"conversation:{conversation_id}"
        
        # Try Redis cache first
        cached_context = self.redis.get(cache_key)
        if cached_context:
            self.logger.info("Context retrieved from cache")
            return json.loads(cached_context)
            
        # Fallback to DynamoDB
        try:
            response = self.table.get_item(
                Key={'conversation_id': conversation_id}
            )
            
            if 'Item' in response:
                context = response['Item']
                
                # Cache for future requests
                self.redis.setex(
                    cache_key,
                    300,  # 5 minutes TTL
                    json.dumps(context, cls=DecimalEncoder)
                )
                
                return context
            else:
                # Initialize new conversation
                return self._initialize_conversation_context(conversation_id, user_id)
                
        except Exception as e:
            self.logger.error("Error retrieving conversation context", error=str(e))
            return self._get_default_context(conversation_id, user_id)
            
    @tracer.capture_method        
    def update_conversation_context(self, conversation_id: str, updates: dict):
        """
        Update conversation context with optimistic locking
        """
        try:
            # Update DynamoDB with atomic operations
            update_expression = "SET "
            expression_values = {}
            expression_names = {}
            
            for key, value in updates.items():
                update_expression += f"#{key} = :{key}, "
                expression_names[f"#{key}"] = key
                expression_values[f":{key}"] = value
                
            # Remove trailing comma and space
            update_expression = update_expression.rstrip(", ")
            
            # Add timestamp and version for optimistic locking
            update_expression += ", #updated_at = :updated_at, #version = #version + :version_inc"
            expression_names["#updated_at"] = "updated_at"
            expression_names["#version"] = "version"
            expression_values[":updated_at"] = datetime.now().isoformat()
            expression_values[":version_inc"] = 1
            
            self.table.update_item(
                Key={'conversation_id': conversation_id},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_names,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW"
            )
            
            # Invalidate cache
            cache_key = f"conversation:{conversation_id}"
            self.redis.delete(cache_key)
            
            self.logger.info("Conversation context updated successfully")
            
        except Exception as e:
            self.logger.error("Error updating conversation context", error=str(e))
            raise e
            
    def _initialize_conversation_context(self, conversation_id: str, user_id: str):
        """Initialize new conversation with default context"""
        context = {
            'conversation_id': conversation_id,
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'version': 1,
            'state': 'active',
            'intent_history': [],
            'property_interests': [],
            'user_preferences': {},
            'conversation_summary': '',
            'last_agent': None,
            'escalation_level': 0,
            'metadata': {}
        }
        
        # Save to DynamoDB
        self.table.put_item(Item=context)
        
        return context
```

## 🔄 Patrón 4: Response Optimization Pattern

### **Descripción**
Optimización de respuestas por canal con formato adaptativo y caching inteligente.

### **Implementación**

```python
class ResponseOptimizer:
    """
    Optimización de respuestas por canal y modalidad
    Caching inteligente + formato adaptativo
    """
    
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.redis = redis.Redis.from_url(os.environ.get('REDIS_URL'))
        self.cloudfront = boto3.client('cloudfront')
        
        self.logger = Logger(service="response-optimizer")
        
    def optimize_response_for_channel(self, response_data, channel_type, user_preferences):
        """
        Optimize response based on channel characteristics
        """
        if channel_type == 'whatsapp':
            return self._optimize_for_whatsapp(response_data, user_preferences)
        elif channel_type == 'web_chat':
            return self._optimize_for_web(response_data, user_preferences)
        elif channel_type == 'voice':
            return self._optimize_for_voice(response_data, user_preferences)
        else:
            return self._optimize_generic(response_data, user_preferences)
            
    def _optimize_for_whatsapp(self, response_data, preferences):
        """WhatsApp-specific optimizations"""
        optimized = {
            'text': self._format_whatsapp_text(response_data.text),
            'media': [],
            'quick_replies': [],
            'interactive_elements': []
        }
        
        # Image optimizations for WhatsApp
        if response_data.images:
            for image in response_data.images[:3]:  # Max 3 images
                optimized_image = self._optimize_image_for_whatsapp(image)
                optimized['media'].append(optimized_image)
                
        # Document handling
        if response_data.documents:
            for doc in response_data.documents[:1]:  # Max 1 document
                optimized_doc = self._optimize_document_for_whatsapp(doc)
                optimized['media'].append(optimized_doc)
                
        # Quick replies (max 10)
        if response_data.suggested_actions:
            optimized['quick_replies'] = response_data.suggested_actions[:10]
            
        return optimized
        
    def _optimize_for_web(self, response_data, preferences):
        """Web chat optimizations"""
        return {
            'html': self._format_rich_html(response_data),
            'attachments': self._process_web_attachments(response_data.attachments),
            'interactive_cards': self._create_property_cards(response_data.properties),
            'quick_actions': response_data.suggested_actions,
            'typing_indicator': True
        }
        
    def _optimize_for_voice(self, response_data, preferences):
        """Voice-specific optimizations"""
        # Generate SSML for natural speech
        ssml_text = self._generate_ssml(
            response_data.text,
            voice_settings=preferences.get('voice', {})
        )
        
        return {
            'ssml': ssml_text,
            'text_fallback': response_data.text,
            'audio_url': self._generate_audio_if_needed(ssml_text),
            'pause_points': self._identify_pause_points(response_data.text),
            'interactive_prompts': self._create_voice_prompts(response_data.suggested_actions)
        }
```

## 📊 Métricas y Monitoreo de Patrones

### **Dashboard de Patrones Híbridos**

```python
class HybridPatternsMetrics:
    """
    Métricas específicas para patrones híbridos
    Monitoring de eficiencia y performance
    """
    
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.metrics = Metrics(namespace="UrbanHub/HybridPatterns")
        
    def track_pattern_performance(self, pattern_name, execution_data):
        """Track performance of specific hybrid pattern"""
        
        # Pattern execution metrics
        self.metrics.add_metric(
            f"{pattern_name}ExecutionTime", 
            execution_data.duration_ms, 
            "Milliseconds"
        )
        
        self.metrics.add_metric(
            f"{pattern_name}Success", 
            1 if execution_data.success else 0, 
            "Count"
        )
        
        # Pattern-specific metrics
        if pattern_name == "WebhookEnhancement":
            self.track_webhook_pattern_metrics(execution_data)
        elif pattern_name == "MultimodalProcessing":
            self.track_multimodal_pattern_metrics(execution_data)
        elif pattern_name == "StateManagement":
            self.track_state_pattern_metrics(execution_data)
        elif pattern_name == "ResponseOptimization":
            self.track_response_pattern_metrics(execution_data)
            
    def track_webhook_pattern_metrics(self, data):
        """Webhook pattern specific metrics"""
        self.metrics.add_metric("WebhookLatency", data.webhook_latency, "Milliseconds")
        self.metrics.add_metric("EnhancementLatency", data.enhancement_latency, "Milliseconds")
        self.metrics.add_metric("BirdResponseLatency", data.bird_response_latency, "Milliseconds")
        
    def track_multimodal_pattern_metrics(self, data):
        """Multimodal processing metrics"""
        self.metrics.add_metric("ModalitiesProcessed", len(data.modalities), "Count")
        self.metrics.add_metric("TextProcessingTime", data.text_processing_ms, "Milliseconds")
        self.metrics.add_metric("ImageProcessingTime", data.image_processing_ms, "Milliseconds")
        self.metrics.add_metric("AudioProcessingTime", data.audio_processing_ms, "Milliseconds")
```

---

## 📚 Próximos Pasos

1. **[Implementar Agentes Especializados](../intelligent-agents/README.md)** con estos patrones
2. **[Configurar Integraciones](../hybrid-integrations/README.md)** usando los templates
3. **[Desplegar Infraestructura](../enterprise-deployment/README.md)** con los patrones optimizados
4. **[Testing y Validación](../advanced-testing-framework/README.md)** de todos los patrones

---

**🔄 Patrones optimizados con LangChain + AWS Powertools + Bird.com**  
📅 Versión: 2.0 - Advanced Integration Patterns  
🔄 Última actualización: 2025-09-01