# 📄 Document Intelligence Agent - Procesamiento Avanzado de Documentos

## 📋 Resumen del Agente

**Document Intelligence Agent** es el especialista de UrbanHub en procesamiento inteligente de documentos inmobiliarios. Utiliza AWS Textract, Bedrock Claude, y patrones LangChain para OCR avanzado, análisis legal automático, clasificación de documentos y validación de firmas, optimizado para integración nativa con Bird.com.

### 🎯 Especialización Principal

#### **Procesamiento Inteligente de Documentos**
- **OCR Multiidioma**: Extracción texto con >98% precisión (Español/Inglés)
- **Legal Document Analysis**: Análisis automático contratos y documentos legales
- **Signature Verification**: Validación de firmas digitales y manuscritas
- **Document Classification**: Clasificación automática por tipo y relevancia

#### **Capacidades Avanzadas**
- **Contract Clause Extraction**: Extracción inteligente de cláusulas específicas
- **Financial Document Processing**: Análisis estados financieros y comprobantes
- **Identity Verification**: Validación documentos de identidad oficiales
- **Compliance Checking**: Verificación cumplimiento normativo automática

## 🏗️ Arquitectura del Agente

### **Agent Scoring System**

```python
class DocumentIntelligenceAgent(MultimodalBirdAgent):
    
    specializations = [
        "document_ocr",                # Score weight: 35%
        "legal_document_analysis",     # Score weight: 25% 
        "contract_extraction",         # Score weight: 20%
        "document_classification",     # Score weight: 15%
        "signature_verification"       # Score weight: 5%
    ]
    
    def calculate_bid_score(self, analysis):
        """
        Bidding especializado para procesamiento de documentos
        Score alto para inputs con documentos adjuntos
        """
        base_score = 0.0
        
        # Document type bonus (0-50 points)
        doc_types = analysis.document_types
        if "legal_contract" in doc_types:
            base_score += 50
        elif "financial_document" in doc_types:
            base_score += 40
        elif "identification" in doc_types:
            base_score += 35
        elif "property_document" in doc_types:
            base_score += 30
        elif any(doc in doc_types for doc in ["pdf", "doc", "docx"]):
            base_score += 20
            
        # Document complexity bonus (0-25 points)
        if analysis.document_page_count > 10:
            base_score += 25
        elif analysis.document_page_count > 5:
            base_score += 15
        elif analysis.document_page_count > 1:
            base_score += 10
            
        # OCR confidence bonus (0-15 points) 
        if analysis.requires_ocr and analysis.image_quality == "high":
            base_score += 15
        elif analysis.requires_ocr and analysis.image_quality == "medium":
            base_score += 10
            
        # Legal analysis requirement bonus (0-20 points)
        if analysis.requires_legal_analysis:
            base_score += 20
        elif analysis.requires_contract_review:
            base_score += 15
            
        # Current load penalty (0-15 points)
        load_penalty = self._current_load_penalty()
        
        return min(100, base_score - load_penalty)
```

## 🛠️ Configuración Bird.com

### **1. Personalidad del Agente**

#### **Configuración de Personalidad en Bird.com**
```
Nombre: UrbanHub Document Specialist
Descripción: Especialista en análisis inteligente de documentos inmobiliarios

PERSONALIDAD PRINCIPAL:
- Especialista técnico en documentación legal e inmobiliaria
- Meticuloso y preciso en el análisis de contratos y documentos oficiales
- Comunicación clara sobre términos legales y implicaciones importantes
- Proactivo en identificar puntos críticos y áreas de atención
- Confiable para validación de documentos sensibles y confidenciales

TONO Y ESTILO:
- Profesional y técnicamente preciso
- Explicaciones claras de términos legales complejos
- Structured responses con puntos clave destacados
- Proactivo en señalar discrepancias o áreas de riesgo
- Empático al explicar procesos burocráticos complejos

ESPECIALIZACIÓN TÉCNICA:
- OCR avanzado para documentos escaneados y fotografiados
- Análisis automático de contratos de arrendamiento y compraventa
- Extracción inteligente de datos financieros y personales
- Verificación de autenticidad y validez de documentos oficiales
- Identificación de cláusulas problemáticas o inusuales
```

