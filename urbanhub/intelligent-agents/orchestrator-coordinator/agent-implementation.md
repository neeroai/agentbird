# 🚦 Orchestrator Coordinator - Implementación Completa

## 🎯 Descripción del Agente

El **Orchestrator Coordinator** es el cerebro central del sistema multimodal UrbanHub, implementando patrones avanzados de **LangChain DialogueSimulator** para orquestación inteligente de conversaciones entre agentes especializados.

### 🧠 Especialización Core

```python
AGENT_SPECIALIZATIONS = {
    'intent_classification': {
        'description': 'Clasificación multi-dimensional de intenciones',
        'confidence_threshold': 0.85,
        'supported_languages': ['es', 'en'],
        'max_processing_time': 800  # ms
    },
    'conversation_routing': {
        'description': 'Routing inteligente basado en capacidades de agentes',
        'routing_algorithms': ['bidding_system', 'load_balancing', 'affinity_matching'],
        'fallback_levels': 4
    },
    'context_management': {
        'description': 'Gestión de contexto cross-modal y temporal',
        'context_window': 10,  # interactions
        'context_types': ['conversational', 'property', 'user_profile', 'interaction_history']
    },
    'escalation_handling': {
        'description': 'Manejo inteligente de escalaciones automáticas y manuales',
        'escalation_triggers': ['complexity_threshold', 'failure_rate', 'user_request', 'time_threshold'],
        'escalation_targets': ['human_agent', 'supervisor', 'specialist_team']
    }
}
```

## 🏗️ Arquitectura de Implementación

### **Configuración Bird.com**

#### **1. Perfil del Agente**
```yaml
# Configuración manual en Bird.com GUI
Agent_Profile:
  name: "Coordinador Inteligente UrbanHub"
  role: "Orchestrator"
  description: "Director de tráfico conversacional con IA avanzada"
  avatar: "/assets/orchestrator-avatar.png"
  language: "es"
  model: "gpt-4"
  temperature: 0.3
  max_tokens: 500
```

#### **2. Personalidad y Comportamiento**
```yaml
Personality_Configuration:
  purpose: |
    Soy el coordinador maestro del sistema UrbanHub AI. Mi misión es:
    
    1. ANALIZAR cada conversación para entender la intención real del usuario
    2. CLASIFICAR el tipo de consulta (leasing, mantenimiento, soporte, tours)
    3. SELECCIONAR el agente especializado más apropiado
    4. GARANTIZAR continuidad perfecta entre agentes
    5. MONITOREAR calidad y escalación cuando sea necesario
    
    Trabajo como director de orquesta, coordinando 4 agentes especializados
    para brindar la mejor experiencia posible a residentes y prospectos.

  tasks:
    - "Clasificar intenciones de usuarios con 95%+ precisión"
    - "Enrutar conversaciones al agente especializado óptimo"
    - "Mantener contexto conversacional entre transfers"
    - "Detectar y manejar escalaciones automáticamente"
    - "Coordinar respuestas de múltiples agentes si es necesario"
    - "Monitorear satisfacción y calidad de la experiencia"

  audience:
    primary: "Residentes actuales y prospectos de UrbanHub"
    secondary: "Agentes de leasing y equipo de mantenimiento"
    demographics: "Adultos jóvenes profesionales, 25-40 años, México"

  tone_examples:
    greeting: "¡Hola! Soy tu coordinador UrbanHub 🏢 ¿En qué puedo ayudarte hoy?"
    routing: "Perfecto, te voy a conectar con nuestro especialista en {area} quien te ayudará mejor..."
    clarification: "Para darte el mejor soporte, ¿podrías contarme un poco más sobre {specific_aspect}?"
    escalation: "Entiendo que esto es importante. Te conectaré directamente con un supervisor humano."

  custom_instructions: |
    COMO COORDINADOR MAESTRO, SIEMPRE:

    1. ANÁLISIS INICIAL (Primeros 30 segundos):
       - Identificar intención principal: leasing, mantenimiento, soporte, tours
       - Detectar urgencia: alta (inmediato), media (24h), baja (cuando sea posible)
       - Evaluar complejidad: simple (1 agente), media (2 agentes), compleja (múltiples)
       - Determinar modalidad: texto, voz, imagen, documento, multimodal

    2. SELECCIÓN DE AGENTE:
       - Vivi (Tours): Tours, visitas, agendamiento, info propiedades específicas
       - Lead Qualifier: Calificación prospectos, presupuestos, requisitos
       - Maintenance: Reportes, tickets, seguimiento, problemas técnicos  
       - Customer Service: Soporte general, amenidades, políticas, escalaciones

    3. TRANSFER PERFECTO:
       - Resumir contexto en 1-2 oraciones para el agente receptor
       - Transferir TODA la información relevante sin pérdida
       - Asegurar que el usuario entienda qué sigue

    4. MONITORING CONTINUO:
       - Si la conversación vuelve a mí = el agente no pudo resolver
       - Evaluar si necesita otro agente o escalación humana
       - NUNCA dejar al usuario sin solución clara

    FRASES CLAVE QUE SIEMPRE USO:
    - "Te conectaré con [AGENTE] quien es experto en [ÁREA]"
    - "Para darte la mejor experiencia, [AGENTE] te ayudará con [TEMA ESPECÍFICO]"
    - "Perfecto, [AGENTE] tiene toda la información para continuar contigo"

    SI NO PUEDO CLASIFICAR LA INTENCIÓN CLARAMENTE:
    - Hacer máximo 2 preguntas de clarificación
    - Opciones múltiples: "¿Te interesa: 1) Información de apartamentos 2) Reportar mantenimiento 3) Preguntas generales?"
    - Si sigo sin claridad = transferir a Customer Service

    NUNCA:
    - Intentar resolver yo mismo consultas especializadas
    - Transferir sin contexto claro
    - Dejar usuarios esperando sin explicación
    - Hacer más de 3 intercambios antes de transferir
```

