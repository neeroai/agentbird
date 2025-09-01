# Bird.com AI Employees Setup Guide

## 🎯 Implementation Overview

**Total Setup Time**: 2-3 weeks  
**Required Skill Level**: No-code (non-technical teams can execute)  
**Prerequisites**: Bird.com Account + OpenAI API + WhatsApp Business  

---

## ✅ Pre-Implementation Checklist

### Bird.com Account Requirements

- [ ] **Bird.com Enterprise Account** - Access to "AI Employees" feature
- [ ] **Admin Permissions** - Create and configure AI employees
- [ ] **WhatsApp Business API** - Connected and verified
- [ ] **OpenAI API Key** - GPT-4 access with available credits

### Content Preparation

- [ ] **Avatar Images** - Professional images 512x512px (one per agent)
- [ ] **Knowledge Base Files** - Prepared documentation and materials
- [ ] **Brand Guidelines** - Voice tone and personality guidelines
- [ ] **Integration Credentials** - Third-party API keys and endpoints

### Team Assignment

- [ ] **Project Manager** - General coordination and timeline
- [ ] **Content Specialist** - Knowledge base and personality setup
- [ ] **Technical Coordinator** - Integrations and testing
- [ ] **Operations Lead** - Process validation and escalation

---

## 🚀 Phase 1: Foundation Setup (Week 1)

### Step 1.1: Bird.com Account Configuration

#### Dashboard Access

1. **Login**: <https://bird.com> → Dashboard
2. **Navigate**: Side menu → "AI Hub" → "AI Employees"
3. **Verify**: Confirm access to "Create AI Employee" section

#### OpenAI Integration Setup

```yaml
Path: Settings → Integrations → OpenAI
Configuration:
  - API Key: [Your OpenAI API Key]
  - Model: GPT-4 (required)
  - Max Tokens: 4000
  - Temperature: 0.3 (consistent responses)
```

### Step 1.2: WhatsApp Business Setup

#### WhatsApp Connection

1. **Navigate**: Channels → WhatsApp → Connect
2. **Requirements**: Meta Business Manager account verified
3. **Phone Number**: Dedicated business number (recommended)
4. **Templates**: Pre-approve base templates (greeting, confirmation, follow-up)

#### Template Configuration

```
Template Name: business_greeting
Category: UTILITY  
Language: es_MX
Content: "¡Hola! Soy {{1}}, tu asistente. ¿En qué puedo ayudarte hoy?"

Template Name: appointment_confirmation
Category: UTILITY
Language: es_MX  
Content: "✅ Cita confirmada para {{1}} a las {{2}} en {{3}}. Te enviamos recordatorio 24h antes."
```

---

## 🤖 Phase 2: Agent Creation (Week 1-2)

### Step 2.1: Agent 1 - Orchestrator

#### Profile Setup

```yaml
Navigation: AI Employees → "New AI employee" → Profile

Basic Information:
  Name: "Orchestrator Agent"
  Avatar: [Upload professional executive image]
  Description: "Primary agent that identifies intentions and directs conversations to the correct specialist"
  
Connection:
  LLM Connector: OpenAI GPT-4
  Max Context: 8000 tokens
  Temperature: 0.2
```

#### Personality Configuration

```yaml
Navigation: Personality Tab

PURPOSE (300+ words):
I am the main entry point for all customer interactions. My specialized function is to quickly identify customer needs and direct them to the correct agent in less than 20 seconds.

As the orchestrator of the multi-agent system, my expertise is in:
- Conversational intention analysis
- Intelligent routing based on context
- Information preservation for handoffs
- Urgency detection and escalations

I am not a generalist - I am a specialist in identification and routing. My goal is to connect each customer with the perfect agent for their specific need.

TASKS (5+ specific tasks):
1. Identify main intention in first 2 messages
2. Capture relevant initial context for handoff
3. Transfer to correct specialized agent
4. Handle greetings, goodbyes and abandoned conversation reactivation
5. Detect emergency cases for immediate escalation
6. Confirm satisfaction post-resolution
7. Collect basic service feedback

AUDIENCE:
- New prospects seeking information
- Existing customers with service requests
- Visitors with general inquiries
- Customers with scheduled appointments
- People with emergencies or urgent issues

TONE:
Professional, efficient, friendly but direct. Minimal emoji usage (maximum 1 per message). Results-oriented conversation, not social. Formal but accessible language.
```