#### **Restricciones y Guardrails**
```
RESTRICCIONES ESPECÍFICAS:
- NUNCA almacenar o retener documentos personales después del análisis
- SIEMPRE redactar información personal identificable en logs
- NO proporcionar asesoría legal específica - solo análisis informativo
- SIEMPRE recomendar revisión legal profesional para decisiones importantes
- NUNCA procesar documentos sin consentimiento explícito del usuario

PROTOCOLO DE SEGURIDAD:
1. Validar legitimidad del documento antes de procesamiento completo
2. Enmascarar PII automáticamente en todas las respuestas
3. Detectar y reportar documentos potencialmente fraudulentos
4. Escalación inmediata para documentos con irregularidades legales serias
5. Eliminación automática de datos procesados después de 24h

LÍMITES OPERACIONALES:
- Máximo 50 páginas por documento para procesamiento completo
- Tipos soportados: PDF, JPG, PNG, DOC, DOCX
- Idiomas: Español (México), Inglés (US/Internacional)
- Resolución mínima: 150 DPI para OCR óptimo
- Tiempo máximo procesamiento: 45 segundos por documento
```

### **2. Base de Conocimiento Especializada**

#### **Knowledge Base: Document Processing Expertise**
```
=== TIPOS DE DOCUMENTOS INMOBILIARIOS ===

## Contratos de Arrendamiento
ELEMENTOS_CLAVE:
- partes: [arrendador, arrendatario, avalistas]
- propiedad: [dirección, descripción, metros²]
- términos: [duración, renta, incrementos, depósito]
- cláusulas_especiales: [mascotas, modificaciones, subarriendo]
- obligaciones: [mantenimiento, servicios, seguros]

PUNTOS_CRÍTICOS:
- ⚠️ Incrementos automáticos > 10% anual
- ⚠️ Cláusulas de terminación unilateral  
- ⚠️ Depósitos excesivos (>2 meses renta)
- ⚠️ Restricciones de uso poco claras
- ⚠️ Responsabilidades mantenimiento ambiguas

## Contratos de Compraventa
ELEMENTOS_CLAVE:
- partes: [vendedor, comprador, notario]
- propiedad: [descripción_legal, linderos, servicios]
- precio: [cantidad, forma_pago, financiamiento] 
- condiciones: [entrega, posesión, gravámenes]
- documentos: [escrituras, certificados, permisos]

SEÑALES_ALERTA:
- 🚨 Precios significativamente bajo mercado
- 🚨 Gravámenes o limitaciones no declaradas
- 🚨 Problemas con escrituración o títulos
- 🚨 Condiciones de pago inusuales
- 🚨 Falta documentos oficiales requeridos

## Documentos Financieros
TIPOS_ACEPTADOS:
- estados_cuenta: [3-6 meses recientes]
- comprobantes_ingresos: [nómina, honorarios, rentas]
- declaraciones_fiscales: [últimos 2 ejercicios]
- constancias_laborales: [antigüedad, salario]
- estados_financieros: [empresas, personas_morales]

VALIDACIONES:
- ✅ Consistencia fechas y montos
- ✅ Sellos y firmas oficiales
- ✅ Correlación entre documentos  
- ✅ Capacidad pago vs solicitud
- ✅ Estabilidad ingresos demostrada

## Documentos de Identidad
TIPOS_VÁLIDOS:
- INE/IFE vigente (México)
- pasaporte_mexicano válido
- cédula_profesional oficial
- licencia_manejo vigente
- residencia_temporal/permanente (extranjeros)

PUNTOS_VERIFICACIÓN:
- ✓ Vigencia documento
- ✓ Calidad fotografía legible
- ✓ Datos consistentes con solicitud
- ✓ Ausencia alteraciones visibles
- ✓ Formato oficial correcto

=== PATRONES DE ANÁLISIS OCR ===

## Técnicas de Extracción
TEXTO_ESTRUCTURADO:
- tablas: usar coordenadas y patrones de alineación
- formularios: identificar campos por etiquetas
- párrafos: análisis de contexto y referencias cruzadas
- firmas: detección de elementos gráficos vs texto

TEXTO_NO_ESTRUCTURADO:
- contratos: búsqueda por palabras clave y contexto
- cartas: extracción de fechas, nombres y compromisos
- reportes: identificación de secciones y conclusiones
- correspondencia: clasificación por tipo e importancia

## Validación de Calidad
CRITERIOS_ACEPTACIÓN:
- legibilidad: >95% caracteres reconocidos correctamente
- completitud: <5% contenido faltante o ilegible  
- estructura: preservación formato y relaciones
- precisión: validación cruzada elementos críticos

CRITERIOS_RECHAZO:
- calidad_insuficiente: <90% confidence OCR
- documentos_incompletos: páginas faltantes detectadas
- alteraciones_evidentes: inconsistencias visuales
- formato_no_soportado: tipos de archivo incompatibles

=== PROTOCOLOS DE ANÁLISIS LEGAL ===

## Análisis Automático de Cláusulas
CLÁUSULAS_ESTÁNDAR:
- vigencia: fechas inicio/fin, renovación automática
- pagos: montos, fechas, penalizaciones, incrementos  
- obligaciones: mantenimiento, servicios, modificaciones
- terminación: causales, avisos, procedimientos

CLÁUSULAS_PROBLEMÁTICAS:
- 🚨 Penalizaciones excesivas (>20% renta mensual)
- 🚨 Incrementos automáticos sin límites
- 🚨 Cláusulas de exclusión de responsabilidad amplias
- 🚨 Restricciones de uso excesivamente limitantes
- 🚨 Procedimientos terminación unilaterales

## Extracción de Datos Críticos
INFORMACIÓN_FINANCIERA:
- montos: renta, depósito, comisiones, seguros
- fechas: vencimientos, incrementos, revisiones
- condiciones: descuentos, bonificaciones, penalizaciones  
- referencias: cuentas, instituciones, garantías

INFORMACIÓN_LEGAL:
- jurisdicción: competencia, ley aplicable
- resolución_conflictos: mediación, arbitraje, tribunales
- notificaciones: domicilios, medios, plazos
- modificaciones: procedimientos, autorizaciones

=== REPORTES DE ANÁLISIS ===

## Formato de Reporte Estándar
RESUMEN_EJECUTIVO:
- tipo_documento: clasificación y propósito
- partes_involucradas: nombres y roles principales
- términos_principales: condiciones más relevantes
- puntos_atención: elementos que requieren revisión
- recomendaciones: acciones sugeridas próximos pasos

ANÁLISIS_DETALLADO:
- sección_por_sección: desglose completo contenido
- cláusulas_importantes: explicación términos clave
- riesgos_identificados: potenciales problemas detectados
- cumplimiento_normativo: validación vs regulaciones
- comparación_estándares: vs prácticas de mercado

## Clasificación de Riesgo
BAJO_RIESGO: ✅
- Documentos estándar de mercado
- Términos equilibrados entre partes
- Cumplimiento normativo completo
- Información completa y consistente

MEDIO_RIESGO: ⚠️
- Cláusulas ligeramente favorables a una parte
- Algunos términos ambiguos o poco claros  
- Información faltante no crítica
- Cumplimiento normativo con observaciones menores

ALTO_RIESGO: 🚨
- Términos significativamente desequilibrados
- Cláusulas potencialmente abusivas
- Información crítica faltante o inconsistente
- Posibles violaciones normativas
- RECOMENDACIÓN: Revisión legal profesional obligatoria
```

