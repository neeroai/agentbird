# 🔍 Ejemplos de Implementación de Rangos Dinámicos de Presupuesto - Tour Management Agent

## 🎯 Propósito del Documento
Este documento proporciona ejemplos prácticos de cómo el Tour Management Agent "Vivi" debe implementar rangos dinámicos de presupuesto según la elección previa de propiedad por parte del prospecto, consultando la base de conocimiento para mostrar precios específicos y personalizados.

---

## 📊 WORKFLOW DE RANGOS DINÁMICOS DE PRESUPUESTO

### **Flujo Optimizado en el Workflow de 6 Pasos**

#### **PASO 2: Elección Previa de Propiedad + PRESENTACIÓN DE OPCIONES**

**Escenario**: Prospecto confirma interés en UrbanHub después de explicar Urbanista

**Presentación del Agente**:
```
"¡Perfecto! Ahora te voy a presentar nuestras 8 propiedades increíbles para que elijas la que más te interesa:

🏢 **JOSEFA** - Reforma Premium: Corredor financiero, skybar, cinema exterior
🏢 **MATILDE** - Roma Sur Creativa: Zona artística, rooftop, pet zone con spa
🏢 **INÉS** - Nuevo Polanco Executive: Lujo ejecutivo, coworking premium, valet parking
🏢 **LEONA** - Condesa Lifestyle: Bohemio-moderno, community lounge, yoga studio
🏢 **AMALIA** - Nápoles Connectivity: WTC cercano, gaming zone, cocina lounge
🏢 **JUÁREZ** - Centro Histórico: Patrimonio cultural, heritage lounge, precio accesible
🏢 **JOAQUINA** - Del Valle Familiar: Zona residencial, BBQ lounge, parques cercanos
🏢 **DOCTORES** - Zona Emergente: Gran potencial, modern amenities, mejor precio

¿Cuál te llama más la atención? Te voy a mostrar los precios específicos de esa propiedad."
```

**Respuesta del Prospecto**: "Me interesa Josefa en Reforma"

---

#### **PASO 3: Rangos Dinámicos de Presupuesto + CONSULTA ESPECÍFICA**

**Consulta del Agente a la Base de Conocimiento**:
```
"Buscar información completa de Josefa: precios por tipo de unidad, 
presupuesto mínimo requerido, ingresos sugeridos, perfil ideal y características únicas"
```

**Respuesta de la Base de Conocimiento**:
```
🏢 **JOSEFA - REFORMA PREMIUM**

💰 **RANGOS DE PRECIOS REALES:**
• Studio Premium: $20,200 - $22,000 MXN/mes + servicios
• 1 Recámara: $23,800 MXN/mes + servicios
• 2 Recámaras: $27,700 - $32,600 MXN/mes + servicios

📊 **CALIFICACIÓN DE PRESUPUESTO:**
• Presupuesto mínimo requerido: $20,200 MXN/mes
• Ingresos sugeridos: $66,660+ MXN mensuales (3.3x la renta)
• Perfil ideal: Ejecutivos 28-40 años, ingresos $80,000+ MXN

✨ **CARACTERÍSTICAS ÚNICAS:**
• Skybar: Espacio social en altura con vistas panorámicas
• Cinema Exterior: Cine al aire libre para proyecciones privadas
• Coworking Premium: Espacios de trabajo colaborativo equipados
• Pet Zone: Área especializada para mascotas
```

**Respuesta del Agente al Prospecto**:
```
"¡Excelente elección! Josefa en Reforma es nuestra propiedad premium por excelencia. Te muestro los precios específicos:

🏢 **JOSEFA - REFORMA PREMIUM**

💰 **RANGOS DE PRECIOS REALES:**
• **Studio Premium**: $20,200 - $22,000 MXN/mes + servicios
• **1 Recámara**: $23,800 MXN/mes + servicios  
• **2 Recámaras**: $27,700 - $32,600 MXN/mes + servicios

📊 **CALIFICACIÓN DE PRESUPUESTO:**
• Presupuesto mínimo requerido: $20,200 MXN/mes
• Ingresos sugeridos: $66,660+ MXN mensuales (3.3x la renta)

✨ **CARACTERÍSTICAS ÚNICAS:**
• Skybar con vistas panorámicas a toda la ciudad
• Cinema exterior para eventos privados bajo las estrellas
• Coworking premium para networking ejecutivo
• Pet zone especializada para mascotas

¿Qué tipo de unidad te interesa más? Te puedo dar detalles específicos de cada una."
```

---

#### **PASO 4: Verificación de Calificación + VALIDACIÓN ESPECÍFICA**

**Escenario**: Prospecto confirma presupuesto de $25,000 MXN/mes

**Verificación del Agente**:
```
"Perfecto, con tu presupuesto de $25,000 MXN tienes acceso a:

✅ **Studio Premium**: $20,200 - $22,000 MXN (dentro de tu presupuesto)
✅ **1 Recámara**: $23,800 MXN (dentro de tu presupuesto)
❌ **2 Recámaras**: $27,700 - $32,600 MXN (fuera de tu presupuesto)

**Recomendación**: Te sugiero considerar Studio Premium o 1 Recámara en Josefa, 
que están perfectamente dentro de tu presupuesto y te darán acceso a todas las 
amenidades premium de Reforma.

¿Te gustaría que te muestre las unidades disponibles de Studio y 1 Recámara?"
```