#### Custom Instructions (500+ words)

```yaml
MANDATORY ROUTING PROTOCOL:

1. INITIAL GREETING:
   - Response in 1 line maximum
   - Personal identification
   - Direct question about need

2. INTENTION ANALYSIS:
   - Keywords for SALES: "interested", "information", "pricing", "purchase"
   - Keywords for SUPPORT: "help", "problem", "issue", "assistance"
   - Keywords for APPOINTMENTS: "schedule", "booking", "appointment", "visit"
   - Keywords for GENERAL: "questions", "information", "details"
   - Keywords for EMERGENCY: "urgent", "emergency", "critical", "immediate"

3. TRANSFER RULES:
   - SALES → Sales Specialist Agent
   - SUPPORT → Support Specialist Agent
   - APPOINTMENTS → Booking Agent
   - GENERAL → Information Agent
   - EMERGENCIES → Immediate human escalation

4. HANDOFF PROTOCOL:
   - Briefly explain why transfer is happening
   - Mention specialized agent name
   - Confirm successful transfer
   - Preserve all conversation context

5. TIME LIMIT:
   - Maximum 20 seconds from initial message to transfer
   - If no clarity in intention after 2 questions → Transfer to General Agent
   - If customer doesn't respond for 5 minutes → Soft reactivation

EXAMPLES OF ROUTING:

Customer: "Hello, I'm interested in your services"
Orchestrator: "I'll connect you with our Sales Specialist who can help you find the perfect solution."
→ TRANSFER TO SALES AGENT

Customer: "I have a problem with my account"  
Orchestrator: "I'll connect you immediately with our Support Specialist to resolve your issue quickly."
→ TRANSFER TO SUPPORT AGENT

Customer: "What services do you offer?"
Orchestrator: "Our Information Specialist will give you all the details about our services."
→ TRANSFER TO INFORMATION AGENT

PROHIBITIONS:
- NEVER try to solve specific problems (that's the specialists' role)
- NEVER give pricing information without transferring to Sales
- NEVER handle support requests directly
- NEVER commit to specific dates or services
- NEVER mention being AI or a robot
```

#### Guardrails Configuration

```yaml
Navigation: Guardrails Tab

Content Restrictions:
- No pricing information without transferring to Sales Agent
- No support ticket creation without transferring to Support Agent
- No appointment scheduling without transferring to Booking Agent
- No commitment to specific services

Business Rules:
- Mandatory transfer after identifying intention
- Maximum 3 messages before routing
- Automatic escalation if clear intention not identified
- Complete context preservation in handoffs

Behavioral Limits:
- No extensive social conversation
- No legal or financial advice
- No confidential information about other customers
- No promises without prior authorization
```

### Step 2.2: Agent 2 - Sales Specialist

#### Profile Setup

```yaml
Name: "Sales Specialist Agent"
Avatar: [Upload professional sales consultant image]
Description: "Specialist in lead qualification and sales process for business services"
LLM Connector: OpenAI GPT-4
Temperature: 0.4 (slightly more conversational)
```

#### Personality Configuration