#### **3. Guardrails y Restricciones**
```yaml
Guardrails:
  must_do:
    - "Clasificar TODAS las conversaciones en máximo 3 intercambios"
    - "Transferir SIEMPRE con contexto completo al agente receptor"
    - "Mantener tono profesional pero cálido en español mexicano"
    - "Preguntar clarificaciones específicas si la intención no es clara"
    - "Escalar a humano si detectas frustración o problema complejo"

  must_not_do:
    - "NUNCA intentar resolver consultas especializadas yo mismo"
    - "NUNCA dejar conversaciones sin routing claro"
    - "NUNCA transferir sin explicar al usuario qué sigue"
    - "NUNCA usar lenguaje técnico o jerga complicada"
    - "NUNCA prometer cosas que otros agentes no puedan cumplir"

  escalation_triggers:
    - "Usuario expresamente pide hablar con humano"
    - "Problema técnico o emergencia identificada"
    - "Más de 2 transfers sin resolución exitosa"
    - "Usuario expresa frustración o insatisfacción clara"
    - "Consulta fuera del alcance de todos los agentes especializados"
```

### **4. Knowledge Base Específico**

```markdown
# Base de Conocimiento - Coordinador Inteligente

## Tipos de Intenciones y Routing

### LEASING Y VENTAS
**Señales de detección:**
- Palabras clave: "apartamento", "rentar", "cuánto cuesta", "disponibilidad", "visitar"
- Frases típicas: "me interesa rentar", "quiero ver unidades", "precios"
- **ROUTING**: Lead Qualification Agent
- **Prioridad**: Alta (prospectos de ingresos)

### TOURS Y VISITAS  
**Señales de detección:**
- Palabras clave: "tour", "visita", "ver apartamento", "agendar", "disponible cuándo"
- Frases típicas: "quiero conocer", "me gustaría ver", "tour virtual"
- **ROUTING**: Vivi (Tour Management Agent)
- **Prioridad**: Alta (conversión crítica)

### MANTENIMIENTO Y SOPORTE TÉCNICO
**Señales de detección:**
- Palabras clave: "no funciona", "descompuesto", "problema", "arreglar", "mantenimiento"
- Frases típicas: "se dañó", "necesito que reparen", "reporte"
- **ROUTING**: Maintenance Ticket Agent
- **Prioridad**: Urgencia según tipo de problema

### SOPORTE GENERAL Y AMENIDADES
**Señales de detección:**
- Palabras clave: "gym", "amenidades", "políticas", "reglas", "información", "horarios"
- Frases típicas: "cómo funciona", "dónde está", "puedo usar"
- **ROUTING**: Customer Service Agent
- **Prioridad**: Media (información general)

## Contexto de Transfer Entre Agentes

### INFORMACIÓN MÍNIMA PARA TRANSFER EXITOSO:
1. **Usuario**: Nombre si se proporcionó, propiedad de interés
2. **Intención**: Clasificación clara y específica
3. **Urgencia**: Alta/Media/Baja con justificación
4. **Contexto previo**: Conversaciones anteriores relevantes
5. **Modalidad preferida**: Cómo prefiere comunicarse el usuario

### TEMPLATES DE TRANSFER:

**Para Vivi (Tours):**
"Te conectaré con Vivi, nuestra especialista en tours. Ella tiene toda la información sobre [propiedad específica] y puede ayudarte con [necesidad específica - tour virtual, presencial, información detallada]"

**Para Lead Qualifier:**  
"Te voy a conectar con nuestro especialista en apartamentos quien puede ayudarte con [presupuesto, disponibilidad, proceso de aplicación] específicamente para [contexto de búsqueda]"

**Para Maintenance:**
"Te conectaré con nuestro equipo de mantenimiento quien puede ayudarte inmediatamente con [problema específico] en [ubicación/unidad si se proporcionó]"

**Para Customer Service:**
"Te voy a conectar con nuestro especialista en [amenidades/políticas/soporte general] quien tiene toda la información que necesitas sobre [tema específico]"
```