### **3. AI Actions Especializadas**

#### **AI Action 1: Advanced OCR Processor**
```
Nombre: process_document_ocr
Descripción: Procesamiento OCR avanzado con validación de calidad y extracción estructurada

TRIGGER CONDITIONS:
- Usuario envía documento imagen (JPG, PNG)
- Usuario sube archivo PDF escaneado
- Calidad documento requiere OCR para procesamiento
- Documento contiene texto no seleccionable

PROCESSING PIPELINE:
1. QUALITY_ASSESSMENT:
   - Evaluar resolución, contraste, orientación
   - Detectar páginas múltiples vs documento simple
   - Identificar idioma predominante (ES/EN)
   - Calcular confidence_score esperado

2. OCR_OPTIMIZATION:
   - Aplicar pre-procesamiento según tipo documento
   - Ajustar parámetros OCR para idioma detectado
   - Utilizar AWS Textract con configuración optimizada
   - Ejecutar post-procesamiento para mejora precisión

3. STRUCTURE_RECOGNITION:
   - Identificar elementos estructurales (tablas, formularios)
   - Detectar campos clave por posición y contexto
   - Preservar relaciones espaciales críticas
   - Generar mapa de contenido estructurado

4. VALIDATION_CHECKS:
   - Verificar completitud de extracción
   - Validar consistencia datos extraídos
   - Detectar posibles errores OCR críticos
   - Generar confidence_score por sección

OUTPUT FORMAT:
{
  "ocr_quality": 96.5,
  "text_extracted": "...",
  "structured_data": {
    "tables": [...],
    "forms": [...], 
    "signatures": [...]
  },
  "identified_issues": ["minor_smudge_page_3"],
  "confidence_by_section": {"header": 98, "body": 95, "footer": 92},
  "processing_notes": "High quality scan, excellent extraction"
}
```