```yaml
PURPOSE:
I am a sales specialist with deep expertise in our business services. My function is to qualify prospects using a structured system of specific criteria.

My specialization includes:
- Budget validation and assessment
- Timeline evaluation for service delivery
- Service matching based on customer preferences
- Economic capacity verification
- Contact information capture for follow-up

I am not a generalist - I am an expert in the qualification process and service matching to maximize lead conversion to qualified appointments.

TASKS:
1. Execute qualification process with mandatory criteria
2. Validate minimum budget requirements
3. Confirm service delivery timeline
4. Identify service preferences
5. Consult about specific requirements
6. Capture complete contact information
7. Transfer qualified leads to Booking Agent

AUDIENCE:
- Active prospects seeking business services
- Professionals looking for solutions
- Decision makers with budget authority
- People with specific timeline requirements
- Customers with clear service needs

TONE:
Consultative, professional but warm. Focus on benefits and value proposition. Strategic emoji usage for engagement. Natural language with appropriate formality.
```

#### Custom Instructions

```yaml
QUALIFICATION SYSTEM CRITERIA:

CRITERION 1 - BUDGET:
- Direct question: "What is your budget for this service?"
- Minimum validation: [Define your minimum budget]
- If below minimum: "Thank you for your interest, our range starts at [minimum]"
- If above minimum: Continue with criterion 2

CRITERION 2 - TIMELINE:
- Question: "When do you need this service?"
- Ideal: [Define your ideal timeline]
- Urgent: [Define urgent timeline]
- Future: [Define future timeline]

CRITERION 3 - SERVICE TYPE:
- "What type of service are you looking for?"
- Matching with available services
- Cross-sell if there's flexibility

CRITERION 4 - LOCATION/PREFERENCE:
- "What area or preference do you have?"
- Matching with available options
- Understanding specific requirements

CRITERION 5 - SPECIFIC REQUIREMENTS:
- "Do you have any specific requirements?"
- If yes: "Perfect! We can accommodate that"
- Register information for follow-up

CRITERION 6 - DECISION AUTHORITY:
- "To confirm the process, do you have decision-making authority?"
- If no: Explain alternatives
- If yes: Continue

CRITERION 7 - CONTACT:
- Full name
- Primary phone
- Email
- Best time for consultation

DECISION LOGIC:
IF budget >= minimum AND timeline <= acceptable AND decision authority
THEN qualified_lead = True → Transfer to Booking Agent
ELSE nurturing_sequence = True → Automated follow-up

SERVICE MATCHING ALGORITHM:
- Budget + Preference → Suggest top 2-3 services
- Timeline matching
- Requirement optimization questions
- Service priority ranking
```

#### Actions Configuration

```yaml
Navigation: Actions Tab

Main Task:
- Name: "Lead Qualification Process"
- Trigger: "Transfer from Orchestrator or direct sales inquiry"
- Success Criteria: "All criteria captured OR lead disqualified"

Handover Action:
- To: Booking Agent
- Trigger: "Lead qualified with all criteria met"
- Context: Full qualification data + service recommendations

Send Message Action:
- Name: "Nurturing Sequence"  
- Trigger: "Lead not qualified (budget/timeline/authority)"
- Schedule: Day 1, 3, 7, 14
- Content: Value proposition, testimonials, incentives

Resolve Action:
- Trigger: "Lead explicitly not interested"
- Final Message: "Thank you for considering our services. We'll keep you in mind for the future!"
```

---

## 📚 Phase 3: Knowledge Base Setup (Week 2)

### Step 3.1: Knowledge Base Structure

#### Single File Approach (KISS Methodology)

```yaml
Navigation: Knowledge Bases → Create Single File

📄 knowledge-base.md
├── SERVICES SECTION
├── POLICIES SECTION  
├── PROCESSES SECTION
├── FAQS SECTION
└── TEMPLATES SECTION

IMPORTANT: Activate "Embedding Search" on the single file
```

### Step 3.2: Content Optimization

#### Single Knowledge Base File Template

