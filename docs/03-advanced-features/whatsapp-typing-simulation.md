# WhatsApp Typing Simulation para Bird.com AI Employees

## 📋 Resumen Ejecutivo

Esta documentación proporciona una implementación completa para simular el efecto "typing..." (está escribiendo) en WhatsApp Business API para los AI Employees de Bird.com, creando una experiencia más humana en las conversaciones automatizadas.

### 🔍 Hallazgos Clave de Investigación

- **❌ WhatsApp Business API NO soporta indicadores de typing nativos**
- **✅ Implementación posible mediante delays estratégicos y gestión de flujo de conversación**
- **⚡ Mejora significativa en la experiencia de usuario con implementación adecuada**

---

## 🎯 Estrategias de Implementación

### 1. Simulación de Typing mediante Delays Calculados

La estrategia principal consiste en calcular delays realistas basados en velocidades de escritura humana:

```javascript
function calculateTypingDelay(responseText, complexity = 'medium') {
  const words = responseText.split(' ').length;
  const characters = responseText.length;
  
  // Velocidades base de escritura (palabras por minuto)
  const speeds = {
    simple: 50,    // Respuestas rápidas
    medium: 35,    // Respuestas estándar  
    complex: 25    // Respuestas detalladas
  };
  
  const wpm = speeds[complexity];
  const baseTypingTime = (words / wpm) * 60 * 1000; // Convertir a ms
  
  // Añadir tiempo de "pensamiento" para respuestas complejas
  const thinkingTime = complexity === 'complex' ? 3000 : 1000;
  
  // Añadir variación aleatoria (±20%)
  const variation = (Math.random() - 0.5) * 0.4 + 1;
  
  return Math.max(
    Math.min((baseTypingTime + thinkingTime) * variation, 30000), // Máx 30s
    1000 // Mín 1s
  );
}
```

### 2. Message Chunking para Respuestas Largas

División de respuestas extensas en fragmentos más naturales:

```javascript
async function sendChunkedResponse(longResponse, phoneNumberId, recipientId) {
  const chunks = splitIntoChunks(longResponse, 300); // Fragmentos de 300 caracteres
  
  for (let i = 0; i < chunks.length; i++) {
    if (i > 0) {
      // Añadir delay entre fragmentos para simular escritura continua
      await new Promise(resolve => setTimeout(resolve, 3000));
    }
    
    await sendWhatsAppMessage({
      messaging_product: "whatsapp",
      to: recipientId,
      type: "text",
      text: { body: chunks[i] }
    });
  }
}
```

---

## 🔧 Implementación Técnica para Bird.com

### Clase Principal: WhatsAppTypingSimulator

