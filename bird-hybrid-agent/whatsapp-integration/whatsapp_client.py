"""
WhatsApp Business API Client for Bird.com Hybrid AI
Comprehensive integration with WhatsApp Business API including 
message templates, rich media, session management, and compliance.
"""

import os
import json
import time
import uuid
import base64
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import requests
import boto3
from botocore.exceptions import ClientError

# AWS Powertools for observability
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

# Initialize observability tools
logger = Logger(service="whatsapp-integration")
tracer = Tracer(service="whatsapp-integration")
metrics = Metrics(namespace="UrbanHub/WhatsAppIntegration")

@dataclass
class WhatsAppMessage:
    """Structure for WhatsApp messages"""
    to: str  # Phone number in international format
    type: str  # text, image, document, audio, template
    content: Union[str, Dict[str, Any]]
    message_id: str = None
    timestamp: datetime = None
    reply_to: str = None  # Message ID being replied to
    
    def __post_init__(self):
        if self.message_id is None:
            self.message_id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class WhatsAppUser:
    """Structure for WhatsApp users"""
    phone: str
    name: str = ""
    profile_pic: str = ""
    language: str = "es"
    is_business: bool = False
    last_seen: datetime = None

@dataclass  
class WhatsAppSession:
    """Structure for WhatsApp conversation sessions"""
    phone: str
    session_id: str
    start_time: datetime
    last_activity: datetime
    message_count: int = 0
    session_type: str = "standard"  # standard, support, sales
    context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}

class WhatsAppTemplateManager:
    """Manages WhatsApp message templates and compliance"""
    
    def __init__(self):
        # Pre-approved message templates (these need Meta approval)
        self.templates = {
            'welcome': {
                'name': 'urbanhub_welcome',
                'language': 'es_MX',
                'components': [
                    {
                        'type': 'BODY',
                        'text': '¡Hola {{1}}! 👋 Bienvenido a UrbanHub. Soy tu asistente personal y estoy aquí para ayudarte a encontrar tu nuevo hogar. ¿En qué puedo ayudarte hoy?'
                    }
                ]
            },
            
            'tour_confirmation': {
                'name': 'urbanhub_tour_confirmation',
                'language': 'es_MX', 
                'components': [
                    {
                        'type': 'BODY',
                        'text': '✅ ¡Perfecto! Tu tour en {{1}} está confirmado para el {{2}} a las {{3}}. Te enviaremos un recordatorio 24h antes. ¿Tienes alguna pregunta específica sobre la propiedad?'
                    }
                ]
            },
            
            'maintenance_scheduled': {
                'name': 'urbanhub_maintenance_scheduled', 
                'language': 'es_MX',
                'components': [
                    {
                        'type': 'BODY',
                        'text': '🔧 Tu solicitud de mantenimiento #{{1}} ha sido programada. Un técnico llegará el {{2}} entre {{3}}. Por favor asegúrate de estar disponible. ¿Necesitas reprogramar?'
                    }
                ]
            },
            
            'payment_reminder': {
                'name': 'urbanhub_payment_reminder',
                'language': 'es_MX',
                'components': [
                    {
                        'type': 'BODY',
                        'text': '💰 Recordatorio: Tu pago de ${{1}} MXN vence el {{2}}. Puedes pagar desde tu app UrbanHub o con tu ejecutivo. ¿Necesitas ayuda con el proceso de pago?'
                    }
                ]
            }
        }
    
    def get_template(self, template_name: str, parameters: List[str]) -> Dict[str, Any]:
        """Get formatted template with parameters"""
        
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} not found")
        
        template = self.templates[template_name].copy()
        
        # Replace parameters in template
        for component in template['components']:
            if component['type'] == 'BODY':
                text = component['text']
                for i, param in enumerate(parameters, 1):
                    text = text.replace(f'{{{{{i}}}}}', param)
                component['text'] = text
        
        return template
    
    def validate_template_usage(self, template_name: str, user_phone: str) -> bool:
        """Validate if template can be sent to user (24h rule compliance)"""
        
        # Check 24-hour window for template messages
        # This would typically query a database of recent messages
        # For now, return True (implement proper validation in production)
        return True