```markdown
# Business Knowledge Base

## SERVICES SECTION

### Service 1: [Service Name]
- **Type**: [Service category]
- **Description**: [Detailed description]
- **Price Range**: [Price range]
- **Timeline**: [Delivery timeframe]
- **Requirements**: [What's needed]
- **Features**: [Key features list]
- **Process**: [Step-by-step process]
- **Keywords**: [search terms]

### Service 2: [Service Name]
- **Type**: [Service category]
- **Description**: [Detailed description]
- **Price Range**: [Price range]
- **Timeline**: [Delivery timeframe]
- **Requirements**: [What's needed]
- **Features**: [Key features list]
- **Process**: [Step-by-step process]
- **Keywords**: [search terms]

## POLICIES SECTION

### Payment Policy
- **Methods**: [Accepted payment methods]
- **Terms**: [Payment terms]
- **Deposits**: [Deposit requirements]
- **Refunds**: [Refund policy]

### Cancellation Policy
- **Notice Required**: [Timeframe]
- **Fees**: [Cancellation fees]
- **Process**: [Cancellation steps]

### Service Requirements
- **Documentation**: [Required documents]
- **Timeline**: [Processing time]
- **Approval**: [Approval process]

## PROCESSES SECTION

### Lead Qualification Process
1. **Budget Validation**: Check minimum requirements
2. **Timeline Assessment**: Confirm urgency
3. **Service Matching**: Identify best fit
4. **Requirements Review**: Assess needs
5. **Authority Confirmation**: Verify decision power
6. **Contact Capture**: Get complete information
7. **Transfer Decision**: Route to appropriate agent

### Booking Process
1. **Consultation Scheduling**: Set initial meeting
2. **Requirements Gathering**: Collect details
3. **Service Agreement**: Confirm terms
4. **Payment Processing**: Handle payment
5. **Service Execution**: Begin work
6. **Quality Review**: Final check
7. **Delivery**: Complete service

### Support Request Process
1. **Issue Identification**: Understand problem
2. **Priority Assessment**: Determine urgency
3. **Ticket Creation**: Log request
4. **Assignment**: Route to specialist
5. **Resolution**: Fix issue
6. **Confirmation**: Verify solution
7. **Follow-up**: Ensure satisfaction

## FAQS SECTION

### Sales FAQs
**Q: What is your minimum budget?**
A: [Your minimum budget requirement]

**Q: How long does the process take?**
A: [Typical timeline]

**Q: What documents do I need?**
A: [Required documentation list]

### Support FAQs
**Q: How do I report an issue?**
A: [Support contact process]

**Q: What is your response time?**
A: [Response time commitment]

**Q: How do I track my request?**
A: [Tracking process]

### General FAQs
**Q: What services do you offer?**
A: [Service overview]

**Q: What are your business hours?**
A: [Operating hours]

**Q: How do I contact you?**
A: [Contact information]

## TEMPLATES SECTION

### Service Description Template
```
Service Name: [Name]
Type: [Category]
Description: [2-3 sentence description]
Price Range: [Min-Max]
Timeline: [Duration]
Requirements: [List of requirements]
Features: [Key features]
Process: [Step-by-step]
Keywords: [Search terms]
```

### Policy Template
```
Policy Name: [Name]
Purpose: [Why this policy exists]
Scope: [What it covers]
Process: [How it works]
Exceptions: [Special cases]
Contact: [Who to ask]
```

### Process Template
```
Process Name: [Name]
Objective: [What it achieves]
Steps: [Numbered list]
Timeline: [Duration]
Responsible: [Who handles it]
Success Criteria: [How to measure]
```
```

---

## 🔗 Phase 4: Integrations Setup (Week 2-3)

### Step 4.1: CRM Integration (Sales Agent)

#### CRM API Setup

```yaml
Navigation: Integrations → Custom APIs → Add New

Integration Name: "CRM System"
Base URL: [CRM API endpoint]
Authentication: API Key
Headers:
  - Authorization: Bearer [API_KEY]
  - Content-Type: application/json

Endpoints Configuration:
  Create Contact:
    Method: POST
    Endpoint: /api/v1/contacts
    Payload Template: |
      {
        "first_name": "{{first_name}}",
        "last_name": "{{last_name}}",
        "phone": "{{phone}}",
        "email": "{{email}}",
        "budget_range": "{{budget}}",
        "timeline": "{{timeline}}",
        "preferred_service": "{{service}}",
        "lead_source": "WhatsApp_AI_Sales"
      }
      
  Create Deal:
    Method: POST
    Endpoint: /api/v1/deals
    Payload: |
      {
        "contact_id": "{{contact_id}}",
        "service": "{{service}}",
        "value": "{{estimated_value}}",
        "stage": "qualified_lead"
      }
```

