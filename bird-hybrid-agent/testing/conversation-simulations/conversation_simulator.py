"""
Conversation Simulation Framework for Bird.com Hybrid AI Testing
Simulates realistic user conversations for comprehensive testing
"""

import json
import time
import random
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class UserPersona(Enum):
    """Different user personas for simulation"""
    YOUNG_PROFESSIONAL = "young_professional"
    FAMILY_ORIENTED = "family_oriented"
    BUDGET_CONSCIOUS = "budget_conscious"
    LUXURY_SEEKER = "luxury_seeker"
    PET_OWNER = "pet_owner"
    FRUSTRATED_CUSTOMER = "frustrated_customer"
    EXISTING_RESIDENT = "existing_resident"

@dataclass
class SimulationConfig:
    """Configuration for conversation simulation"""
    persona: UserPersona
    conversation_length: int = 10  # Number of exchanges
    response_delay_range: Tuple[int, int] = (1, 5)  # Seconds
    include_multimodal: bool = True
    test_voice_brand: bool = True
    simulate_interruptions: bool = False
    error_injection_rate: float = 0.05  # 5% chance of errors

class ConversationSimulator:
    """Simulates realistic user conversations for testing"""
    
    def __init__(self):
        self.personas = self._initialize_personas()
        self.conversation_templates = self._initialize_templates()
        self.metrics = {}
    
    def _initialize_personas(self) -> Dict[UserPersona, Dict[str, Any]]:
        """Initialize user persona characteristics"""
        return {
            UserPersona.YOUNG_PROFESSIONAL: {
                'name': 'Alex Martínez',
                'age_range': '25-30',
                'budget_range': (18000, 28000),
                'property_interests': ['Josefa', 'Matilde', 'Amalia'],
                'communication_style': 'direct',
                'tech_savvy': True,
                'time_availability': 'evenings_weekends',
                'priorities': ['location', 'amenities', 'commute'],
                'personality_traits': ['impatient', 'detail_oriented', 'decisive']
            },
            UserPersona.FAMILY_ORIENTED: {
                'name': 'Carmen y Roberto González',
                'age_range': '30-40',
                'budget_range': (22000, 35000),
                'property_interests': ['Joaquina', 'Inés', 'Amalia'],
                'communication_style': 'thorough',
                'tech_savvy': False,
                'time_availability': 'afternoons',
                'priorities': ['safety', 'schools', 'family_amenities'],
                'personality_traits': ['cautious', 'family_focused', 'price_sensitive']
            },
            UserPersona.BUDGET_CONSCIOUS: {
                'name': 'Diana López',
                'age_range': '22-28',
                'budget_range': (15000, 20000),
                'property_interests': ['Juárez', 'Natalia', 'Matilde'],
                'communication_style': 'price_focused',
                'tech_savvy': True,
                'time_availability': 'flexible',
                'priorities': ['price', 'value', 'location'],
                'personality_traits': ['negotiator', 'researcher', 'practical']
            },
            UserPersona.LUXURY_SEEKER: {
                'name': 'Eduardo Fernández',
                'age_range': '35-45',
                'budget_range': (35000, 60000),
                'property_interests': ['Inés', 'Josefa', 'Leona'],
                'communication_style': 'quality_focused',
                'tech_savvy': True,
                'time_availability': 'business_hours',
                'priorities': ['luxury', 'status', 'service'],
                'personality_traits': ['demanding', 'quality_focused', 'status_conscious']
            },
            UserPersona.PET_OWNER: {
                'name': 'Sofia Ramírez',
                'age_range': '28-35',
                'budget_range': (20000, 30000),
                'property_interests': ['Leona', 'Joaquina', 'Matilde'],
                'communication_style': 'pet_focused',
                'tech_savvy': True,
                'time_availability': 'mornings_evenings',
                'priorities': ['pet_policies', 'outdoor_space', 'community'],
                'personality_traits': ['caring', 'community_oriented', 'active']
            },
            UserPersona.FRUSTRATED_CUSTOMER: {
                'name': 'Miguel Torres',
                'age_range': '30-40',
                'budget_range': (25000, 35000),
                'property_interests': ['multiple'],
                'communication_style': 'frustrated',
                'tech_savvy': True,
                'time_availability': 'stressed',
                'priorities': ['resolution', 'honesty', 'efficiency'],
                'personality_traits': ['frustrated', 'skeptical', 'time_pressed']
            },
            UserPersona.EXISTING_RESIDENT: {
                'name': 'Ana Patricia Vega',
                'age_range': '25-35',
                'budget_range': None,  # Already resident
                'property_interests': ['current_property'],
                'communication_style': 'familiar',
                'tech_savvy': True,
                'time_availability': 'flexible',
                'priorities': ['service', 'maintenance', 'community'],
                'personality_traits': ['familiar', 'expectant', 'loyal']
            }
        }
    
    def _initialize_templates(self) -> Dict[UserPersona, List[Dict[str, Any]]]:
        """Initialize conversation templates for each persona"""
        return {
            UserPersona.YOUNG_PROFESSIONAL: [
                {
                    'stage': 'opening',
                    'messages': [
                        "Hola, busco un departamento cerca de Reforma para este mes",
                        "Buenos días, me interesa rentar y trabajo en Polanco",
                        "Hi, looking for a 1BR apartment, do you speak English?"
                    ],
                    'expected_responses': ['greeting', 'property_matching', 'language_accommodation']
                },
                {
                    'stage': 'property_inquiry',
                    'messages': [
                        "¿Qué opciones tienen en Josefa?",
                        "Necesito algo con buen internet para home office",
                        "¿Incluye servicios o se pagan aparte?"
                    ],
                    'expected_responses': ['property_details', 'amenity_info', 'pricing_info']
                },
                {
                    'stage': 'tour_booking',
                    'messages': [
                        "¿Puedo ver el departamento hoy en la tarde?",
                        "¿Tienen horarios disponibles este fin de semana?",
                        "Prefiero tours virtuales, ¿es posible?"
                    ],
                    'expected_responses': ['tour_scheduling', 'availability_check', 'virtual_tour_offer']
                }
            ],
            
            UserPersona.FAMILY_ORIENTED: [
                {
                    'stage': 'opening',
                    'messages': [
                        "Hola, somos una familia con dos niños y buscamos departamento",
                        "Buenos días, necesitamos un lugar seguro para nuestra familia",
                        "¿Tienen opciones family-friendly?"
                    ],
                    'expected_responses': ['family_greeting', 'safety_assurance', 'family_options']
                },
                {
                    'stage': 'family_concerns',
                    'messages': [
                        "¿Qué tan seguro es el área para niños?",
                        "¿Hay escuelas buenas cerca?",
                        "¿Tienen áreas de juego para niños?"
                    ],
                    'expected_responses': ['safety_info', 'school_info', 'family_amenities']
                },
                {
                    'stage': 'practical_questions',
                    'messages': [
                        "¿Permiten mascotas? Tenemos un perro pequeño",
                        "¿Hay suficiente espacio de estacionamiento?",
                        "¿Qué incluye la renta exactamente?"
                    ],
                    'expected_responses': ['pet_policy', 'parking_info', 'rental_inclusions']
                }
            ],
            
            UserPersona.PET_OWNER: [
                {
                    'stage': 'opening',
                    'messages': [
                        "Hola, tengo dos gatos y busco un lugar pet-friendly",
                        "Buenos días, ¿son realmente pet lovers como dicen?",
                        "¿Qué políticas tienen para mascotas?"
                    ],
                    'expected_responses': ['pet_welcome', 'pet_lover_confirmation', 'pet_policies']
                },
                {
                    'stage': 'pet_specifics',
                    'messages': [
                        "¿Hay límite en el número de mascotas?",
                        "¿Tienen áreas especiales para mascotas?",
                        "¿Cobran depósito adicional por las mascotas?"
                    ],
                    'expected_responses': ['pet_limits', 'pet_amenities', 'pet_fees']
                },
                {
                    'stage': 'community_focus',
                    'messages': [
                        "¿Hay otros residentes con mascotas?",
                        "¿Organizan eventos para la comunidad pet?",
                        "¿Las mascotas pueden usar todas las áreas comunes?"
                    ],
                    'expected_responses': ['pet_community', 'pet_events', 'pet_access']
                }
            ],
            
            UserPersona.FRUSTRATED_CUSTOMER: [
                {
                    'stage': 'frustrated_opening',
                    'messages': [
                        "Ya llevo días tratando de conseguir información clara",
                        "Nadie me ha podido dar precios reales, solo rangos",
                        "Estoy cansado de que me den vueltas"
                    ],
                    'expected_responses': ['empathy', 'problem_solving', 'direct_help']
                },
                {
                    'stage': 'specific_complaints',
                    'messages': [
                        "El otro agente me dijo una cosa y ahora me dicen otra",
                        "Ya visité 3 propiedades y todas tienen 'problemas técnicos'",
                        "¿En serio van a poder ayudarme o es lo mismo de siempre?"
                    ],
                    'expected_responses': ['acknowledgment', 'solution_focus', 'credibility_building']
                },
                {
                    'stage': 'resolution_seeking',
                    'messages': [
                        "Solo necesito saber: ¿tienen disponible o no?",
                        "¿Pueden garantizarme que el tour va a suceder?",
                        "¿Con quién puedo hablar que realmente resuelva?"
                    ],
                    'expected_responses': ['definitive_answers', 'assurance', 'escalation_offer']
                }
            ]
        }
    
    async def simulate_conversation(self, config: SimulationConfig) -> Dict[str, Any]:
        """Simulate a complete conversation with specified configuration"""
        
        persona_data = self.personas[config.persona]
        conversation_template = self.conversation_templates.get(config.persona, [])
        
        simulation_results = {
            'persona': config.persona.value,
            'persona_data': persona_data,
            'conversation_id': f"sim_{int(time.time())}_{random.randint(1000, 9999)}",
            'exchanges': [],
            'metrics': {
                'start_time': datetime.now().isoformat(),
                'total_exchanges': 0,
                'avg_response_time': 0,
                'voice_brand_mentions': 0,
                'escalations': 0,
                'user_satisfaction_score': 0,
                'conversation_completion': False,
                'errors_encountered': 0
            },
            'analysis': {}
        }
        
        # Simulate conversation exchanges
        for exchange_num in range(config.conversation_length):
            exchange_result = await self._simulate_exchange(
                exchange_num, 
                conversation_template,
                persona_data,
                config,
                simulation_results
            )
            
            simulation_results['exchanges'].append(exchange_result)
            
            # Update metrics
            self._update_simulation_metrics(simulation_results, exchange_result)
            
            # Add realistic delay between exchanges
            delay = random.uniform(*config.response_delay_range)
            await asyncio.sleep(delay)
        
        # Finalize simulation
        simulation_results['metrics']['end_time'] = datetime.now().isoformat()
        simulation_results['analysis'] = self._analyze_conversation(simulation_results)
        
        return simulation_results
    
    async def _simulate_exchange(self, exchange_num: int, template: List[Dict], 
                                persona_data: Dict, config: SimulationConfig, 
                                simulation_data: Dict) -> Dict[str, Any]:
        """Simulate a single conversation exchange"""
        
        # Determine conversation stage
        stage_index = min(exchange_num // 2, len(template) - 1)
        current_stage = template[stage_index] if template else {'stage': 'general', 'messages': ['Continue conversation']}
        
        # Generate user message
        user_message = await self._generate_user_message(
            current_stage, persona_data, exchange_num, config
        )
        
        # Simulate AI response processing time
        processing_start = time.time()
        
        # Generate expected AI response
        ai_response = await self._generate_ai_response(
            user_message, persona_data, current_stage, simulation_data
        )
        
        processing_time = (time.time() - processing_start) * 1000
        
        # Inject errors if configured
        error_occurred = False
        if random.random() < config.error_injection_rate:
            error_occurred = True
            ai_response = await self._inject_error(ai_response)
        
        exchange = {
            'exchange_number': exchange_num + 1,
            'stage': current_stage['stage'],
            'user_message': user_message,
            'ai_response': ai_response,
            'processing_time_ms': processing_time,
            'error_occurred': error_occurred,
            'timestamp': datetime.now().isoformat(),
            'analysis': {
                'intent_detected': self._detect_intent(user_message),
                'voice_brand_used': self._check_voice_brand_usage(ai_response),
                'escalation_triggered': self._check_escalation(ai_response),
                'user_sentiment': self._analyze_sentiment(user_message),
                'response_quality_score': self._score_response_quality(ai_response, user_message)
            }
        }
        
        return exchange
    
    async def _generate_user_message(self, stage: Dict, persona_data: Dict, 
                                   exchange_num: int, config: SimulationConfig) -> Dict[str, Any]:
        """Generate realistic user message based on persona and stage"""
        
        # Select message from template or generate dynamic one
        if 'messages' in stage and stage['messages']:
            base_message = random.choice(stage['messages'])
        else:
            base_message = self._generate_dynamic_message(persona_data, exchange_num)
        
        # Add persona-specific variations
        message_variations = {
            UserPersona.YOUNG_PROFESSIONAL: self._add_professional_variations,
            UserPersona.FAMILY_ORIENTED: self._add_family_variations,
            UserPersona.BUDGET_CONSCIOUS: self._add_budget_variations,
            UserPersona.LUXURY_SEEKER: self._add_luxury_variations,
            UserPersona.PET_OWNER: self._add_pet_variations,
            UserPersona.FRUSTRATED_CUSTOMER: self._add_frustrated_variations,
            UserPersona.EXISTING_RESIDENT: self._add_resident_variations
        }
        
        persona_key = UserPersona(persona_data.get('persona_type', UserPersona.YOUNG_PROFESSIONAL))
        if persona_key in message_variations:
            base_message = message_variations[persona_key](base_message, exchange_num)
        
        # Include multimodal content if configured
        multimodal_content = None
        if config.include_multimodal and random.random() < 0.3:  # 30% chance
            multimodal_content = self._generate_multimodal_content(stage['stage'])
        
        return {
            'text': base_message,
            'type': 'text',
            'multimodal': multimodal_content,
            'timestamp': datetime.now().isoformat()
        }
    
    async def _generate_ai_response(self, user_message: Dict, persona_data: Dict, 
                                  stage: Dict, simulation_data: Dict) -> str:
        """Generate realistic AI response based on context"""
        
        # This would integrate with actual AI system in real implementation
        # For simulation, generate contextually appropriate responses
        
        base_responses = {
            'opening': [
                "¡Hola {name}! Bienvenido a UrbanHub. Me da mucho gusto poder ayudarte a encontrar tu nuevo hogar.",
                "¡Perfecto! Veo que buscas {property_type}. Te voy a mostrar las mejores opciones que tenemos.",
                "¡Qué padre que te interese UrbanHub! Tenemos varias propiedades que podrían ser perfectas para ti."
            ],
            'property_inquiry': [
                "{property} es una excelente opción en {location}. Con precios desde ${price}, tu dinero realmente rinde más aquí.",
                "Te va a encantar {property}. Lo que más me gusta es {feature}. ¿Te gustaría que te cuente más sobre las amenidades?",
                "Basado en lo que me platicas, creo que {property} sería perfecta para ti porque {reason}."
            ],
            'tour_booking': [
                "¡Por supuesto! Tengo disponibilidad {availability}. ¿Te funciona {proposed_time}?",
                "Perfecto, vamos a agendar tu tour. Te va a encantar conocer {property} en persona.",
                "¡Excelente! Te voy a conectar con {agent_name} quien se especializa en tours de {property}."
            ]
        }
        
        stage_key = stage.get('stage', 'opening')
        if stage_key in base_responses:
            response_template = random.choice(base_responses[stage_key])
        else:
            response_template = "Perfecto, entiendo tu consulta. Déjame ayudarte con eso."
        
        # Add voice brand messaging contextually
        if random.random() < 0.4:  # 40% chance of voice brand usage
            voice_brand_messages = [
                "Tu dinero rinde más aquí en UrbanHub.",
                "When you live in here, you thrive out there.",
                "Somos pet lovers, no solo pet friendly.",
                "Es más que cuatro paredes, es tu nuevo estilo de vida."
            ]
            
            # Select appropriate voice brand message based on context
            context_keywords = user_message['text'].lower()
            if 'precio' in context_keywords or 'costo' in context_keywords:
                response_template += " " + voice_brand_messages[0]
            elif 'mascota' in context_keywords or 'perro' in context_keywords:
                response_template += " " + voice_brand_messages[2]
            else:
                response_template += " " + random.choice(voice_brand_messages)
        
        # Personalize response based on persona
        response = self._personalize_response(response_template, persona_data, user_message)
        
        return response
    
    def _personalize_response(self, template: str, persona_data: Dict, user_message: Dict) -> str:
        """Personalize response based on user persona"""
        
        personalizations = {
            '{name}': persona_data.get('name', 'amigo'),
            '{property}': random.choice(persona_data.get('property_interests', ['una propiedad'])),
            '{location}': 'CDMX',
            '{price}': f"{random.randint(*persona_data.get('budget_range', (20000, 30000))):,}",
            '{property_type}': 'departamento',
            '{feature}': random.choice(['la ubicación', 'las amenidades', 'el diseño']),
            '{reason}': 'tiene todo lo que buscas',
            '{availability}': 'mañana por la tarde',
            '{proposed_time}': '4:00 PM',
            '{agent_name}': 'Vivi'
        }
        
        response = template
        for placeholder, value in personalizations.items():
            response = response.replace(placeholder, value)
        
        return response
    
    def _update_simulation_metrics(self, simulation_results: Dict, exchange: Dict):
        """Update simulation metrics based on exchange results"""
        
        metrics = simulation_results['metrics']
        analysis = exchange['analysis']
        
        metrics['total_exchanges'] += 1
        
        # Update response time average
        current_avg = metrics['avg_response_time']
        new_time = exchange['processing_time_ms']
        metrics['avg_response_time'] = (current_avg * (metrics['total_exchanges'] - 1) + new_time) / metrics['total_exchanges']
        
        # Count voice brand mentions
        if analysis['voice_brand_used']:
            metrics['voice_brand_mentions'] += 1
        
        # Count escalations
        if analysis['escalation_triggered']:
            metrics['escalations'] += 1
        
        # Count errors
        if exchange['error_occurred']:
            metrics['errors_encountered'] += 1
        
        # Update satisfaction score (simplified)
        if analysis['response_quality_score'] > 7:
            metrics['user_satisfaction_score'] += 1
    
    def _analyze_conversation(self, simulation_results: Dict) -> Dict[str, Any]:
        """Analyze complete conversation simulation"""
        
        metrics = simulation_results['metrics']
        exchanges = simulation_results['exchanges']
        
        analysis = {
            'conversation_flow': self._analyze_flow(exchanges),
            'intent_accuracy': self._calculate_intent_accuracy(exchanges),
            'response_quality': {
                'avg_score': sum(e['analysis']['response_quality_score'] for e in exchanges) / len(exchanges),
                'consistency': self._check_response_consistency(exchanges),
                'voice_brand_integration': metrics['voice_brand_mentions'] / metrics['total_exchanges']
            },
            'performance': {
                'avg_response_time': metrics['avg_response_time'],
                'error_rate': metrics['errors_encountered'] / metrics['total_exchanges'],
                'escalation_rate': metrics['escalations'] / metrics['total_exchanges']
            },
            'user_experience': {
                'satisfaction_estimate': min(10, metrics['user_satisfaction_score'] * 2),
                'conversation_completion': metrics['total_exchanges'] >= 5,
                'goal_achievement': self._assess_goal_achievement(simulation_results)
            },
            'recommendations': self._generate_recommendations(simulation_results)
        }
        
        return analysis
    
    def _detect_intent(self, message: str) -> str:
        """Simple intent detection for simulation"""
        text = message.lower()
        
        if any(word in text for word in ['precio', 'costo', 'cuanto']):
            return 'pricing_inquiry'
        elif any(word in text for word in ['tour', 'ver', 'visita']):
            return 'tour_request'
        elif any(word in text for word in ['problema', 'fuga', 'no funciona']):
            return 'maintenance_request'
        elif any(word in text for word in ['mascota', 'perro', 'gato', 'pet']):
            return 'pet_inquiry'
        else:
            return 'general_inquiry'
    
    def _check_voice_brand_usage(self, response: str) -> bool:
        """Check if voice brand messaging is used in response"""
        voice_brand_phrases = [
            'tu dinero rinde más',
            'when you live in here, you thrive out there',
            'pet lovers',
            'más que cuatro paredes'
        ]
        
        return any(phrase in response.lower() for phrase in voice_brand_phrases)
    
    def _check_escalation(self, response: str) -> bool:
        """Check if response includes escalation"""
        escalation_phrases = [
            'te voy a conectar',
            'nuestro especialista',
            'mi supervisor',
            'equipo técnico'
        ]
        
        return any(phrase in response.lower() for phrase in escalation_phrases)
    
    def _analyze_sentiment(self, message: str) -> str:
        """Simple sentiment analysis for simulation"""
        text = message.lower()
        
        negative_words = ['problema', 'malo', 'frustra', 'cansado', 'molesto']
        positive_words = ['gracias', 'perfecto', 'excelente', 'me gusta', 'bueno']
        
        negative_count = sum(1 for word in negative_words if word in text)
        positive_count = sum(1 for word in positive_words if word in text)
        
        if negative_count > positive_count:
            return 'negative'
        elif positive_count > negative_count:
            return 'positive'
        else:
            return 'neutral'
    
    def _score_response_quality(self, response: str, user_message: Dict) -> float:
        """Score response quality on scale of 1-10"""
        score = 5.0  # Base score
        
        # Length appropriateness
        if 50 <= len(response) <= 300:
            score += 1.0
        
        # Personalization
        if any(name in response.lower() for name in ['amigo', 'perfecto', 'excelente']):
            score += 1.0
        
        # Contextual relevance (simplified)
        user_text = user_message.get('text', '').lower()
        if any(word in response.lower() for word in user_text.split()[:3]):
            score += 1.0
        
        # Voice brand integration
        if self._check_voice_brand_usage(response):
            score += 1.0
        
        # Call to action
        if any(phrase in response.lower() for phrase in ['¿te gustaría', '¿qué opinas', '¿prefieres']):
            score += 1.0
        
        return min(10.0, score)
    
    # Helper methods for generating persona-specific variations
    def _add_professional_variations(self, message: str, exchange_num: int) -> str:
        if exchange_num < 3:
            return message.replace('Hola', 'Buenos días').replace('busco', 'necesito')
        return message
    
    def _add_family_variations(self, message: str, exchange_num: int) -> str:
        family_additions = [' para mi familia', ' que sea seguro para los niños', ' con espacios familiares']
        if random.random() < 0.4:
            return message + random.choice(family_additions)
        return message
    
    def _add_budget_variations(self, message: str, exchange_num: int) -> str:
        budget_phrases = ['¿Cuál es el precio más bajo?', '¿Hay descuentos?', '¿Incluye todo?']
        if exchange_num > 2 and random.random() < 0.5:
            return message + ' ' + random.choice(budget_phrases)
        return message
    
    def _add_luxury_variations(self, message: str, exchange_num: int) -> str:
        luxury_additions = [' de alta gama', ' premium', ' exclusivo']
        return message + random.choice(luxury_additions) if random.random() < 0.3 else message
    
    def _add_pet_variations(self, message: str, exchange_num: int) -> str:
        pet_mentions = ['Tengo dos gatos', 'Mi perro es grande', '¿Son realmente pet lovers?']
        if random.random() < 0.6:
            return message + '. ' + random.choice(pet_mentions)
        return message
    
    def _add_frustrated_variations(self, message: str, exchange_num: int) -> str:
        frustration_level = min(exchange_num, 5)
        frustrated_prefixes = ['Ya intenté antes...', 'Espero que ahora sí...', 'La última vez...']
        
        if frustration_level > 2:
            return random.choice(frustrated_prefixes) + ' ' + message
        return message
    
    def _add_resident_variations(self, message: str, exchange_num: int) -> str:
        resident_context = ['Como residente de UrbanHub', 'Vivo en Josefa', 'Soy inquilino actual']
        if exchange_num == 0:
            return random.choice(resident_context) + ', ' + message.lower()
        return message
    
    # Additional utility methods
    def _generate_dynamic_message(self, persona_data: Dict, exchange_num: int) -> str:
        """Generate dynamic message when no template available"""
        dynamic_messages = [
            "¿Podrías darme más información?",
            "No estoy seguro de entender, ¿puedes explicarme?",
            "¿Qué otras opciones tienes disponibles?",
            "Me interesa saber más detalles.",
            "¿Cuáles son los siguientes pasos?"
        ]
        return random.choice(dynamic_messages)
    
    def _generate_multimodal_content(self, stage: str) -> Dict[str, Any]:
        """Generate multimodal content for testing"""
        multimodal_types = {
            'opening': None,  # Usually just text
            'property_inquiry': {
                'type': 'image',
                'description': 'Screenshot of another property listing',
                'purpose': 'comparison'
            },
            'tour_booking': {
                'type': 'voice',
                'description': 'Voice message explaining schedule constraints',
                'duration_seconds': 15
            }
        }
        
        return multimodal_types.get(stage)
    
    async def _inject_error(self, response: str) -> str:
        """Inject realistic errors for testing"""
        error_types = [
            'timeout',
            'incomplete_response',
            'wrong_language',
            'formatting_error'
        ]
        
        error = random.choice(error_types)
        
        if error == 'timeout':
            return "[ERROR: Response timeout]"
        elif error == 'incomplete_response':
            return response[:len(response)//2] + "..."
        elif error == 'wrong_language':
            return "I apologize, but I can help you in English..."
        else:  # formatting_error
            return response.replace(' ', '').replace('.', ',')
    
    def _analyze_flow(self, exchanges: List[Dict]) -> Dict[str, Any]:
        """Analyze conversation flow quality"""
        stages = [e['stage'] for e in exchanges]
        stage_transitions = list(zip(stages[:-1], stages[1:]))
        
        return {
            'stages_covered': len(set(stages)),
            'natural_progression': len(stage_transitions) > 0,
            'stage_repetitions': len(stages) - len(set(stages)),
            'flow_smoothness_score': min(10, len(set(stages)) * 2)
        }
    
    def _calculate_intent_accuracy(self, exchanges: List[Dict]) -> float:
        """Calculate intent detection accuracy (simplified)"""
        correct_intents = sum(1 for e in exchanges if e['analysis']['intent_detected'] != 'unknown')
        return correct_intents / len(exchanges) if exchanges else 0.0
    
    def _check_response_consistency(self, exchanges: List[Dict]) -> float:
        """Check response consistency across conversation"""
        # Simplified: check if voice brand usage is consistent
        voice_brand_uses = [e['analysis']['voice_brand_used'] for e in exchanges]
        return sum(voice_brand_uses) / len(voice_brand_uses) if voice_brand_uses else 0.0
    
    def _assess_goal_achievement(self, simulation_results: Dict) -> bool:
        """Assess if user's goal was likely achieved"""
        persona = simulation_results['persona']
        exchanges = simulation_results['exchanges']
        
        # Simplified goal assessment
        final_stages = [e['stage'] for e in exchanges[-3:]]
        
        goal_indicators = {
            'young_professional': ['tour_booking', 'application'],
            'family_oriented': ['safety_confirmation', 'tour_booking'],
            'pet_owner': ['pet_confirmation', 'tour_booking'],
            'frustrated_customer': ['resolution', 'satisfaction']
        }
        
        expected_indicators = goal_indicators.get(persona, ['general_satisfaction'])
        return any(indicator in ' '.join(final_stages) for indicator in expected_indicators)
    
    def _generate_recommendations(self, simulation_results: Dict) -> List[str]:
        """Generate recommendations based on simulation results"""
        recommendations = []
        analysis = simulation_results['analysis']
        
        if analysis['performance']['avg_response_time'] > 2000:
            recommendations.append("Optimize response time - currently averaging over 2 seconds")
        
        if analysis['response_quality']['voice_brand_integration'] < 0.3:
            recommendations.append("Increase voice brand integration - currently below 30%")
        
        if analysis['performance']['error_rate'] > 0.05:
            recommendations.append("Address error handling - error rate above 5%")
        
        if analysis['user_experience']['satisfaction_estimate'] < 7:
            recommendations.append("Improve user experience - satisfaction below target")
        
        return recommendations


# Batch simulation runner
class BatchSimulationRunner:
    """Run multiple conversation simulations for comprehensive testing"""
    
    def __init__(self):
        self.simulator = ConversationSimulator()
    
    async def run_persona_analysis(self, iterations_per_persona: int = 5) -> Dict[str, Any]:
        """Run simulations for all personas and analyze results"""
        
        results = {
            'summary': {},
            'detailed_results': [],
            'comparative_analysis': {},
            'recommendations': []
        }
        
        for persona in UserPersona:
            persona_results = []
            
            for i in range(iterations_per_persona):
                config = SimulationConfig(
                    persona=persona,
                    conversation_length=8,
                    include_multimodal=True,
                    test_voice_brand=True
                )
                
                simulation_result = await self.simulator.simulate_conversation(config)
                persona_results.append(simulation_result)
            
            # Aggregate persona results
            results['detailed_results'].extend(persona_results)
            results['summary'][persona.value] = self._aggregate_persona_results(persona_results)
        
        # Generate comparative analysis
        results['comparative_analysis'] = self._compare_personas(results['summary'])
        results['recommendations'] = self._generate_overall_recommendations(results)
        
        return results
    
    def _aggregate_persona_results(self, persona_results: List[Dict]) -> Dict[str, Any]:
        """Aggregate results for a single persona"""
        if not persona_results:
            return {}
        
        total_conversations = len(persona_results)
        
        aggregated = {
            'total_conversations': total_conversations,
            'avg_response_time': sum(r['metrics']['avg_response_time'] for r in persona_results) / total_conversations,
            'avg_satisfaction': sum(r['analysis']['user_experience']['satisfaction_estimate'] for r in persona_results) / total_conversations,
            'voice_brand_usage_rate': sum(r['analysis']['response_quality']['voice_brand_integration'] for r in persona_results) / total_conversations,
            'error_rate': sum(r['analysis']['performance']['error_rate'] for r in persona_results) / total_conversations,
            'escalation_rate': sum(r['analysis']['performance']['escalation_rate'] for r in persona_results) / total_conversations,
            'goal_achievement_rate': sum(1 for r in persona_results if r['analysis']['user_experience']['goal_achievement']) / total_conversations
        }
        
        return aggregated
    
    def _compare_personas(self, summary: Dict) -> Dict[str, Any]:
        """Compare performance across different personas"""
        
        if not summary:
            return {}
        
        metrics = ['avg_response_time', 'avg_satisfaction', 'voice_brand_usage_rate', 
                  'error_rate', 'escalation_rate', 'goal_achievement_rate']
        
        comparison = {}
        
        for metric in metrics:
            values = [data[metric] for data in summary.values() if metric in data]
            
            if values:
                comparison[metric] = {
                    'best_persona': min(summary.items(), key=lambda x: x[1].get(metric, 0) if 'rate' in metric and metric != 'goal_achievement_rate' else -x[1].get(metric, 0))[0],
                    'worst_persona': max(summary.items(), key=lambda x: x[1].get(metric, 0) if 'rate' in metric and metric != 'goal_achievement_rate' else -x[1].get(metric, 0))[0],
                    'average': sum(values) / len(values),
                    'range': max(values) - min(values)
                }
        
        return comparison
    
    def _generate_overall_recommendations(self, results: Dict) -> List[str]:
        """Generate system-wide recommendations based on all simulations"""
        recommendations = []
        
        comparison = results['comparative_analysis']
        
        # Response time recommendations
        if comparison.get('avg_response_time', {}).get('average', 0) > 2000:
            recommendations.append("CRITICAL: System-wide response time above 2 seconds - optimize processing pipeline")
        
        # Satisfaction recommendations  
        if comparison.get('avg_satisfaction', {}).get('average', 0) < 7:
            recommendations.append("Improve overall user satisfaction - currently below 7/10 target")
        
        # Voice brand recommendations
        if comparison.get('voice_brand_usage_rate', {}).get('average', 0) < 0.4:
            recommendations.append("Increase voice brand integration across all personas - currently below 40%")
        
        # Error handling recommendations
        if comparison.get('error_rate', {}).get('average', 0) > 0.05:
            recommendations.append("Address system error handling - error rate above 5% threshold")
        
        # Persona-specific recommendations
        worst_satisfaction_persona = comparison.get('avg_satisfaction', {}).get('worst_persona')
        if worst_satisfaction_persona:
            recommendations.append(f"Focus on improving experience for {worst_satisfaction_persona} persona")
        
        return recommendations


if __name__ == "__main__":
    # Example usage
    async def main():
        simulator = ConversationSimulator()
        
        config = SimulationConfig(
            persona=UserPersona.YOUNG_PROFESSIONAL,
            conversation_length=6,
            include_multimodal=True,
            test_voice_brand=True
        )
        
        result = await simulator.simulate_conversation(config)
        print(json.dumps(result, indent=2, default=str))
    
    asyncio.run(main())