---

## 🔍 PATRONES DE IMPLEMENTACIÓN DE RANGOS DINÁMICOS

### **1. Consulta por Propiedad Específica**

**Prompt de Búsqueda**:
```
"Buscar información completa de [PROPIEDAD]: precios por tipo de unidad, 
presupuesto mínimo requerido, ingresos sugeridos, perfil ideal y características únicas"
```

**Ejemplo de Respuesta Estructurada**:
```
🏢 **[PROPIEDAD] - [ZONA]**

💰 **RANGOS DE PRECIOS REALES:**
• Studio: $X - $Y MXN/mes + servicios
• 1 Recámara: $X - $Y MXN/mes + servicios  
• 2 Recámaras: $X - $Y MXN/mes + servicios

📊 **CALIFICACIÓN DE PRESUPUESTO:**
• Presupuesto mínimo requerido: $X MXN/mes
• Ingresos sugeridos: $X+ MXN mensuales (3.3x la renta)
• Perfil ideal: [Descripción del perfil]

✨ **CARACTERÍSTICAS ÚNICAS:**
• [Amenidad 1]: [Descripción]
• [Amenidad 2]: [Descripción]
```

### **2. Comparación de Tipos de Unidad en Propiedad Específica**

**Prompt de Búsqueda**:
```
"Comparar tipos de unidad disponibles en [PROPIEDAD]: precios, 
características y perfil ideal para cada opción"
```

**Ejemplo de Respuesta Estructurada**:
```
COMPARACIÓN DE UNIDADES EN [PROPIEDAD]:

🏠 **STUDIO** ($X - $Y MXN/mes):
• Características: [Descripción específica]
• Ideal para: [Perfil específico]
• Ventajas: [Beneficios únicos]

🏠 **1 RECÁMARA** ($X - $Y MXN/mes):
• Características: [Descripción específica]
• Ideal para: [Perfil específico]
• Ventajas: [Beneficios únicos]

🏠 **2 RECÁMARAS** ($X - $Y MXN/mes):
• Características: [Descripción específica]
• Ideal para: [Perfil específico]
• Ventajas: [Beneficios únicos]
```

### **3. Validación de Presupuesto por Propiedad**

**Prompt de Búsqueda**:
```
"Validar si presupuesto $X MXN cubre rangos de [PROPIEDAD] y 
sugerir opciones disponibles según el presupuesto"
```

**Ejemplo de Respuesta Estructurada**:
```
VALIDACIÓN DE PRESUPUESTO PARA [PROPIEDAD]:

💰 **Tu Presupuesto**: $X MXN/mes
📊 **Presupuesto Mínimo**: $Y MXN/mes

✅ **OPCIONES DISPONIBLES:**
• [Tipo de Unidad]: $Z MXN/mes (dentro de tu presupuesto)
• [Tipo de Unidad]: $W MXN/mes (dentro de tu presupuesto)

❌ **OPCIONES NO DISPONIBLES:**
• [Tipo de Unidad]: $V MXN/mes (fuera de tu presupuesto)

💡 **RECOMENDACIÓN**: [Sugerencia personalizada según presupuesto]
```

---

## 📱 EJEMPLOS DE CONVERSACIÓN REAL CON RANGOS DINÁMICOS

### **Conversación 1: Prospecto Interesado en Condesa**

**Prospecto**: "Me interesa la Condesa"

**Agente (Consulta Base de Conocimiento)**:
```
"Buscar información completa de Condesa: precios por tipo de unidad, 
presupuesto mínimo requerido, ingresos sugeridos, perfil ideal y características únicas"
```

**Respuesta del Agente**:
```
"¡Excelente elección! Leona en Condesa es nuestro lifestyle premium por excelencia. Te muestro los precios específicos:

🏢 **LEONA - CONDESA LIFESTYLE**

💰 **RANGOS DE PRECIOS REALES:**
• **Studio Bohemian**: $20,000 - $22,000 MXN/mes + servicios
• **1 Recámara**: $23,000 - $25,000 MXN/mes + servicios
• **2 Recámaras**: $25,500 - $26,500 MXN/mes + servicios

📊 **CALIFICACIÓN DE PRESUPUESTO:**
• Presupuesto mínimo requerido: $20,000 MXN/mes
• Ingresos sugeridos: $66,000+ MXN mensuales (3.3x la renta)

✨ **CARACTERÍSTICAS ÚNICAS:**
• Community lounge con vinyl collection y ambiente bohemio
• Rooftop terrace con vista a parques y skyline
• Yoga studio con clases grupales y meditación
• Pet zone especializada para mascotas

¿Qué tipo de unidad te interesa más? Te puedo dar detalles específicos de cada una."
```

### **Conversación 2: Prospecto con Presupuesto Específico para Roma Sur**