```javascript
class WhatsAppTypingSimulator {
  constructor(phoneNumberId, accessToken) {
    this.phoneNumberId = phoneNumberId;
    this.accessToken = accessToken;
    this.baseUrl = `https://graph.facebook.com/v18.0/${phoneNumberId}`;
  }

  async sendMessageWithTypingSimulation(to, message, options = {}) {
    try {
      // Calcular delay de typing
      const delay = this.calculateTypingDelay(message, options.complexity);
      
      // Log interno para tracking
      console.log(`Simulando typing por ${delay}ms`);
      
      // Aplicar delay de typing
      await this.sleep(delay);
      
      // Enviar mensaje
      const response = await fetch(`${this.baseUrl}/messages`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          messaging_product: "whatsapp",
          to: to,
          type: "text",
          text: { body: message }
        })
      });

      return await response.json();
    } catch (error) {
      console.error('Error enviando mensaje de WhatsApp:', error);
      throw error;
    }
  }

  calculateTypingDelay(message, complexity = 'medium') {
    const words = message.split(' ').length;
    const speeds = { simple: 60, medium: 40, complex: 25 };
    const wpm = speeds[complexity];
    
    const typingTime = (words / wpm) * 60 * 1000;
    const thinkingTime = complexity === 'complex' ? 3000 : 1500;
    
    return Math.max(Math.min(typingTime + thinkingTime, 20000), 1000);
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### Integración Específica con Bird.com

```javascript
class BirdWhatsAppIntegration extends WhatsAppTypingSimulator {
  constructor(config) {
    super(config.phoneNumberId, config.accessToken);
    this.birdApiKey = config.birdApiKey;
    this.conversationStates = new Map();
  }

  async processBirdAIMessage(incomingMessage) {
    const { from, text, timestamp } = incomingMessage;
    
    // Obtener o crear estado de conversación
    const state = this.getConversationState(from);
    
    // Generar respuesta del AI de Bird.com
    const aiResponse = await this.callBirdAI(text.body, state.context);
    
    // Determinar complejidad de respuesta basada en output del AI
    const complexity = this.analyzeResponseComplexity(aiResponse);
    
    // Enviar con simulación de typing
    await this.sendMessageWithTypingSimulation(from, aiResponse, { complexity });
    
    // Actualizar estado de conversación
    this.updateConversationState(from, { 
      last_response: aiResponse, 
      timestamp: Date.now() 
    });
  }

  async callBirdAI(message, context) {
    // Integración con API de Bird.com AI
    const response = await fetch('https://api.bird.com/ai/chat', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.birdApiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: message,
        context: context,
        platform: 'whatsapp'
      })
    });
    
    const result = await response.json();
    return result.response;
  }

  analyzeResponseComplexity(response) {
    if (response.length < 50) return 'simple';
    if (response.includes('déjame revisar') || response.includes('calcular')) return 'complex';
    return 'medium';
  }

  getConversationState(userId) {
    if (!this.conversationStates.has(userId)) {
      this.conversationStates.set(userId, {
        context: [],
        last_interaction: Date.now(),
        interaction_count: 0
      });
    }
    return this.conversationStates.get(userId);
  }

  updateConversationState(userId, updates) {
    const state = this.getConversationState(userId);
    Object.assign(state, updates);
    state.interaction_count++;
    state.last_interaction = Date.now();
  }
}
```

---

## ⏱️ Configuraciones de Timing Recomendadas

### Patrones de Timing Óptimos

```javascript
const conversationTimings = {
  // Contacto inicial
  first_message: {
    acknowledgment: 500,   // Reconocimiento rápido "Vi tu mensaje"
    response: 3000        // Respuesta inicial reflexiva
  },
  
  // Conversación en curso
  follow_up: {
    simple_answer: 1500,   // Respuestas factual rápidas
    explanation: 4000,     // Explicaciones detalladas
    research_needed: 8000  // Consultas complejas que requieren búsqueda
  },
  
  // Gestión de conversación
  clarification_request: 2000,  // Pidiendo más información
  goodbye: 1000,               // Cierre cortés
  error_recovery: 2500         // Manejando malentendidos
};
```

### Ajuste Dinámico de Timing

```javascript
function adaptTimingToContext(baseDelay, contextFactors) {
  let adjustedDelay = baseDelay;
  
  // Ajuste por hora del día
  if (contextFactors.isBusinessHours) {
    adjustedDelay *= 0.8; // Más rápido en horario laboral
  }
  
  // Nivel de paciencia del usuario (inferido de frecuencia de mensajes)
  if (contextFactors.userImpatience > 0.7) {
    adjustedDelay *= 0.6; // Más rápido para usuarios impacientes
  }
  
  // Urgencia del mensaje
  if (contextFactors.urgencyKeywords.length > 0) {
    adjustedDelay *= 0.5; // Mucho más rápido para mensajes urgentes
  }
  
  return Math.max(adjustedDelay, 500); // Nunca menos de 500ms
}
```

---

## 🚀 Configuración de Webhook para Bird.com

### Endpoint de Webhook

```javascript
// Endpoint de webhook de Bird.com para mensajes de WhatsApp
app.post('/webhook/whatsapp', async (req, res) => {
  const { entry } = req.body;
  
  for (const change of entry[0].changes) {
    if (change.field === 'messages') {
      const message = change.value.messages[0];
      
      // Procesar con simulación de typing
      await processMessageWithTypingSimulation(message);
    }
  }
  
  res.status(200).send('OK');
});

async function processMessageWithTypingSimulation(message) {
  // 1. Marcar mensaje como recibido inmediatamente
  await markMessageAsReceived(message.id);
  
  // 2. Generar respuesta del AI
  const aiResponse = await generateBirdAIResponse(message.text.body);
  
  // 3. Calcular y aplicar delay de typing
  const typingDelay = calculateTypingDelay(aiResponse);
  await simulateTypingDelay(typingDelay);
  
  // 4. Enviar respuesta
  await sendWhatsAppMessage(aiResponse, message.from);
}
```

### Configuración de Variables de Entorno

```bash
# Variables requeridas para Bird.com WhatsApp Integration
WHATSAPP_ACCESS_TOKEN=tu_access_token_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id_aqui
BIRD_API_KEY=tu_bird_api_key_aqui
WEBHOOK_VERIFY_TOKEN=tu_webhook_verify_token_aqui

# Configuraciones opcionales
TYPING_SIMULATION_ENABLED=true
MAX_TYPING_DELAY=30000
MIN_TYPING_DELAY=1000
DEFAULT_TYPING_COMPLEXITY=medium
```

---

## 📊 Gestión de Estado de Conversaciones

### Sistema de Estados de Conversación

```javascript
class ConversationStateManager {
  constructor() {
    this.conversations = new Map();
    this.cleanupInterval = 3600000; // Limpiar cada hora
    this.maxStateAge = 86400000; // 24 horas máximo
    
    // Iniciar limpieza automática
    setInterval(() => this.cleanupOldStates(), this.cleanupInterval);
  }

  getState(userId) {
    const now = Date.now();
    
    if (!this.conversations.has(userId)) {
      this.conversations.set(userId, {
        created: now,
        last_updated: now,
        interaction_count: 0,
        context: [],
        user_behavior: {
          avg_response_time: 0,
          patience_level: 'normal',
          typical_message_length: 0
        },
        typing_preferences: {
          preferred_delay: 'auto',
          complexity_override: null
        }
      });
    }

    const state = this.conversations.get(userId);
    state.last_updated = now;
    return state;
  }

  updateState(userId, updates) {
    const state = this.getState(userId);
    Object.assign(state, updates);
    state.interaction_count++;
    
    // Actualizar comportamiento del usuario
    this.analyzeUserBehavior(state, updates);
  }

  analyzeUserBehavior(state, lastInteraction) {
    // Analizar patrones de comportamiento para ajustar timing
    if (lastInteraction.response_time) {
      const currentAvg = state.user_behavior.avg_response_time;
      state.user_behavior.avg_response_time = 
        (currentAvg * 0.8) + (lastInteraction.response_time * 0.2);
    }

    // Determinar nivel de paciencia
    if (state.user_behavior.avg_response_time < 5000) {
      state.user_behavior.patience_level = 'low';
    } else if (state.user_behavior.avg_response_time > 20000) {
      state.user_behavior.patience_level = 'high';
    }
  }

  cleanupOldStates() {
    const now = Date.now();
    for (const [userId, state] of this.conversations.entries()) {
      if (now - state.last_updated > this.maxStateAge) {
        this.conversations.delete(userId);
      }
    }
  }
}
```

---

## 🔄 Gestión de Colas para Conversaciones Múltiples

### Sistema de Colas Inteligente

```javascript
class ConversationQueueManager {
  constructor() {
    this.activeConversations = new Map();
    this.responseQueue = [];
    this.processingQueue = false;
  }

  async queueResponse(userId, response, priority = 'normal', context = {}) {
    const item = {
      userId,
      response,
      priority,
      context,
      timestamp: Date.now(),
      estimatedDelay: this.calculateDelay(response, context)
    };

    // Insertar basado en prioridad y timing
    this.insertByPriority(item);
    
    // Procesar cola si no está ya procesándose
    if (!this.processingQueue) {
      await this.processQueue();
    }
  }

  insertByPriority(item) {
    const priorities = { urgent: 0, high: 1, normal: 2, low: 3 };
    const itemPriority = priorities[item.priority];

    let insertIndex = this.responseQueue.length;
    for (let i = 0; i < this.responseQueue.length; i++) {
      if (priorities[this.responseQueue[i].priority] > itemPriority) {
        insertIndex = i;
        break;
      }
    }

    this.responseQueue.splice(insertIndex, 0, item);
  }

  async processQueue() {
    this.processingQueue = true;

    while (this.responseQueue.length > 0) {
      const item = this.responseQueue.shift();
      
      // Verificar si el usuario sigue en conversación activa
      if (this.shouldProcessMessage(item)) {
        await this.sendWithSimulatedTyping(item);
      }
    }

    this.processingQueue = false;
  }

  shouldProcessMessage(item) {
    const now = Date.now();
    const timeSinceQueued = now - item.timestamp;
    
    // No procesar mensajes muy antiguos (>2 minutos)
    return timeSinceQueued < 120000;
  }

  async sendWithSimulatedTyping(item) {
    try {
      // Marcar conversación como activa
      this.activeConversations.set(item.userId, {
        status: 'typing',
        startTime: Date.now()
      });

      // Aplicar delay de typing
      await new Promise(resolve => setTimeout(resolve, item.estimatedDelay));

      // Enviar mensaje
      await this.sendMessage(item.userId, item.response);

      // Actualizar estado de conversación
      this.activeConversations.set(item.userId, {
        status: 'idle',
        lastMessage: Date.now()
      });

    } catch (error) {
      console.error(`Error procesando mensaje para ${item.userId}:`, error);
      // Reintentar una vez
      setTimeout(() => this.queueResponse(
        item.userId, 
        item.response, 
        'high', 
        { ...item.context, retry: true }
      ), 5000);
    }
  }

  calculateDelay(response, context) {
    // Usar la función de cálculo de delay principal
    return calculateTypingDelay(response, context.complexity || 'medium');
  }
}
```

---

## 📈 Monitoreo y Optimización

### Métricas Clave para Monitorear

```javascript
const monitoringMetrics = {
  // Métricas de rendimiento
  performance: {
    avg_response_time: "Tiempo promedio de respuesta incluyendo delays",
    message_delivery_rate: "Tasa de entrega exitosa de mensajes",
    error_rate: "Tasa de errores en simulación de typing",
    queue_processing_time: "Tiempo de procesamiento de cola"
  },
  
  // Métricas de experiencia de usuario
  user_experience: {
    conversation_completion_rate: "Mensajes que llevan a resolución exitosa",
    user_satisfaction_score: "Puntuación de satisfacción inferida",
    conversation_length: "Duración promedio de conversaciones",
    user_return_rate: "Tasa de usuarios que regresan"
  },
  
  // Métricas de efectividad
  effectiveness: {
    typing_detection_rate: "Tasa de usuarios que detectan delays artificiales",
    engagement_improvement: "Mejora en engagement vs respuestas inmediatas",
    business_outcome_impact: "Impacto en métricas de negocio"
  }
};
```

### Sistema de Analytics

```javascript
class TypingSimulationAnalytics {
  constructor() {
    this.metrics = {
      daily: new Map(),
      hourly: new Map(),
      user_specific: new Map()
    };
  }

  recordTypingEvent(userId, eventType, data) {
    const timestamp = Date.now();
    const date = new Date(timestamp).toISOString().split('T')[0];
    const hour = new Date(timestamp).getHours();

    // Métricas diarias
    if (!this.metrics.daily.has(date)) {
      this.metrics.daily.set(date, {
        total_events: 0,
        avg_delay: 0,
        user_satisfaction: 0,
        errors: 0
      });
    }

    // Métricas por usuario
    if (!this.metrics.user_specific.has(userId)) {
      this.metrics.user_specific.set(userId, {
        total_interactions: 0,
        preferred_timing: 'auto',
        satisfaction_trend: [],
        typing_effectiveness: 0
      });
    }

    // Registrar evento específico
    this.updateMetrics(date, hour, userId, eventType, data);
  }

  updateMetrics(date, hour, userId, eventType, data) {
    const dailyMetrics = this.metrics.daily.get(date);
    const userMetrics = this.metrics.user_specific.get(userId);

    switch (eventType) {
      case 'typing_simulation_start':
        dailyMetrics.total_events++;
        userMetrics.total_interactions++;
        break;
        
      case 'typing_simulation_complete':
        const avgDelay = dailyMetrics.avg_delay;
        dailyMetrics.avg_delay = (avgDelay * 0.9) + (data.delay * 0.1);
        break;
        
      case 'user_satisfaction_feedback':
        userMetrics.satisfaction_trend.push(data.score);
        if (userMetrics.satisfaction_trend.length > 10) {
          userMetrics.satisfaction_trend.shift();
        }
        break;
        
      case 'typing_detection':
        userMetrics.typing_effectiveness = Math.max(0, 
          userMetrics.typing_effectiveness - 0.1);
        break;
    }
  }

  generateDailyReport(date) {
    const metrics = this.metrics.daily.get(date);
    if (!metrics) return null;

    return {
      date,
      total_typing_events: metrics.total_events,
      average_delay: Math.round(metrics.avg_delay),
      error_rate: (metrics.errors / metrics.total_events) * 100,
      user_satisfaction: this.calculateOverallSatisfaction(date),
      recommendations: this.generateRecommendations(metrics)
    };
  }

  generateRecommendations(metrics) {
    const recommendations = [];

    if (metrics.avg_delay > 10000) {
      recommendations.push("Considerar reducir delays promedio - pueden ser muy largos");
    }

    if (metrics.error_rate > 0.05) {
      recommendations.push("Investigar y corregir errores en simulación de typing");
    }

    if (this.calculateOverallSatisfaction() < 7) {
      recommendations.push("Optimizar timing basado en feedback de usuarios");
    }

    return recommendations;
  }
}
```

---

## ⚠️ Limitaciones y Consideraciones

### Limitaciones Técnicas

```javascript
const technicalLimitations = {
  whatsapp_api: {
    no_native_typing: "WhatsApp Business API no soporta indicadores nativos",
    rate_limits: "1,000 mensajes por segundo (Cloud API)",
    message_ordering: "No garantiza orden de entrega para mensajes rápidos",
    session_timeout: "Ventana de 24 horas para mensajes"
  },
  
  implementation_challenges: {
    detection_risk: "Usuarios pueden detectar delays artificiales",
    timing_precision: "Latencia de red afecta precisión",
    memory_usage: "Estados de conversación consumen memoria",
    scaling_complexity: "Complejidad aumenta con múltiples conversaciones"
  }
};
```

### Estrategias de Mitigación de Riesgos

```javascript
const riskMitigations = {
  timing_detection: {
    strategy: "Añadir variación aleatoria a delays",
    implementation: "Variancia del ±20% en tiempos calculados",
    monitoring: "Detectar patrones de abandono post-delay"
  },
  
  user_frustration: {
    strategy: "Timing adaptativo basado en comportamiento del usuario",
    implementation: "Respuestas más rápidas para usuarios recurrentes",
    fallback: "Opción de desactivar delays para consultas urgentes"
  },
  
  system_reliability: {
    strategy: "Fallback a respuestas inmediatas",
    implementation: "Omitir delays durante alta carga o errores",
    monitoring: "Alertas automáticas para degradación de servicio"
  },
  
  compliance_privacy: {
    strategy: "Almacenamiento seguro de estados de conversación",
    implementation: "Cifrado de datos y limpieza automática",
    compliance: "Cumplimiento con GDPR/CCPA para datos de conversación"
  }
};
```

---

## 🚀 Roadmap de Implementación

### Fase 1: Implementación Básica (2-3 semanas)

**Semana 1:**
- [ ] Implementar algoritmos básicos de cálculo de delay
- [ ] Crear integración de webhook con WhatsApp Cloud API
- [ ] Desarrollar sistema básico de gestión de estado de conversación
- [ ] Configurar entorno de pruebas

**Semana 2:**
- [ ] Integrar con pipeline de procesamiento de AI de Bird.com
- [ ] Implementar sistema de análisis de complejidad de respuesta
- [ ] Crear sistema básico de monitoreo
- [ ] Pruebas con grupo limitado de usuarios

**Semana 3:**
- [ ] Refinamiento basado en feedback inicial
- [ ] Optimización de rendimiento
- [ ] Documentación de API interna
- [ ] Preparación para Fase 2

### Fase 2: Funcionalidades Avanzadas (3-4 semanas)

**Semana 4-5:**
- [ ] Implementar ajustes de timing conscientes del contexto
- [ ] Desarrollar sistema de message chunking
- [ ] Crear gestión de colas para conversaciones múltiples
- [ ] Añadir analytics y métricas de rendimiento

**Semana 6-7:**
- [ ] Sistema de aprendizaje adaptativo basado en comportamiento de usuario
- [ ] Implementar manejo de errores y fallbacks
- [ ] Crear dashboard de monitoreo en tiempo real
- [ ] Pruebas de carga y optimización

### Fase 3: Optimización y Escalado (2-3 semanas)

**Semana 8-9:**
- [ ] Análisis de complejidad impulsado por AI
- [ ] Timing dinámico basado en comportamiento del usuario
- [ ] Balanceado de carga y manejo de errores avanzado
- [ ] Sistema de A/B testing integrado

**Semana 10:**
- [ ] Pruebas comprehensivas y validación de rendimiento
- [ ] Documentación final y guías de usuario
- [ ] Despliegue gradual y monitoreo
- [ ] Análisis de resultados y optimizaciones finales

---

## 🔧 Código de Ejemplo Completo

### Implementación Lista para Producción

```javascript
// whatsapp-typing-simulator.js
const express = require('express');
const fetch = require('node-fetch');

class ProductionWhatsAppTypingSimulator {
  constructor(config) {
    this.config = config;
    this.app = express();
    this.conversationManager = new ConversationStateManager();
    this.queueManager = new ConversationQueueManager();
    this.analytics = new TypingSimulationAnalytics();
    
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupMiddleware() {
    this.app.use(express.json());
    this.app.use((req, res, next) => {
      // Logging y monitoring
      console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
      next();
    });
  }

  setupRoutes() {
    // Webhook de verificación
    this.app.get('/webhook', (req, res) => {
      const verifyToken = req.query['hub.verify_token'];
      if (verifyToken === this.config.WEBHOOK_VERIFY_TOKEN) {
        res.send(req.query['hub.challenge']);
      } else {
        res.status(403).send('Token de verificación inválido');
      }
    });

    // Webhook de mensajes
    this.app.post('/webhook', async (req, res) => {
      try {
        await this.handleIncomingMessage(req.body);
        res.status(200).send('OK');
      } catch (error) {
        console.error('Error procesando mensaje:', error);
        res.status(500).send('Error interno del servidor');
      }
    });

    // Endpoint de métricas
    this.app.get('/metrics', (req, res) => {
      const date = req.query.date || new Date().toISOString().split('T')[0];
      const report = this.analytics.generateDailyReport(date);
      res.json(report);
    });

    // Endpoint de configuración
    this.app.post('/config/user/:userId', (req, res) => {
      const { userId } = req.params;
      const { typing_preferences } = req.body;
      
      const state = this.conversationManager.getState(userId);
      state.typing_preferences = { ...state.typing_preferences, ...typing_preferences };
      
      res.json({ success: true, preferences: state.typing_preferences });
    });
  }

  async handleIncomingMessage(body) {
    const entry = body.entry?.[0];
    const changes = entry?.changes?.[0];
    
    if (changes?.field === 'messages') {
      const messages = changes.value?.messages;
      if (messages?.length > 0) {
        const message = messages[0];
        await this.processMessage(message, changes.value.metadata.phone_number_id);
      }
    }
  }

  async processMessage(message, phoneNumberId) {
    const userId = message.from;
    const messageText = message.text?.body;
    
    if (!messageText) return; // Solo procesar mensajes de texto

    try {
      // Registrar evento
      this.analytics.recordTypingEvent(userId, 'message_received', {
        message_length: messageText.length,
        timestamp: Date.now()
      });

      // Obtener respuesta del AI de Bird.com
      const aiResponse = await this.getBirdAIResponse(messageText, userId);
      
      // Determinar complejidad y prioridad
      const complexity = this.analyzeResponseComplexity(aiResponse, messageText);
      const priority = this.determinePriority(messageText, userId);
      
      // Encolar respuesta con simulación de typing
      await this.queueManager.queueResponse(userId, aiResponse, priority, {
        complexity,
        phone_number_id: phoneNumberId,
        original_message: messageText
      });

    } catch (error) {
      console.error(`Error procesando mensaje de ${userId}:`, error);
      
      // Enviar respuesta de error sin delay
      await this.sendImmediateResponse(userId, phoneNumberId, 
        "Disculpa, hubo un problema técnico. Por favor intenta de nuevo.");
    }
  }

  async getBirdAIResponse(message, userId) {
    const conversationState = this.conversationManager.getState(userId);
    
    try {
      const response = await fetch(`${this.config.BIRD_API_URL}/ai/chat`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.config.BIRD_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message,
          context: conversationState.context.slice(-5), // Últimas 5 interacciones
          user_id: userId,
          platform: 'whatsapp',
          typing_simulation: true
        })
      });

      if (!response.ok) {
        throw new Error(`Bird API error: ${response.status}`);
      }

      const result = await response.json();
      
      // Actualizar contexto de conversación
      this.conversationManager.updateState(userId, {
        context: [...conversationState.context.slice(-4), {
          user_message: message,
          ai_response: result.response,
          timestamp: Date.now()
        }]
      });

      return result.response;

    } catch (error) {
      console.error('Error llamando a Bird AI:', error);
      throw error;
    }
  }

  analyzeResponseComplexity(response, originalMessage) {
    // Palabras clave que indican complejidad
    const complexKeywords = [
      'analizar', 'calcular', 'investigar', 'revisar', 'consultar',
      'verificar', 'comparar', 'evaluar', 'procesar'
    ];
    
    const urgentKeywords = [
      'urgente', 'emergencia', 'inmediato', 'rápido', 'ahora'
    ];

    // Análisis básico
    if (urgentKeywords.some(keyword => 
      originalMessage.toLowerCase().includes(keyword))) {
      return 'simple'; // Responder rápido a urgencias
    }

    if (response.length < 50) return 'simple';
    
    if (response.length > 200 || 
        complexKeywords.some(keyword => 
          response.toLowerCase().includes(keyword))) {
      return 'complex';
    }

    return 'medium';
  }

  determinePriority(message, userId) {
    const urgentPatterns = /\b(urgente|emergencia|ayuda|problema)\b/i;
    const conversationState = this.conversationManager.getState(userId);
    
    if (urgentPatterns.test(message)) return 'urgent';
    if (conversationState.interaction_count === 0) return 'high'; // Primer contacto
    
    return 'normal';
  }

  async sendImmediateResponse(userId, phoneNumberId, message) {
    try {
      const response = await fetch(
        `https://graph.facebook.com/v18.0/${phoneNumberId}/messages`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.config.WHATSAPP_ACCESS_TOKEN}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            messaging_product: "whatsapp",
            to: userId,
            type: "text",
            text: { body: message }
          })
        }
      );

      if (!response.ok) {
        throw new Error(`WhatsApp API error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error enviando respuesta inmediata:', error);
      throw error;
    }
  }

  start(port = 3000) {
    this.app.listen(port, () => {
      console.log(`🚀 Servidor de simulación de typing iniciado en puerto ${port}`);
      console.log(`📱 Webhook URL: http://localhost:${port}/webhook`);
      console.log(`📊 Métricas disponibles en: http://localhost:${port}/metrics`);
    });
  }
}