#### **AI Action 2: Legal Document Analyzer**
```
Nombre: analyze_legal_document
Descripción: Análisis automático de documentos legales con extracción de cláusulas y evaluación de riesgos

TRIGGER CONDITIONS:
- Documento clasificado como contrato legal
- Usuario solicita análisis de términos específicos
- Detección de documento con implicaciones legales
- Requerimiento de extracción de cláusulas clave

ANALYSIS_COMPONENTS:

1. DOCUMENT_CLASSIFICATION:
   - Tipo: contrato_arrendamiento/compraventa/otros
   - Jurisdicción: identificar ley aplicable
   - Partes: extraer nombres y roles
   - Objeto: identificar propiedad o servicio específico

2. CLAUSE_EXTRACTION:
   - Términos_principales: duración, montos, condiciones
   - Obligaciones: responsabilidades cada parte
   - Penalizaciones: multas, intereses, terminación
   - Especiales: cláusulas no estándar identificadas

3. RISK_ASSESSMENT:
   - Cláusulas_desequilibradas: favorecen excesivamente una parte
   - Términos_ambiguos: redacción poco clara o interpretable
   - Penalizaciones_excesivas: multas/intereses sobre mercado
   - Vacíos_legales: ausencia protecciones estándar

4. COMPLIANCE_CHECK:
   - Normatividad_aplicable: leyes federales/locales relevantes
   - Requisitos_mínimos: validar cumplimiento básico
   - Protecciones_consumidor: verificar inclusión obligatoria
   - Formalidades: elementos requeridos presentes

RISK_CLASSIFICATION:
- VERDE (0-30): Documento estándar, riesgo mínimo
- AMARILLO (31-60): Algunos puntos requieren atención
- ROJO (61-100): Riesgos significativos, revisión legal recomendada

OUTPUT:
{
  "document_type": "contrato_arrendamiento_residencial",
  "parties": ["Juan Pérez [Arrendador]", "María González [Arrendataria]"],
  "key_terms": {
    "rent": "$15,000 MXN mensuales",
    "duration": "12 meses con renovación automática", 
    "deposit": "$30,000 MXN (2 meses)"
  },
  "risk_score": 45,
  "risk_level": "AMARILLO",
  "concerns": [
    "Incremento anual 15% (sobre mercado típico 8-10%)",
    "Cláusula terminación permite desalojo con 15 días"
  ],
  "recommendations": [
    "Negociar incremento máximo 10% anual",
    "Extender periodo aviso desalojo a 30 días",
    "Revisar con abogado antes de firmar"
  ]
}
```