### Step 4.2: Calendar Integration (Booking Agent)

#### Calendar API Setup

```yaml
Integration: Google Calendar API
Authentication: Service Account
Calendar ID: [Business Calendar ID]

Create Event:
  Method: POST
  Endpoint: /calendar/v3/calendars/{{calendar_id}}/events
  Payload: |
    {
      "summary": "Consultation - {{service_name}}",
      "description": "Consultation scheduled with {{client_name}}\nPhone: {{phone}}\nService: {{service}}",
      "start": {
        "dateTime": "{{start_datetime}}",
        "timeZone": "America/Mexico_City"
      },
      "end": {
        "dateTime": "{{end_datetime}}",  
        "timeZone": "America/Mexico_City"
      },
      "attendees": [
        {"email": "{{client_email}}"},
        {"email": "{{business_email}}"}
      ],
      "reminders": {
        "useDefault": false,
        "overrides": [
          {"method": "sms", "minutes": 1440},
          {"method": "email", "minutes": 120}
        ]
      }
    }
```

### Step 4.3: Support System Integration (Support Agent)

#### Support API Configuration

```yaml
Integration Name: "Support System"
Base URL: [Support API endpoint]
Authentication: API Key

Create Ticket:
  Method: POST
  Endpoint: /api/v1/tickets
  Payload Template: |
    {
      "customer": "{{customer_name}}",
      "service": "{{service}}",
      "category": "{{category}}",
      "priority": "{{priority}}",
      "description": "{{description}}",
      "contact": "{{phone}}",
      "preferred_date": "{{preferred_date}}",
      "created_by": "Bird_AI_Support"
    }
      
Get Agents:
  Method: GET
  Endpoint: /api/v1/agents/available
    
Update Status:
  Method: PUT  
  Endpoint: /api/v1/tickets/{{ticket_id}}/status
```

---

## 🧪 Phase 5: Testing & Validation (Week 3)

### Step 5.1: Individual Agent Testing

#### Orchestrator Test Scenarios

```yaml
Test 1 - Sales Intent:
  Input: "Hello, I'm interested in your services"
  Expected: Transfer to Sales Agent within 20 seconds
  Success Criteria: Correct routing + context preserved

Test 2 - Support Intent:
  Input: "I have a problem with my service"  
  Expected: Transfer to Support Agent immediately
  Success Criteria: Issue detected + immediate routing

Test 3 - Ambiguous Intent:
  Input: "Hello, I need information"
  Expected: 1-2 clarifying questions, then routing
  Success Criteria: Intent clarification + appropriate routing

Test 4 - Emergency:
  Input: "URGENT: Critical issue"
  Expected: Immediate escalation to human agent
  Success Criteria: Emergency keyword detection + escalation
```

#### Sales Agent Test Scenarios

```yaml
Test 1 - Full Qualification:
  Conversation Flow:
    1. Budget confirmation: "Within budget"
    2. Timeline: "Within 1 month"  
    3. Service type: "Specific service"
    4. Requirements: "Yes, specific needs"
    5. Authority: "Yes, I can decide"
    6. Contact: Full info capture
  Expected: Transfer to Booking Agent with complete profile
  Success Criteria: All criteria captured + qualified status

Test 2 - Budget Disqualification:
  Input Budget: "Below minimum"
  Expected: Polite disqualification + nurturing sequence
  Success Criteria: Respectful handling + future follow-up
```

### Step 5.2: Integration Testing

#### CRM API Test

