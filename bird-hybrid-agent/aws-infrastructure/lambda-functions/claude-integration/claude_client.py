"""
Claude Integration Client for Bird.com Hybrid AI
Advanced integration with Anthropic Claude API including context management,
prompt optimization, and response processing.
"""

import os
import json
import time
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import anthropic
import boto3
from botocore.exceptions import ClientError

# AWS Powertools for observability
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

# Initialize observability tools
logger = Logger(service="claude-integration")
tracer = Tracer(service="claude-integration") 
metrics = Metrics(namespace="UrbanHub/ClaudeIntegration")

@dataclass
class ConversationContext:
    """Conversation context structure for Claude interactions"""
    conversation_id: str
    user_id: str
    messages: List[Dict[str, Any]]
    user_preferences: Dict[str, Any] = None
    property_interests: List[str] = None
    session_start: datetime = None
    last_updated: datetime = None
    total_tokens_used: int = 0
    conversation_summary: str = ""

@dataclass
class ClaudeRequest:
    """Structure for Claude API requests"""
    prompt_type: str  # intent-classification, response-generation, multimodal-processing
    content: str
    context: ConversationContext = None
    temperature: float = 0.7
    max_tokens: int = 4000
    system_prompt: str = ""
    include_images: bool = False
    image_data: List[str] = None

@dataclass  
class ClaudeResponse:
    """Structure for Claude API responses"""
    content: str
    usage: Dict[str, int]
    model_used: str
    processing_time_ms: int
    confidence_score: float = 0.0
    metadata: Dict[str, Any] = None

class ClaudeContextManager:
    """Manages conversation context and memory optimization"""
    
    def __init__(self, dynamodb_table: str, s3_bucket: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.context_table = self.dynamodb.Table(dynamodb_table)
        self.s3_client = boto3.client('s3')
        self.s3_bucket = s3_bucket
        
        # Context management settings
        self.max_context_length = 200000  # Claude's context window
        self.max_messages_in_context = 50
        self.summarization_threshold = 40
    
    @tracer.capture_method
    def get_conversation_context(self, conversation_id: str) -> Optional[ConversationContext]:
        """Retrieve conversation context from storage"""
        try:
            response = self.context_table.get_item(
                Key={'conversation_id': conversation_id}
            )
            
            if 'Item' not in response:
                return None
            
            item = response['Item']
            
            # Convert to ConversationContext object
            context = ConversationContext(
                conversation_id=item['conversation_id'],
                user_id=item.get('user_id', ''),
                messages=item.get('messages', []),
                user_preferences=item.get('user_preferences', {}),
                property_interests=item.get('property_interests', []),
                session_start=datetime.fromisoformat(item.get('session_start', datetime.now().isoformat())),
                last_updated=datetime.fromisoformat(item.get('last_updated', datetime.now().isoformat())),
                total_tokens_used=item.get('total_tokens_used', 0),
                conversation_summary=item.get('conversation_summary', '')
            )
            
            return context
            
        except ClientError as e:
            logger.error(f"Failed to retrieve conversation context: {str(e)}")
            return None
    
    @tracer.capture_method 
    def save_conversation_context(self, context: ConversationContext):
        """Save conversation context to storage"""
        try:
            # Update timestamp
            context.last_updated = datetime.now()
            
            # Convert to DynamoDB item
            item = {
                'conversation_id': context.conversation_id,
                'user_id': context.user_id,
                'messages': context.messages,
                'user_preferences': context.user_preferences or {},
                'property_interests': context.property_interests or [],
                'session_start': context.session_start.isoformat() if context.session_start else datetime.now().isoformat(),
                'last_updated': context.last_updated.isoformat(),
                'total_tokens_used': context.total_tokens_used,
                'conversation_summary': context.conversation_summary,
                'ttl': int(time.time()) + (30 * 24 * 3600)  # 30 days TTL
            }
            
            self.context_table.put_item(Item=item)
            
            logger.info(f"Saved context for conversation {context.conversation_id}")
            
        except ClientError as e:
            logger.error(f"Failed to save conversation context: {str(e)}")
            raise
    
    @tracer.capture_method
    def optimize_context_for_claude(self, context: ConversationContext) -> List[Dict[str, str]]:
        """Optimize conversation context for Claude API call"""
        
        # If we have too many messages, summarize older ones
        if len(context.messages) > self.summarization_threshold:
            context = self._summarize_old_messages(context)
        
        # Convert to Claude message format
        claude_messages = []
        
        # Add conversation summary if available
        if context.conversation_summary:
            claude_messages.append({
                "role": "assistant",
                "content": f"[Resumen de conversación previa: {context.conversation_summary}]"
            })
        
        # Add recent messages
        recent_messages = context.messages[-self.max_messages_in_context:]
        
        for msg in recent_messages:
            claude_messages.append({
                "role": msg.get('role', 'user'),
                "content": msg.get('content', '')
            })
        
        return claude_messages
    
    @tracer.capture_method
    def _summarize_old_messages(self, context: ConversationContext) -> ConversationContext:
        """Summarize older messages to manage context length"""
        
        if len(context.messages) <= self.summarization_threshold:
            return context
        
        # Messages to summarize (older ones)
        messages_to_summarize = context.messages[:-20]  # Keep last 20 as-is
        
        # Create summarization prompt
        messages_text = "\n".join([
            f"{msg.get('role', 'user')}: {msg.get('content', '')}" 
            for msg in messages_to_summarize
        ])
        
        summary_prompt = f"""
        Resume esta conversación de WhatsApp entre un usuario y el asistente de UrbanHub, 
        manteniendo información clave sobre:
        - Preferencias de propiedades mencionadas
        - Presupuesto y requisitos
        - Propiedades específicas discutidas
        - Decisiones o compromisos establecidos
        - Estado actual de la búsqueda
        
        Conversación:
        {messages_text}
        
        Resumen:"""
        
        try:
            # Use Claude to create summary
            claude_client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
            
            response = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                temperature=0.1,
                messages=[{"role": "user", "content": summary_prompt}]
            )
            
            summary = response.content[0].text
            
            # Update context with summary and reduced messages
            context.conversation_summary = summary
            context.messages = context.messages[-20:]  # Keep only recent messages
            
            logger.info(f"Summarized {len(messages_to_summarize)} messages for conversation {context.conversation_id}")
            
        except Exception as e:
            logger.error(f"Failed to summarize messages: {str(e)}")
            # Fallback: just truncate without summary
            context.messages = context.messages[-30:]
        
        return context
    
    def estimate_token_count(self, text: str) -> int:
        """Rough estimation of token count (Claude uses ~4 chars per token)"""
        return len(text) // 4