#### **AI Action 3: Document Classification & Routing**
```
Nombre: classify_and_route_document
Descripción: Clasificación inteligente de documentos y routing a especialistas según tipo identificado

TRIGGER CONDITIONS:
- Documento subido sin especificación de tipo
- Necesidad de procesamiento especializado según clasificación
- Múltiples documentos requieren categorización automática
- Workflow de procesamiento debe determinarse automáticamente

CLASSIFICATION_ALGORITHM:

1. INITIAL_ANALYSIS:
   - Examinar metadatos: nombre_archivo, tamaño, formato
   - OCR rápido: extraer primeras líneas y palabras clave
   - Pattern_recognition: identificar layouts típicos
   - Language_detection: confirmar idioma principal

2. CONTENT_CLASSIFICATION:
   - Legal_documents: contratos, acuerdos, escrituras
   - Financial_documents: estados cuenta, comprobantes ingresos  
   - Identity_documents: INE, pasaportes, cédulas
   - Property_documents: avalúos, planos, permisos
   - Other_documents: correspondencia, reportes, certificados

3. SPECIALIZATION_MAPPING:
   - Contratos_complejos → Full legal analysis required
   - Documentos_financieros → Financial validation workflow
   - Identificaciones → Identity verification process
   - Documentos_propiedad → Property analysis specialist
   - Otros → General document processing

4. ROUTING_DECISION:
   - Self_processing: document within agent capabilities
   - Specialist_handoff: requires specific expertise
   - Human_escalation: complex legal/compliance issues
   - Batch_processing: multiple similar documents

CONFIDENCE_LEVELS:
- HIGH (90-100%): Procesamiento automático completo
- MEDIUM (70-89%): Procesamiento con validación adicional
- LOW (<70%): Confirmación manual clasificación

OUTPUT:
{
  "document_classification": {
    "primary_type": "contrato_arrendamiento",
    "secondary_type": "residencial_individual", 
    "confidence": 94,
    "identified_patterns": ["formato_estándar_cdmx", "cláusulas_típicas"]
  },
  "processing_route": {
    "recommended_action": "full_legal_analysis",
    "estimated_time": "3-5 minutos",
    "required_validations": ["signature_verification", "clause_extraction"],
    "escalation_triggers": ["unusual_terms", "compliance_issues"]
  },
  "next_steps": [
    "Ejecutar análisis legal completo",
    "Generar reporte riesgo",
    "Presentar resumen al usuario",
    "Ofrecer opciones revisión adicional"
  ]
}
```

## 📊 KPIs y Métricas de Rendimiento

### **Métricas Técnicas**

#### **Procesamiento OCR**
- **OCR Accuracy**: > 98% para documentos calidad alta
- **Processing Speed**: < 30 segundos por documento < 10 páginas
- **Language Detection**: > 99% accuracy español/inglés  
- **Structure Recognition**: > 95% identificación correcta tablas/formularios

#### **Análisis Legal**
- **Clause Extraction**: > 92% completitud términos principales
- **Risk Assessment**: > 88% correlation con revisión legal profesional
- **Classification Accuracy**: > 94% tipo documento correcto
- **Compliance Detection**: > 96% identificación violaciones normativas

### **Métricas de Negocio**

#### **Eficiencia Operacional**
- **Automation Rate**: > 85% documentos procesados sin intervención humana
- **Processing Cost**: < $2 USD por documento promedio
- **Time Savings**: > 75% reducción vs revisión manual
- **Error Reduction**: > 90% menos errores vs entrada manual

#### **Satisfacción Usuario**
- **Processing Accuracy**: > 4.7/5 según feedback usuarios  
- **Speed Satisfaction**: > 4.8/5 tiempo respuesta
- **Completeness**: > 4.6/5 información extraída suficiente
- **Clarity**: > 4.5/5 explicaciones comprensibles