// Configuración y inicio
const config = {
  WHATSAPP_ACCESS_TOKEN: process.env.WHATSAPP_ACCESS_TOKEN,
  WEBHOOK_VERIFY_TOKEN: process.env.WEBHOOK_VERIFY_TOKEN,
  BIRD_API_KEY: process.env.BIRD_API_KEY,
  BIRD_API_URL: process.env.BIRD_API_URL || 'https://api.bird.com'
};

// Validar configuración
const requiredConfig = ['WHATSAPP_ACCESS_TOKEN', 'WEBHOOK_VERIFY_TOKEN', 'BIRD_API_KEY'];
for (const key of requiredConfig) {
  if (!config[key]) {
    console.error(`❌ Variable de entorno faltante: ${key}`);
    process.exit(1);
  }
}

// Iniciar servidor
const simulator = new ProductionWhatsAppTypingSimulator(config);
simulator.start(process.env.PORT || 3000);

module.exports = ProductionWhatsAppTypingSimulator;
```

---

## 📝 Conclusiones y Próximos Pasos

### Resumen de Implementación

Esta documentación proporciona una implementación completa para simular indicadores de typing en WhatsApp Business API para Bird.com AI employees. Aunque WhatsApp no soporta typing indicators nativos para la API de negocios, la implementación de delays estratégicos y gestión inteligente de flujo de conversación puede crear una experiencia significativamente más humana.

### Beneficios Esperados

1. **📈 Mejora en Experiencia de Usuario**: Conversaciones más naturales y humanas
2. **⚡ Mayor Engagement**: Usuarios más comprometidos con la conversación
3. **🎯 Personalización**: Adaptación automática al comportamiento del usuario
4. **📊 Insights Valiosos**: Métricas detalladas sobre patrones de conversación

### Próximos Pasos Recomendados

1. **Implementar Fase 1** con funcionalidad básica de typing simulation
2. **Ejecutar pruebas A/B** para medir impacto en satisfacción del usuario
3. **Recopilar métricas** durante 2-4 semanas para optimización
4. **Iterar y mejorar** basado en datos reales de uso
5. **Escalar gradualmente** a todos los AI employees de Bird.com

### Contacto y Soporte

Para preguntas sobre implementación o soporte técnico, consultar:
- Documentación oficial de WhatsApp Business API
- Portal de desarrolladores de Bird.com
- Repositorio de código interno para actualizaciones

### Enlaces Relacionados

- [Implementación de Foundation](../02-implementation/phase1-foundation.md) - Configuración básica del sistema WhatsApp
- [Funcionalidades de Intelligence](../02-implementation/phase2-intelligence.md) - Capacidades avanzadas de AI
- [Arquitectura del Sistema](../01-architecture/system-overview.md) - Vista general de la arquitectura

---

*Última actualización: Septiembre 2024*
*Versión: 1.0.0*