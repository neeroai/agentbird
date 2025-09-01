"""
Bird.com Webhook Processor - Main Handler
AWS Lambda function for processing Bird.com webhooks with Claude integration

This handler implements the Webhook Enhancement Pattern:
Bird.com webhook → AWS Lambda → Enhanced processing → Response to Bird.com
"""

import json
import os
import time
import hmac
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# AWS Powertools for observability
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.metrics import MetricUnit
import anthropic

# Initialize AWS Powertools
logger = Logger(service="bird-webhook-processor")
tracer = Tracer(service="bird-webhook-processor")  
metrics = Metrics(namespace="UrbanHub/BirdIntegration")

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
eventbridge = boto3.client('events')

# Initialize Claude client
claude_client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

# Environment variables
CONVERSATION_TABLE = os.environ['CONVERSATION_TABLE']
ANALYSIS_TABLE = os.environ['ANALYSIS_TABLE']
EVENT_BUS_NAME = os.environ['EVENT_BUS_NAME']
WEBHOOK_SECRET = os.environ['WEBHOOK_SECRET']
S3_BUCKET = os.environ['MEDIA_BUCKET']

class WebhookProcessor:
    """Enhanced webhook processor with multi-agent routing capabilities"""
    
    def __init__(self):
        self.conversation_table = dynamodb.Table(CONVERSATION_TABLE)
        self.analysis_table = dynamodb.Table(ANALYSIS_TABLE)
        
        # Agent routing configuration
        self.agent_routing = {
            'maintenance': {
                'keywords': ['problema', 'fuga', 'no funciona', 'reparar', 'aire acondicionado', 'plomería'],
                'confidence_threshold': 0.8,
                'priority': 'urgent'
            },
            'leasing': {
                'keywords': ['precio', 'disponible', 'tour', 'renta', 'contrato', 'propiedad'],
                'confidence_threshold': 0.85,
                'priority': 'high'
            },
            'payments': {
                'keywords': ['pago', 'recibo', 'factura', 'cobro', 'tarjeta'],
                'confidence_threshold': 0.9,
                'priority': 'medium'
            },
            'amenities': {
                'keywords': ['gym', 'co-working', 'azotea', 'terraza', 'mascotas', 'reserva'],
                'confidence_threshold': 0.8,
                'priority': 'low'
            }
        }
    
    @tracer.capture_method
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """Verify Bird.com webhook HMAC signature"""
        try:
            expected_signature = hmac.new(
                WEBHOOK_SECRET.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Remove 'sha256=' prefix if present
            if signature.startswith('sha256='):
                signature = signature[7:]
                
            return hmac.compare_digest(expected_signature, signature)
        except Exception as e:
            logger.error("Signature verification failed", error=str(e))
            return False
    
    @tracer.capture_method
    async def classify_intent_with_claude(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Use Claude to classify user intent and extract entities"""
        
        prompt = f"""
        Analiza el siguiente mensaje de WhatsApp y clasifica la intención del usuario.
        
        Mensaje: "{message.get('text', '')}"
        Usuario: {message.get('sender', {}).get('name', 'Anónimo')}
        Contexto: {message.get('context', {})}
        
        Categorías posibles:
        1. MANTENIMIENTO - Problemas técnicos, reparaciones, fallas
        2. LEASING - Información de propiedades, precios, tours  
        3. PAGOS - Facturación, recibos, problemas de pago
        4. AMENIDADES - Reservas, uso de espacios comunes
        5. OTROS - Consultas generales
        
        Responde en formato JSON con:
        {{
            "intent": "categoria_principal",
            "confidence": 0.95,
            "entities": {{"urgency": "high/medium/low", "property": "nombre_si_aplica"}},
            "routing_recommendation": "agent_sugerido",
            "reasoning": "justificación_breve"
        }}
        """
        
        try:
            response = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            classification = json.loads(response.content[0].text)
            
            # Add processing metadata
            classification['processed_at'] = datetime.now().isoformat()
            classification['processing_time_ms'] = time.time() * 1000
            
            return classification
            
        except Exception as e:
            logger.error("Claude classification failed", error=str(e))
            # Fallback to keyword-based classification
            return self.fallback_classify_intent(message)
    
    @tracer.capture_method
    def fallback_classify_intent(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback keyword-based intent classification"""
        
        text = message.get('text', '').lower()
        max_score = 0
        best_intent = 'others'
        
        for intent, config in self.agent_routing.items():
            score = sum(1 for keyword in config['keywords'] if keyword in text)
            if score > max_score:
                max_score = score
                best_intent = intent
        
        confidence = min(0.8, max_score * 0.2)  # Simple confidence calculation
        
        return {
            'intent': best_intent,
            'confidence': confidence,
            'entities': {'urgency': 'medium'},
            'routing_recommendation': f'{best_intent}-agent',
            'reasoning': f'Keyword matching with {max_score} matches'
        }
    
    @tracer.capture_method
    async def store_conversation_state(self, conversation_id: str, data: Dict[str, Any]):
        """Store conversation state in DynamoDB"""
        try:
            self.conversation_table.put_item(
                Item={
                    'conversation_id': conversation_id,
                    'timestamp': datetime.now().isoformat(),
                    'message_data': data,
                    'ttl': int(time.time()) + (30 * 24 * 3600)  # 30 days TTL
                }
            )
        except ClientError as e:
            logger.error("Failed to store conversation state", error=str(e))
            raise
    
    @tracer.capture_method
    async def store_analysis_result(self, conversation_id: str, analysis: Dict[str, Any]):
        """Store intent analysis result"""
        try:
            self.analysis_table.put_item(
                Item={
                    'conversation_id': conversation_id,
                    'analysis_timestamp': datetime.now().isoformat(),
                    'intent_analysis': analysis,
                    'ttl': int(time.time()) + (90 * 24 * 3600)  # 90 days TTL
                }
            )
        except ClientError as e:
            logger.error("Failed to store analysis result", error=str(e))
            raise
    
    @tracer.capture_method
    async def publish_routing_event(self, classification: Dict[str, Any], message_data: Dict[str, Any]):
        """Publish agent routing event to EventBridge"""
        
        event_detail = {
            'routing_decision': classification,
            'message_data': message_data,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            response = eventbridge.put_events(
                Entries=[
                    {
                        'Source': 'urbanhub.bird.webhook',
                        'DetailType': 'Agent Routing Required',
                        'Detail': json.dumps(event_detail),
                        'EventBusName': EVENT_BUS_NAME
                    }
                ]
            )
            
            logger.info("Published routing event", event_id=response['Entries'][0].get('EventId'))
            
        except ClientError as e:
            logger.error("Failed to publish routing event", error=str(e))
            raise
    
    @tracer.capture_method
    async def process_multimodal_content(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process multimedia content (images, voice, documents)"""
        
        content_analysis = {
            'has_media': False,
            'media_types': [],
            'processing_required': []
        }
        
        # Check for different content types
        if message.get('type') == 'image':
            content_analysis['has_media'] = True
            content_analysis['media_types'].append('image')
            content_analysis['processing_required'].append('visual-analyzer')
            
        elif message.get('type') == 'voice':
            content_analysis['has_media'] = True
            content_analysis['media_types'].append('voice')
            content_analysis['processing_required'].append('voice-assistant')
            
        elif message.get('type') == 'document':
            content_analysis['has_media'] = True
            content_analysis['media_types'].append('document')
            content_analysis['processing_required'].append('document-processor')
        
        # Store media in S3 if present
        if content_analysis['has_media']:
            media_url = await self.store_media_in_s3(message)
            content_analysis['s3_url'] = media_url
        
        return content_analysis

    @tracer.capture_method
    async def store_media_in_s3(self, message: Dict[str, Any]) -> str:
        """Store multimedia content in S3"""
        
        conversation_id = message.get('conversation_id')
        timestamp = int(time.time())
        
        # Generate S3 key
        file_extension = self.get_file_extension(message.get('type'))
        s3_key = f"media/{conversation_id}/{timestamp}.{file_extension}"
        
        try:
            # Store media content (assuming base64 encoded)
            media_content = message.get('media_data', '')
            
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=media_content,
                ContentType=self.get_content_type(message.get('type'))
            )
            
            return f"s3://{S3_BUCKET}/{s3_key}"
            
        except ClientError as e:
            logger.error("Failed to store media in S3", error=str(e))
            raise
    
    def get_file_extension(self, media_type: str) -> str:
        """Get appropriate file extension for media type"""
        extensions = {
            'image': 'jpg',
            'voice': 'ogg', 
            'document': 'pdf',
            'video': 'mp4'
        }
        return extensions.get(media_type, 'bin')
    
    def get_content_type(self, media_type: str) -> str:
        """Get MIME content type for media"""
        types = {
            'image': 'image/jpeg',
            'voice': 'audio/ogg',
            'document': 'application/pdf',
            'video': 'video/mp4'
        }
        return types.get(media_type, 'application/octet-stream')


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Main Lambda handler for Bird.com webhook processing"""
    
    processor = WebhookProcessor()
    
    try:
        # Parse the incoming webhook
        if isinstance(event, dict) and 'body' in event:
            # API Gateway event
            body = event['body']
            headers = event.get('headers', {})
        else:
            # Direct invocation
            body = json.dumps(event)
            headers = {}
        
        # Verify webhook signature
        signature = headers.get('x-bird-signature', '')
        if not processor.verify_webhook_signature(body, signature):
            logger.warning("Invalid webhook signature")
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Invalid signature'})
            }
        
        # Parse message data
        message_data = json.loads(body)
        conversation_id = message_data.get('conversation_id')
        message = message_data.get('message', {})
        
        logger.info("Processing webhook", conversation_id=conversation_id)
        
        # Classify intent using Claude
        classification = processor.classify_intent_with_claude(message)
        
        # Process multimodal content
        media_analysis = processor.process_multimodal_content(message)
        
        # Combine analysis results
        enhanced_analysis = {
            **classification,
            'media_analysis': media_analysis,
            'conversation_id': conversation_id
        }
        
        # Store conversation state and analysis
        processor.store_conversation_state(conversation_id, message_data)
        processor.store_analysis_result(conversation_id, enhanced_analysis)
        
        # Publish routing event for specialized agents
        processor.publish_routing_event(enhanced_analysis, message_data)
        
        # Add metrics
        metrics.add_metric("WebhookProcessed", 1, MetricUnit.Count)
        metrics.add_metric("IntentClassified", 1, MetricUnit.Count)
        
        if enhanced_analysis['confidence'] > 0.9:
            metrics.add_metric("HighConfidenceClassification", 1, MetricUnit.Count)
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'X-Processing-Time': str(time.time() - context.get_remaining_time_in_millis())
            },
            'body': json.dumps({
                'success': True,
                'conversation_id': conversation_id,
                'classification': {
                    'intent': enhanced_analysis['intent'],
                    'confidence': enhanced_analysis['confidence'],
                    'routing_recommendation': enhanced_analysis['routing_recommendation']
                },
                'media_processed': enhanced_analysis['media_analysis']['has_media']
            })
        }
        
    except Exception as e:
        logger.error("Webhook processing failed", error=str(e))
        metrics.add_metric("WebhookErrors", 1, MetricUnit.Count)
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal processing error',
                'message': str(e)
            })
        }


# Export for testing
__all__ = ['lambda_handler', 'WebhookProcessor']