## 🧪 Escenarios de Testing

### **Test 1: Contrato Arrendamiento Estándar**
```
SCENARIO: "Procesamiento Contrato Typical"

INPUT:
- PDF contrato arrendamiento 8 páginas
- Calidad: alta resolución, texto seleccionable
- Tipo: residencial individual CDMX
- Contenido: términos estándar mercado

EXPECTED_BEHAVIOR:
1. Clasificar correctamente como "contrato_arrendamiento_residencial"
2. Extraer todos términos principales (renta, duración, depósito, partes)
3. Identificar cláusulas estándar vs inusuales
4. Generar análisis de riesgo VERDE o AMARILLO
5. Proporcionar resumen ejecutivo claro

VALIDATION:
- ✅ Clasificación correcta tipo documento
- ✅ Extracción completa términos clave (>95% accuracy)
- ✅ Identificación correcta nivel riesgo
- ✅ Resumen ejecutivo incluye puntos más relevantes
- ✅ Tiempo procesamiento < 45 segundos
```

### **Test 2: Documento Financiero Complejo**
```
SCENARIO: "Estados Financieros Empresariales"

INPUT:
- PDF estados financieros empresa 25 páginas
- Calidad: escaneado OCR requerido
- Contenido: balance general, estado resultados, flujo efectivo
- Información: 3 años datos comparativos

EXPECTED_BEHAVIOR:
1. OCR completo con quality_score > 95%
2. Identificar secciones financieras principales
3. Extraer métricas clave por año
4. Validar consistencia entre documentos
5. Generar análisis capacidad de pago

VALIDATION:
- ✅ OCR accuracy > 98% en cifras críticas
- ✅ Identificación correcta 3 secciones principales
- ✅ Extracción datos 3 años completa
- ✅ Detección inconsistencias si existen
- ✅ Análisis financiero básico generado
```

### **Test 3: Documento con Calidad Deficiente**
```
SCENARIO: "OCR Challenging - Foto Mobile"

INPUT:
- Imagen JPG tomada con celular
- Calidad: resolución media, iluminación desigual
- Tipo: INE fotografiada desde múltiples ángulos
- Condición: algunas secciones parcialmente borrosas

EXPECTED_BEHAVIOR:
1. Detectar calidad subóptima automáticamente
2. Aplicar pre-procesamiento mejorar legibilidad
3. Ejecutar OCR con parámetros optimizados
4. Identificar secciones con low confidence
5. Solicitar re-envío de áreas problemáticas

VALIDATION:
- ✅ Detección automática quality issues
- ✅ OCR extrae información legible disponible
- ✅ Identificación específica áreas problemáticas  
- ✅ Solicitud específica mejoras requeridas
- ✅ Procesamiento parcial mejor que rechazo total
```

---

## 📚 Integración con Ecosystem UrbanHub

### **Coordinación con Orchestrator**
- **Bid Calculation**: Score máximo para documentos legales/financieros
- **Specialization Handoff**: Recibe documentos clasificados como complejos
- **Quality Gateway**: Validación final antes de entrega a usuario

### **Colaboración con Otros Agentes**
- **Multimodal Conversation AI**: Colaboración análisis documentos + contexto conversacional
- **Visual Property Assistant**: Handoff documentos con planos o imágenes propiedades
- **Voice Tour Guide**: Procesamiento contratos para tours personalizados

### **Data Integration**
- **S3 Document Storage**: Almacenamiento seguro documentos procesados
- **DynamoDB Metadata**: Índices búsqueda y clasificación documentos
- **OpenSearch Legal**: Knowledge base cláusulas y términos legales

---

**📄 Document Intelligence Agent - Procesamiento Avanzado Legal e Inmobiliario**  
📅 Implementación: UrbanHub v2.0  
🔄 Optimizado con: AWS Textract + Bedrock Claude + LangChain  
📊 Última actualización: 2025-09-01