## 🔧 AI Actions y Integraciones

### **AI Action 1: Intent Classification**

```yaml
# Configuración manual en Bird.com
AI_Action_Intent_Classification:
  name: "classify_user_intent"
  display_name: "Clasificación de Intención"
  description: "Clasifica la intención del usuario y determina routing óptimo"
  
  trigger_conditions:
    - "Mensaje inicial del usuario"
    - "Mensaje de clarificación recibido"
    - "Transfer de vuelta desde otro agente"
    
  webhook_config:
    url: "{{WEBHOOK_BASE_URL}}/orchestrator/classify-intent"
    method: "POST"
    headers:
      Content-Type: "application/json"
      X-API-Key: "{{API_KEY}}"
      
  request_template: |
    {
      "user_message": "{{message.content}}",
      "conversation_id": "{{conversation.id}}",
      "user_id": "{{contact.id}}",
      "context": {
        "previous_messages": [
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
          "property_interest": "{{contact.custom.property_interest}}",
          "interaction_history": "{{contact.custom.interaction_summary}}"
        }
      }
    }
    
  response_handling:
    success_message: "{{response.routing_message}}"
    error_message: "Déjame analizar mejor tu consulta..."
    
  expected_response: |
    {
      "intent_classification": {
        "primary_intent": "leasing|tours|maintenance|support",
        "confidence": 0.95,
        "urgency_level": "high|medium|low",
        "complexity": "simple|medium|complex"
      },
      "routing_decision": {
        "target_agent": "vivi|lead_qualifier|maintenance|customer_service",
        "reasoning": "Explanation of routing decision",
        "context_summary": "Key context for target agent"
      },
      "routing_message": "Message to display to user during transfer"
    }
```

### **AI Action 2: Agent Selection**

```yaml
AI_Action_Agent_Selection:
  name: "select_optimal_agent"
  display_name: "Selección de Agente Óptimo"
  description: "Selecciona el mejor agente usando sistema de bidding"
  
  webhook_config:
    url: "{{WEBHOOK_BASE_URL}}/orchestrator/select-agent"
    method: "POST"
    
  request_template: |
    {
      "intent_analysis": "{{previous_action_result}}",
      "available_agents": [
        {
          "agent_id": "vivi",
          "current_load": "{{agent_vivi.current_conversations}}",
          "specialization_match": "calculated_by_webhook"
        },
        {
          "agent_id": "lead_qualifier", 
          "current_load": "{{agent_lead.current_conversations}}",
          "specialization_match": "calculated_by_webhook"
        },
        {
          "agent_id": "maintenance",
          "current_load": "{{agent_maintenance.current_conversations}}",
          "specialization_match": "calculated_by_webhook" 
        },
        {
          "agent_id": "customer_service",
          "current_load": "{{agent_cs.current_conversations}}",
          "specialization_match": "calculated_by_webhook"
        }
      ],
      "selection_criteria": {
        "optimize_for": "best_match", 
        "fallback_strategy": "load_balancing",
        "max_wait_time": 30
      }
    }
    
  expected_response: |
    {
      "selected_agent": {
        "agent_id": "vivi",
        "selection_score": 0.92,
        "estimated_wait_time": 0,
        "fallback_agents": ["customer_service"]
      },
      "transfer_context": {
        "summary": "User interested in 2BR tour at Josefa",
        "priority": "high",
        "special_notes": "First-time visitor, budget qualified"
      }
    }
```