class WhatsAppClient:
    """Main WhatsApp Business API client"""
    
    def __init__(self):
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.access_token = os.environ['WHATSAPP_ACCESS_TOKEN']
        self.phone_number_id = os.environ['WHATSAPP_PHONE_NUMBER_ID'] 
        self.verify_token = os.environ['WHATSAPP_VERIFY_TOKEN']
        
        # AWS services
        self.s3_client = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Storage configuration
        self.media_bucket = os.environ.get('WHATSAPP_MEDIA_BUCKET', 'urbanhub-whatsapp-media')
        self.session_table = self.dynamodb.Table(os.environ.get('WHATSAPP_SESSION_TABLE', 'whatsapp-sessions'))
        
        # Initialize template manager
        self.template_manager = WhatsAppTemplateManager()
        
        # Headers for API requests
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    @tracer.capture_method
    def send_text_message(self, to: str, text: str, reply_to: str = None) -> Dict[str, Any]:
        """Send a text message"""
        
        message_payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'text',
            'text': {
                'preview_url': True,
                'body': text
            }
        }
        
        # Add reply context if provided
        if reply_to:
            message_payload['context'] = {'message_id': reply_to}
        
        return self._send_message(message_payload)
    
    @tracer.capture_method
    def send_template_message(self, to: str, template_name: str, parameters: List[str]) -> Dict[str, Any]:
        """Send a template message (for notifications outside 24h window)"""
        
        # Validate template usage
        if not self.template_manager.validate_template_usage(template_name, to):
            raise ValueError(f"Template {template_name} cannot be sent to {to} - 24h window exceeded")
        
        # Get template
        template = self.template_manager.get_template(template_name, parameters)
        
        message_payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'template',
            'template': {
                'name': template['name'],
                'language': {
                    'code': template['language']
                },
                'components': template['components']
            }
        }
        
        return self._send_message(message_payload)
    
    @tracer.capture_method
    def send_image_message(self, to: str, image_url: str, caption: str = "", reply_to: str = None) -> Dict[str, Any]:
        """Send an image message"""
        
        message_payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'image',
            'image': {
                'link': image_url,
                'caption': caption
            }
        }
        
        if reply_to:
            message_payload['context'] = {'message_id': reply_to}
        
        return self._send_message(message_payload)
    
    @tracer.capture_method
    def send_document_message(self, to: str, document_url: str, filename: str, caption: str = "", reply_to: str = None) -> Dict[str, Any]:
        """Send a document message"""
        
        message_payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'document',
            'document': {
                'link': document_url,
                'filename': filename,
                'caption': caption
            }
        }
        
        if reply_to:
            message_payload['context'] = {'message_id': reply_to}
        
        return self._send_message(message_payload)
    
    @tracer.capture_method
    def send_audio_message(self, to: str, audio_url: str, reply_to: str = None) -> Dict[str, Any]:
        """Send an audio message"""
        
        message_payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'audio',
            'audio': {
                'link': audio_url
            }
        }
        
        if reply_to:
            message_payload['context'] = {'message_id': reply_to}
        
        return self._send_message(message_payload)
    
    @tracer.capture_method
    def send_interactive_list(self, to: str, header_text: str, body_text: str, footer_text: str, 
                            button_text: str, sections: List[Dict], reply_to: str = None) -> Dict[str, Any]:
        """Send an interactive list message"""
        
        message_payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'interactive',
            'interactive': {
                'type': 'list',
                'header': {
                    'type': 'text',
                    'text': header_text
                },
                'body': {
                    'text': body_text
                },
                'footer': {
                    'text': footer_text
                },
                'action': {
                    'button': button_text,
                    'sections': sections
                }
            }
        }
        
        if reply_to:
            message_payload['context'] = {'message_id': reply_to}
        
        return self._send_message(message_payload)
    
    @tracer.capture_method
    def send_interactive_buttons(self, to: str, body_text: str, buttons: List[Dict], 
                                header_text: str = "", footer_text: str = "", reply_to: str = None) -> Dict[str, Any]:
        """Send an interactive buttons message"""
        
        interactive_payload = {
            'type': 'button',
            'body': {'text': body_text},
            'action': {'buttons': buttons}
        }
        
        if header_text:
            interactive_payload['header'] = {'type': 'text', 'text': header_text}
        
        if footer_text:
            interactive_payload['footer'] = {'text': footer_text}
        
        message_payload = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'interactive',
            'interactive': interactive_payload
        }
        
        if reply_to:
            message_payload['context'] = {'message_id': reply_to}
        
        return self._send_message(message_payload)
    
    @tracer.capture_method
    def _send_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Internal method to send message via WhatsApp API"""
        
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        try:
            start_time = time.time()
            
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            response.raise_for_status()
            result = response.json()
            
            # Add metrics
            metrics.add_metric("WhatsAppMessageSent", 1, MetricUnit.Count)
            metrics.add_metric("WhatsAppAPILatency", processing_time_ms, MetricUnit.Milliseconds)
            
            logger.info("WhatsApp message sent successfully", 
                       message_id=result.get('messages', [{}])[0].get('id'),
                       to=payload.get('to'),
                       type=payload.get('type'))
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"WhatsApp API request failed: {str(e)}")
            metrics.add_metric("WhatsAppAPIErrors", 1, MetricUnit.Count)
            raise
        except Exception as e:
            logger.error(f"Unexpected error sending WhatsApp message: {str(e)}")
            raise
    
    @tracer.capture_method
    def download_media(self, media_id: str) -> Optional[bytes]:
        """Download media from WhatsApp"""
        
        try:
            # Get media URL
            url = f"{self.base_url}/{media_id}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            media_info = response.json()
            media_url = media_info.get('url')
            
            if not media_url:
                logger.error(f"No URL found for media {media_id}")
                return None
            
            # Download media content
            media_response = requests.get(
                media_url, 
                headers=self.headers,
                timeout=60
            )
            media_response.raise_for_status()
            
            return media_response.content
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download media {media_id}: {str(e)}")
            return None
    
    @tracer.capture_method
    def store_media_in_s3(self, media_content: bytes, media_type: str, conversation_id: str) -> str:
        """Store media content in S3"""
        
        timestamp = int(time.time())
        
        # Determine file extension
        extensions = {
            'image': 'jpg',
            'audio': 'ogg',
            'document': 'pdf',
            'video': 'mp4'
        }
        extension = extensions.get(media_type, 'bin')
        
        # Generate S3 key
        s3_key = f"whatsapp-media/{conversation_id}/{timestamp}.{extension}"
        
        try:
            self.s3_client.put_object(
                Bucket=self.media_bucket,
                Key=s3_key,
                Body=media_content,
                ContentType=self._get_content_type(media_type)
            )
            
            return f"s3://{self.media_bucket}/{s3_key}"
            
        except ClientError as e:
            logger.error(f"Failed to store media in S3: {str(e)}")
            raise
    
    def _get_content_type(self, media_type: str) -> str:
        """Get MIME content type for media"""
        types = {
            'image': 'image/jpeg',
            'audio': 'audio/ogg',
            'document': 'application/pdf',
            'video': 'video/mp4'
        }
        return types.get(media_type, 'application/octet-stream')
    
    @tracer.capture_method
    def get_or_create_session(self, phone: str, message_type: str = "standard") -> WhatsAppSession:
        """Get existing session or create new one"""
        
        try:
            # Check for existing active session
            response = self.session_table.get_item(
                Key={'phone': phone}
            )
            
            if 'Item' in response:
                item = response['Item']
                
                # Check if session is still active (within 24 hours)
                last_activity = datetime.fromisoformat(item['last_activity'])
                if datetime.now() - last_activity < timedelta(hours=24):
                    # Update last activity
                    session = WhatsAppSession(
                        phone=item['phone'],
                        session_id=item['session_id'],
                        start_time=datetime.fromisoformat(item['start_time']),
                        last_activity=datetime.now(),
                        message_count=item.get('message_count', 0) + 1,
                        session_type=item.get('session_type', 'standard'),
                        context=item.get('context', {})
                    )
                    
                    self._save_session(session)
                    return session
            
            # Create new session
            session = WhatsAppSession(
                phone=phone,
                session_id=str(uuid.uuid4()),
                start_time=datetime.now(),
                last_activity=datetime.now(),
                message_count=1,
                session_type=message_type,
                context={}
            )
            
            self._save_session(session)
            return session
            
        except ClientError as e:
            logger.error(f"Failed to get/create session: {str(e)}")
            # Return temporary session
            return WhatsAppSession(
                phone=phone,
                session_id=str(uuid.uuid4()),
                start_time=datetime.now(),
                last_activity=datetime.now(),
                session_type=message_type
            )
    
    @tracer.capture_method  
    def _save_session(self, session: WhatsAppSession):
        """Save session to DynamoDB"""
        
        try:
            self.session_table.put_item(
                Item={
                    'phone': session.phone,
                    'session_id': session.session_id,
                    'start_time': session.start_time.isoformat(),
                    'last_activity': session.last_activity.isoformat(),
                    'message_count': session.message_count,
                    'session_type': session.session_type,
                    'context': session.context,
                    'ttl': int(time.time()) + (7 * 24 * 3600)  # 7 days TTL
                }
            )
        except ClientError as e:
            logger.error(f"Failed to save session: {str(e)}")
    
    @tracer.capture_method
    def mark_message_as_read(self, message_id: str) -> bool:
        """Mark message as read"""
        
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            'messaging_product': 'whatsapp',
            'status': 'read',
            'message_id': message_id
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to mark message as read: {str(e)}")
            return False
    
    # Helper methods for creating interactive content
    
    def create_property_list(self, properties: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create interactive list for property selection"""
        
        sections = [{
            'title': 'Propiedades Disponibles',
            'rows': []
        }]
        
        for prop in properties[:10]:  # WhatsApp limit is 10 items
            sections[0]['rows'].append({
                'id': prop['id'],
                'title': prop['name'],
                'description': f"${prop['price']:,} MXN - {prop['location']}"
            })
        
        return {
            'header_text': '🏠 Propiedades UrbanHub',
            'body_text': 'Selecciona una propiedad para obtener más información:',
            'footer_text': 'Powered by UrbanHub AI',
            'button_text': 'Ver Propiedades',
            'sections': sections
        }
    
    def create_tour_buttons(self, property_name: str) -> List[Dict[str, Any]]:
        """Create interactive buttons for tour booking"""
        
        return [
            {
                'type': 'reply',
                'reply': {
                    'id': f'tour_today_{property_name}',
                    'title': '📅 Hoy'
                }
            },
            {
                'type': 'reply', 
                'reply': {
                    'id': f'tour_tomorrow_{property_name}',
                    'title': '📅 Mañana'
                }
            },
            {
                'type': 'reply',
                'reply': {
                    'id': f'tour_custom_{property_name}',
                    'title': '📅 Otra fecha'
                }
            }
        ]

# Webhook verification helper
def verify_webhook(mode: str, token: str, challenge: str) -> Optional[str]:
    """Verify WhatsApp webhook"""
    
    verify_token = os.environ.get('WHATSAPP_VERIFY_TOKEN')
    
    if mode == "subscribe" and token == verify_token:
        logger.info("Webhook verified successfully")
        return challenge
    else:
        logger.warning("Webhook verification failed")
        return None

# Export main classes
__all__ = ['WhatsAppClient', 'WhatsAppMessage', 'WhatsAppSession', 'WhatsAppTemplateManager', 'verify_webhook']