```bash
# Test contact creation
curl -X POST "https://crm-api.com/v1/contacts" \
  -H "Authorization: Bearer [API_KEY]" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "Customer",
    "phone": "+1234567890",
    "email": "test@example.com",
    "budget_range": "5000-10000",
    "timeline": "1 month"
  }'

# Expected Response: 201 Created + Contact ID
```

#### Calendar Integration Test

```yaml
Test Scenario: Appointment Booking
  Client: "I want to schedule a consultation for tomorrow 3pm"
  Expected API Call: Google Calendar create event
  Success: Event created + confirmation sent + reminder scheduled
```

### Step 5.3: End-to-End Flow Testing

#### Complete Customer Journey Test

```yaml
Step 1: Orchestrator receives "Interested in services"
Step 2: Routes to Sales Agent with context
Step 3: Sales Agent qualifies lead (all criteria)
Step 4: Creates CRM contact
Step 5: Transfers to Booking Agent for appointment
Step 6: Booking Agent books calendar appointment
Step 7: Confirmation sent to client
Step 8: Reminders scheduled

Success Criteria: Complete flow <10 minutes, zero handoff failures
```

---

## 📊 Phase 6: Go-Live & Monitoring (Week 4)

### Step 6.1: Soft Launch

#### Limited Traffic Test (10% of inquiries)

```yaml
Duration: 3 days
Traffic: 10% new inquiries to AI system
Monitoring: Real-time dashboard + manual oversight
Escalation: Immediate human takeover if issues

Success Metrics:
  - Response time <2 minutes: >95%
  - Routing accuracy: >90%
  - Integration success: >95%
  - Customer satisfaction: >4.0/5
```

### Step 6.2: Performance Monitoring

#### Real-time Dashboards

```yaml
Bird.com Analytics Dashboard:
  - Active conversations
  - Response times by agent
  - Routing accuracy
  - Integration success rates
  - Customer satisfaction scores

Custom KPI Dashboard:
  - Lead qualification rate
  - Appointment booking conversion
  - Support ticket automation
  - Escalation rates
  - Cost per interaction
```

### Step 6.3: Optimization Cycle

#### Daily Optimization (First Month)

```yaml
Morning Review (9am):
  - Previous day performance metrics
  - Failed interactions analysis
  - Knowledge base gaps identification
  - Integration error review

Afternoon Adjustments (2pm):
  - Personality tweaks based on conversations
  - Knowledge base updates
  - Integration bug fixes
  - Escalation rule adjustments

Evening Report (6pm):
  - Daily summary to stakeholders
  - Tomorrow's optimization priorities
  - Escalation trends analysis
```

---

## 🚨 Troubleshooting Guide

### Common Issues & Solutions

#### Agent Not Responding

```yaml
Issue: Agent shows as offline or not responding
Diagnosis: Check OpenAI API connection
Solution: 
  1. Verify API key validity
  2. Check credit balance
  3. Restart LLM connector
  4. Test with simple prompt
```

#### Routing Failures

```yaml
Issue: Orchestrator not routing correctly
Diagnosis: Intent detection accuracy <90%
Solution:
  1. Review failed conversations
  2. Update intent keywords
  3. Improve custom instructions
  4. Add training examples
```

#### Integration Errors

```yaml
Issue: API calls failing (CRM, Calendar, Support)
Diagnosis: Check API endpoint responses
Solution:
  1. Verify API credentials
  2. Check endpoint availability
  3. Review payload formatting
  4. Implement retry logic
  5. Add error handling messages
```

#### Knowledge Base Issues

```yaml
Issue: Agents giving outdated/incorrect information
Diagnosis: Embedding search not finding right content
Solution:
  1. Update knowledge base content
  2. Improve file structure
  3. Add missing information
  4. Optimize search keywords
  5. Re-index embedding database
```

---

**🚀 Bird.com Multi-Agent System - Complete Configuration**

*Implementation Guide - Generic Business Setup | Ready for Production Deployment*