class ClaudeClient:
    """Main Claude API client with advanced features"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
        self.context_manager = ClaudeContextManager(
            dynamodb_table=os.environ.get('CONTEXT_TABLE', 'conversation-context'),
            s3_bucket=os.environ.get('CONTEXT_BUCKET', 'claude-context-storage')
        )
        
        # Load system prompts
        self.system_prompts = self._load_system_prompts()
        
        # Model configurations
        self.model_config = {
            'intent-classification': {
                'model': 'claude-3-5-sonnet-20241022',
                'temperature': 0.1,
                'max_tokens': 1000
            },
            'response-generation': {
                'model': 'claude-3-5-sonnet-20241022', 
                'temperature': 0.7,
                'max_tokens': 4000
            },
            'multimodal-processing': {
                'model': 'claude-3-5-sonnet-20241022',
                'temperature': 0.2,
                'max_tokens': 4000
            }
        }
    
    def _load_system_prompts(self) -> Dict[str, str]:
        """Load system prompts from configuration"""
        # In production, these would be loaded from S3 or parameter store
        # For now, return basic prompts
        return {
            'intent-classification': "You are an expert intent classifier for UrbanHub's AI system.",
            'response-generation': "You are UrbanHub's conversational AI assistant.",
            'multimodal-processing': "You are UrbanHub's multimodal content analysis specialist."
        }
    
    @tracer.capture_method
    async def process_request(self, request: ClaudeRequest) -> ClaudeResponse:
        """Main method to process Claude requests"""
        
        start_time = time.time()
        
        try:
            # Get model configuration
            config = self.model_config.get(request.prompt_type, self.model_config['response-generation'])
            
            # Prepare messages for Claude
            messages = self._prepare_messages(request)
            
            # Get system prompt
            system_prompt = request.system_prompt or self.system_prompts.get(request.prompt_type, "")
            
            # Make Claude API call
            if request.include_images and request.image_data:
                response = await self._call_claude_with_images(
                    messages=messages,
                    system_prompt=system_prompt,
                    config=config,
                    image_data=request.image_data
                )
            else:
                response = await self._call_claude_text_only(
                    messages=messages,
                    system_prompt=system_prompt,
                    config=config
                )
            
            # Calculate processing time
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            # Update context if provided
            if request.context:
                await self._update_conversation_context(request.context, request.content, response.content[0].text)
            
            # Create response object
            claude_response = ClaudeResponse(
                content=response.content[0].text,
                usage={
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens,
                    'total_tokens': response.usage.input_tokens + response.usage.output_tokens
                },
                model_used=config['model'],
                processing_time_ms=processing_time_ms,
                confidence_score=self._calculate_confidence_score(response.content[0].text),
                metadata={
                    'prompt_type': request.prompt_type,
                    'context_used': request.context is not None
                }
            )
            
            # Add metrics
            metrics.add_metric("ClaudeAPICall", 1, MetricUnit.Count)
            metrics.add_metric("ClaudeLatency", processing_time_ms, MetricUnit.Milliseconds)
            metrics.add_metric("ClaudeTokensUsed", claude_response.usage['total_tokens'], MetricUnit.Count)
            
            return claude_response
            
        except Exception as e:
            logger.error(f"Claude API request failed: {str(e)}")
            metrics.add_metric("ClaudeAPIErrors", 1, MetricUnit.Count)
            raise
    
    @tracer.capture_method
    async def _call_claude_text_only(self, messages: List[Dict], system_prompt: str, config: Dict) -> Any:
        """Make text-only Claude API call"""
        
        return self.client.messages.create(
            model=config['model'],
            max_tokens=config['max_tokens'],
            temperature=config['temperature'],
            system=system_prompt,
            messages=messages
        )
    
    @tracer.capture_method
    async def _call_claude_with_images(self, messages: List[Dict], system_prompt: str, config: Dict, image_data: List[str]) -> Any:
        """Make Claude API call with image analysis"""
        
        # Add image data to the last user message
        if messages and image_data:
            last_message = messages[-1]
            if last_message.get('role') == 'user':
                # Create multimodal content
                content_parts = [{"type": "text", "text": last_message['content']}]
                
                for img_data in image_data:
                    content_parts.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": img_data
                        }
                    })
                
                last_message['content'] = content_parts
        
        return self.client.messages.create(
            model=config['model'],
            max_tokens=config['max_tokens'],
            temperature=config['temperature'],
            system=system_prompt,
            messages=messages
        )
    
    def _prepare_messages(self, request: ClaudeRequest) -> List[Dict[str, str]]:
        """Prepare messages for Claude API call"""
        
        messages = []
        
        # Add conversation context if available
        if request.context:
            context_messages = self.context_manager.optimize_context_for_claude(request.context)
            messages.extend(context_messages)
        
        # Add current message
        messages.append({
            "role": "user",
            "content": request.content
        })
        
        return messages
    
    async def _update_conversation_context(self, context: ConversationContext, user_message: str, assistant_response: str):
        """Update conversation context with new exchange"""
        
        # Add messages to context
        context.messages.extend([
            {"role": "user", "content": user_message, "timestamp": datetime.now().isoformat()},
            {"role": "assistant", "content": assistant_response, "timestamp": datetime.now().isoformat()}
        ])
        
        # Save updated context
        self.context_manager.save_conversation_context(context)
    
    def _calculate_confidence_score(self, response: str) -> float:
        """Calculate confidence score based on response characteristics"""
        
        # Simple heuristic-based confidence scoring
        score = 0.8  # Base score
        
        # Increase score for certain indicators
        if "no estoy seguro" in response.lower() or "no sé" in response.lower():
            score -= 0.3
        
        if len(response) > 100:  # Detailed responses generally more confident
            score += 0.1
            
        if "recomiendo" in response.lower() or "sugiero" in response.lower():
            score += 0.1
        
        return min(1.0, max(0.1, score))

    # Utility methods for specific prompt types
    
    @tracer.capture_method
    async def classify_intent(self, message: str, context: ConversationContext = None) -> Dict[str, Any]:
        """Classify user intent using Claude"""
        
        request = ClaudeRequest(
            prompt_type="intent-classification",
            content=message,
            context=context,
            temperature=0.1,
            max_tokens=1000
        )
        
        response = await self.process_request(request)
        
        try:
            # Parse JSON response
            classification = json.loads(response.content)
            return classification
        except json.JSONDecodeError:
            # Fallback classification
            logger.warning("Failed to parse intent classification JSON")
            return {
                "intent": "others",
                "confidence": 0.5,
                "routing_recommendation": "conversation-ai"
            }
    
    @tracer.capture_method
    async def generate_response(self, message: str, context: ConversationContext = None) -> str:
        """Generate conversational response using Claude"""
        
        request = ClaudeRequest(
            prompt_type="response-generation", 
            content=message,
            context=context,
            temperature=0.7,
            max_tokens=4000
        )
        
        response = await self.process_request(request)
        return response.content
    
    @tracer.capture_method
    async def process_multimodal_content(self, content: str, image_data: List[str] = None, context: ConversationContext = None) -> str:
        """Process multimodal content (text + images) using Claude"""
        
        request = ClaudeRequest(
            prompt_type="multimodal-processing",
            content=content,
            context=context,
            include_images=bool(image_data),
            image_data=image_data or [],
            temperature=0.2,
            max_tokens=4000
        )
        
        response = await self.process_request(request)
        return response.content

# Export main class
__all__ = ['ClaudeClient', 'ConversationContext', 'ClaudeRequest', 'ClaudeResponse']