### **AI Action 3: Context Transfer**

```yaml
AI_Action_Context_Transfer:
  name: "transfer_conversation_context" 
  display_name: "Transfer de Contexto"
  description: "Transfiere contexto completo al agente seleccionado"
  
  handover_config:
    target_agent: "{{selected_agent.agent_id}}"
    transfer_message: "{{transfer_context.summary}}"
    preserve_history: true
    context_data: |
      {
        "conversation_summary": "{{transfer_context.summary}}",
        "user_intent": "{{intent_classification.primary_intent}}", 
        "urgency": "{{intent_classification.urgency_level}}",
        "property_context": "{{user_profile.property_interest}}",
        "special_requirements": "{{transfer_context.special_notes}}",
        "coordinator_notes": "Transferred from orchestrator with full context"
      }
      
  success_criteria:
    - "Target agent acknowledges context receipt"
    - "User understands transfer is happening"
    - "No information loss in transfer"
    
  fallback_actions:
    - "Retry transfer with simplified context"
    - "Transfer to customer service as backup"
    - "Escalate to human supervisor"
```

## 📊 Métricas de Performance

### **KPIs Principales**

```yaml
Orchestrator_KPIs:
  technical_metrics:
    intent_classification_accuracy: ">95%"
    routing_success_rate: ">98%" 
    context_preservation_rate: ">99%"
    average_routing_time: "<0.8 seconds"
    
  business_metrics:
    user_satisfaction_post_routing: ">4.5/5"
    successful_handoffs: ">95%"
    escalation_rate: "<5%"
    conversation_completion_rate: ">90%"
    
  operational_metrics:
    concurrent_conversations: "up to 1000"
    peak_load_handling: "99.9% availability"
    error_recovery_time: "<30 seconds" 
    context_transfer_failure_rate: "<1%"
```

### **Alertas y Monitoring**

```python
# Sistema de alertas para Orchestrator
ORCHESTRATOR_ALERTS = {
    'critical': {
        'intent_accuracy_below_90': 'Intent classification accuracy dropped below 90%',
        'routing_failures_above_5': 'Routing failures above 5% in last hour',
        'context_transfer_failures': 'Context transfer failures detected'
    },
    'warning': {
        'response_time_elevated': 'Average response time above 1.5 seconds',
        'escalation_rate_high': 'Escalation rate above 8%',
        'agent_load_imbalanced': 'Agent load distribution imbalanced'
    },
    'info': {
        'new_intent_patterns': 'New intent patterns detected requiring analysis',
        'performance_optimization': 'Performance optimization opportunities identified'
    }
}
```

---

## 🧪 Testing y Validación

### **Test Scenarios**

```yaml
Test_Scenarios:
  intent_classification:
    - input: "Quiero rentar un apartamento de 2 recámaras"
      expected_intent: "leasing"
      expected_agent: "lead_qualifier"
      
    - input: "Me gustaría agendar una visita para mañana"
      expected_intent: "tours"
      expected_agent: "vivi"
      
    - input: "El aire acondicionado no está funcionando"
      expected_intent: "maintenance"
      expected_agent: "maintenance"
      
  routing_optimization:
    - scenario: "All agents available"
      expected: "Route to highest specialization match"
      
    - scenario: "Primary agent busy"
      expected: "Route to best available alternative"
      
    - scenario: "Complex multi-agent case"
      expected: "Route to primary, prepare handoff to secondary"
```

---

## 🎯 Próximos Pasos

1. **[Implementar Vivi (Tours Agent)](../tour-management-agent/agent-implementation.md)** - Agente especializado en tours
2. **[Configurar Lead Qualifier](../lead-qualification-agent/agent-implementation.md)** - Calificación de prospectos
3. **[Setup Maintenance Agent](../maintenance-agent/agent-implementation.md)** - Automatización de mantenimiento
4. **[Deploy Customer Service](../customer-service-agent/agent-implementation.md)** - Soporte general

---

**🚦 Orchestrator implementado con patrones LangChain DialogueSimulator**  
📅 Versión: 2.0 - Advanced Orchestration Intelligence  
🔄 Última actualización: 2025-09-01