# Claude Code BMad Agent Configuration

This directory contains the Claude Code agent configuration for the BMad-Method framework. The agents have been configured following best practices from Anthropic's research on building effective agents.

## ✅ Configuration Complete

All 9 BMad agents have been successfully converted to Claude Code sub-agent format:

- **`/bmad-master`** - Universal BMad task executor
- **`/dev`** - Expert software engineer (James)
- **`/po`** - Technical product owner (Sarah) 
- **`/pm`** - Product manager (John)
- **`/architect`** - System architect (Winston)
- **`/qa`** - QA architect (Quinn)
- **`/analyst`** - Business analyst (Mary)
- **`/ux-expert`** - UX designer (Sally)
- **`/sm`** - Scrum master (Bob)

## 🛠️ Custom Tools Created

The following custom tools provide access to BMad shared resources:

- **`read_bmad_resource`** - Access templates, tasks, checklists, data, workflows
- **`execute_bmad_task`** - Execute BMad methodology tasks
- **`create_document`** - Create documents using BMad templates
- **`execute_checklist`** - Run validation checklists
- **`shard_document`** - Break large documents into manageable pieces
- **`toggle_kb_mode`** - Access BMad knowledge base

## 🎯 Usage Examples

### Starting a New Project
```bash
# Market research and analysis
/analyst
*brainstorm
*create-project-brief

# Create comprehensive PRD  
/pm
*create-prd

# Design system architecture
/architect
*create-full-stack-architecture

# Validate everything
/po
*execute-checklist-po
```

### Development Workflow
```bash
# Shard large documents for development
/po
*shard-doc docs/prd.md docs/prd

# Create implementation stories
/sm
*draft

# Implement features
/dev
*develop-story

# Quality review
/qa
*review-story
```

### BMad Master (Universal Agent)
```bash
# Access any BMad capability
/bmad-master
*help                    # Show all commands
*kb                      # Knowledge base mode
*task create-next-story  # Execute specific task
*create-doc prd-tmpl     # Create document from template
```

## 📋 Best Practices Applied

### From Anthropic Research
- **Hyper-detailed descriptions** - Each agent has comprehensive 3-4 sentence descriptions
- **XML-structured prompts** - All agent prompts use structured XML tags
- **Read-Plan-Implement-Commit workflow** - Built into dev agent workflow
- **Specialized sub-agents** - Each agent has focused expertise and clear boundaries
- **Tool documentation excellence** - All tools have detailed descriptions and examples

### BMad Methodology Integration
- **Role specialization** - Each agent maintains distinct role and persona
- **Command system preserved** - All BMad `*` prefix commands available
- **Shared resource access** - Full access to templates, tasks, checklists
- **Workflow integration** - Planning → Development phase transitions supported
- **Quality assurance** - Validation checklists and review processes maintained

## 🔧 Technical Architecture

### Agent Definition Structure
```markdown
---
name: agent-name
description: Hyper-detailed description (3-4 sentences)
color: visual-identifier
tools: [list of available tools]
---

# Agent Content with XML Structure
<identity>Agent personality and approach</identity>
<responsibilities>Key duties and expertise</responsibilities>
<commands>Available commands with detailed descriptions</commands>
<principles>Operating principles and rules</principles>
```

### Tool Integration
- **Python-based tools** - All tools implemented as executable Python scripts
- **JSON communication** - Structured input/output using JSON format
- **Error handling** - Comprehensive error handling and user feedback
- **Resource mapping** - Automatic resolution of BMad resource paths

### Shared Resource System
```
.bmad-core/
├── templates/     # YAML document templates (5 files) - Documentation focused
├── tasks/        # Executable workflows (10 files) - Generic processes  
├── checklists/   # Validation checklists (3 files) - Quality assurance
├── data/         # Knowledge base and techniques (3 files) - Methodology
├── agent-teams/  # Team configurations (4 files) - Agent groupings
└── utils/        # Utility resources (2 files) - Support tools
```

## 🚀 Getting Started

1. **Verify installation**:
   ```bash
   python3 .claude/validate_agents.py
   ```

2. **Start with BMad Master**:
   ```bash
   /bmad-master
   *help
   ```

3. **Follow BMad workflows**:
   - **Planning phase**: Use analyst → pm → architect → po
   - **Development phase**: Use po → sm → dev → qa cycles

## 📊 Validation Results

```json
{
  "status": "success",
  "agents_found": 9,
  "tools_found": 6,
  "shared_resources": {
    "templates": 5,
    "tasks": 10, 
    "checklists": 3,
    "data": 3,
    "agent-teams": 4,
    "utils": 2
  },
  "issues": 0
}
```

## 🎨 Agent Personas & Specializations

- **James (Dev)** - Pragmatic senior engineer focused on implementation
- **Sarah (PO)** - Meticulous quality guardian and process steward
- **John (PM)** - Strategic product manager and requirements expert
- **Winston (Architect)** - Holistic system designer and technical leader
- **Quinn (QA)** - Quality-obsessed reviewer and testing strategist
- **Mary (Analyst)** - Strategic researcher and market analysis expert
- **Sally (UX Expert)** - User-centered designer and AI prompt specialist
- **Bob (SM)** - Process-focused story creator and agile facilitator

## 🔍 What's Next

The BMad agents are now fully integrated with Claude Code and ready for use. The configuration follows Anthropic's best practices for agent development while preserving all BMad methodology capabilities.

### Recommended Next Steps:
1. Test agents with simple commands (`/bmad-master *help`)
2. Try the complete planning workflow for a small project
3. Execute a development cycle with document sharding
4. Provide feedback on agent performance and any needed adjustments

---

*BMad agents are now Claude Code native. Start with `/bmad-master *help` to explore all capabilities.*