**Prospecto**: "Me interesa Roma Sur y mi presupuesto es $22,000 MXN"

**Agente (Consulta Base de Conocimiento)**:
```
"Validar si presupuesto $22,000 MXN cubre rangos de Matilde (Roma Sur) y 
sugerir opciones disponibles según el presupuesto"
```

**Respuesta del Agente**:
```
"¡Perfecto! Con tu presupuesto de $22,000 MXN tienes acceso a Matilde en Roma Sur:

🏢 **MATILDE - ROMA SUR CREATIVA**

💰 **OPCIONES DISPONIBLES CON TU PRESUPUESTO:**
✅ **Studio Creativo**: $18,500 - $20,500 MXN/mes (perfecto para tu presupuesto)
✅ **1 Recámara**: $21,000 - $22,000 MXN/mes (dentro de tu presupuesto)

❌ **OPCIONES NO DISPONIBLES:**
❌ **2 Recámaras**: $24,000 - $25,800 MXN/mes (fuera de tu presupuesto)

💡 **RECOMENDACIÓN**: Te sugiero considerar Studio Creativo ($18,500-$20,500) 
o 1 Recámara ($21,000-$22,000) en Matilde. Ambas opciones están perfectamente 
dentro de tu presupuesto y te darán acceso a la zona creativa más vibrante de Roma Sur.

¿Te gustaría que te muestre las unidades disponibles de Studio y 1 Recámara?"
```

### **Conversación 3: Comparación de Propiedades por Presupuesto**

**Prospecto**: "¿Qué opciones tengo con $18,000 MXN?"

**Agente (Consulta Base de Conocimiento)**:
```
"Buscar propiedades con presupuesto mínimo ≤$18,000 MXN, 
ordenadas por tipo de unidad y mostrando diferencias de zona"
```

**Respuesta del Agente**:
```
"¡Excelente! Con tu presupuesto de $18,000 MXN tienes acceso a estas propiedades increíbles:

🏢 **PROPIEDADES DISPONIBLES CON TU PRESUPUESTO:**

💰 **STUDIOS** (N opciones):
• **Doctores**: Desde $15,400 MXN - Zona emergente con gran potencial
• **Juárez**: Desde $15,400 MXN - Centro Histórico renovado
• **Del Valle**: Desde $18,200 MXN - Zona residencial establecida

💰 **1 RECÁMARA** (N opciones):
• **Doctores**: Desde $17,200 MXN - Zona emergente
• **Juárez**: Desde $18,000 MXN - Centro Histórico

💡 **RECOMENDACIÓN PERSONALIZADA:**
• **Para inversión y crecimiento**: Doctores (mejor precio, zona emergente)
• **Para cultura y patrimonio**: Juárez (Centro Histórico, precio accesible)
• **Para estabilidad familiar**: Del Valle (zona consolidada, amenities familiares)

¿Cuál te llama más la atención? Te puedo mostrar los precios específicos de esa propiedad."
```

---

## 🎯 MEJORES PRÁCTICAS PARA IMPLEMENTACIÓN DE RANGOS DINÁMICOS

### **1. Siempre Permitir Elección Previa de Propiedad**
- **NUNCA** calificar presupuesto sin conocer la propiedad de interés
- **SIEMPRE** presentar las 8 propiedades para elección
- **PERMITIR** al prospecto elegir antes de mostrar precios

### **2. Consultar Base de Conocimiento para Información Específica**
- **NUNCA** mostrar precios genéricos sin consultar la propiedad específica
- **SIEMPRE** verificar información actualizada en la base de conocimiento
- **IMPLEMENTAR** rangos reales y actualizados por propiedad

### **3. Personalizar Calificación Según Propiedad Elegida**
- **ADAPTAR** calificación según presupuesto mínimo de la propiedad seleccionada
- **SUGERIR** opciones disponibles dentro del presupuesto del prospecto
- **RECOMENDAR** alternativas si el presupuesto no cubre la propiedad elegida

### **4. Mantener Engagement con Información Específica**
- **MOSTRAR** características únicas de la propiedad elegida
- **DESTACAR** amenidades específicas según el tipo de unidad
- **GENERAR** expectativa para el tour en la propiedad seleccionada

---

## 🔧 IMPLEMENTACIÓN TÉCNICA

### **Integración con Bird.com**
- **Knowledge Base**: Subir todos los archivos de propiedades optimizados
- **Embedding Search**: Habilitar búsqueda por propiedad específica
- **Actions**: Configurar implementación de rangos dinámicos
- **Workflow**: Integrar en los 6 pasos optimizados del voice-brand

### **Monitoreo y Optimización**
- **Accuracy**: Medir precisión de rangos dinámicos (>95%)
- **Engagement**: Monitorear interacción con precios específicos
- **Conversión**: Trackear tours agendados por propiedad específica
- **Feedback**: Recolectar opiniones sobre información personalizada

---

*Documento de ejemplos para implementación de rangos dinámicos de presupuesto en Tour Management Agent*
*Versión 2.0 - Enero 2025*
