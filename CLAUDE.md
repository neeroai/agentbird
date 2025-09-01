# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

AgentBird is a specialized documentation repository primarily focused on Bird.com AI Employee setup and configuration, enhanced with BMad-Method agents optimized for documentation tasks. Understanding this architecture is crucial for productive work:

### Primary Purpose: Bird.com AI Employee Documentation
- **Knowledge Base** (`knowledge-base/`): Comprehensive Spanish-language Bird.com AI setup guides and references
- **Template System** (`templates/`): Reusable configuration guides for Bird.com manual setup (2 files)
- **KISS Compliance**: Enforced by `.cursorrules` - max 20 root files, max 3 templates, no nesting beyond 2 levels
- **Manual Configuration Focus**: All Bird.com setup through web interface (no automated configs)

### BMad Agent System (Optimized Architecture)
- **Claude Code Agent Definitions** (`.claude/agents/`): 12 specialized agents following Claude Code best practices with hyper-detailed descriptions and standardized YAML frontmatter
- **Consolidated Resource Architecture** (`.bmad-core/`):
  - `tasks/`: 10 executable workflow definitions for documentation and planning operations
  - `templates/`: 5 YAML templates for documents (PRD, market research, project brief) with interactive elicitation workflows
  - `checklists/`: 3 validation checklists for quality assurance and change management
  - `data/`: Knowledge base, brainstorming techniques, and methodology documentation
- **Legacy Directory** (`agents/`): Contains only README.md documentation, agent definitions have been consolidated

### Documentation Workflow Pattern
The optimized agent system follows a documentation-focused flow:
1. **Research Phase**: Analyst → Market research and competitive analysis
2. **Planning Phase**: PM → Requirements documentation and project briefs  
3. **Creation Phase**: BMad-Master → Document creation and content development
4. **Validation Phase**: PO → Quality assurance and document validation

## Development Commands

### Primary Commands
```bash
# Install dependencies (required for linting)
npm install

# Lint all markdown files
npm run lint

# Validate internal links across all documentation
npm run validate-links

# Build documentation (placeholder)
npm run build

# Serve documentation (placeholder)
npm run serve
```

### CI/CD Validation
The repository uses GitHub Actions for comprehensive validation:
```bash
# What CI runs on every commit:
npm ci                    # Clean install
npm run lint              # Markdown linting
npm run validate-links    # Link validation
# + Custom file structure validation
# + Basic security scanning for API keys
```

### Working with Documentation Agents
```bash
# Primary agents (fully functional for documentation)
/bmad-master             # Universal executor - all documentation tasks
/pm                      # Product requirements and strategic documents
/analyst                 # Market research and competitive analysis
/po                      # Document validation and quality assurance

# Specialized agents
/api-documenter          # API documentation specialist
/research-analyst        # Strategic research expert
/openai-specialist       # OpenAI integration specialist
/ux-expert              # UX design and frontend specifications

# Agent commands use * prefix
*help                    # Show available commands
*create-doc             # Interactive document creation
*facilitate-brainstorming # Brainstorming sessions
*execute-checklist      # Quality validation
*kb                     # Knowledge base access (bmad-master only)
```

### File Structure Validation
```bash
# Validate knowledge base structure
ls knowledge-base/       # Bird.com documentation structure

# Validate templates directory structure  
ls templates/            # Should contain 2 files max (KISS compliance)
ls .bmad-core/           # Consolidated BMad resources (30 files)
```

## Key Architectural Insights

### Optimized Agent Architecture (Claude Code Best Practices)
The agent system has been optimized following Claude Code best practices research:
- **Single Source of Truth**: All agent definitions consolidated in `.claude/agents/` directory
- **Hyper-Detailed Descriptions**: Agent descriptions follow Claude Code recommendation for 3-4+ sentences with specific use cases, capabilities, and constraints
- **Standardized YAML Frontmatter**: Each agent includes name, detailed description, color, and tool definitions
- **Resource Consolidation**: Eliminated duplication between `agents/_shared/` and `.bmad-core/` - single `.bmad-core/` location
- **Tool-Based Resource Access**: Agents access BMad resources through standardized tools rather than direct file references
- **90% Duplication Reduction**: Reduced from 30+ duplicated agent files across 3 locations to 12 optimized agents

### YAML-Driven Templates
The BMad system uses sophisticated YAML templates with interactive workflows:
- Templates define document structure, elicitation strategies, and validation rules
- Interactive mode enables progressive document building through agent conversations
- Templates are versioned and support multiple output formats

### Agent Resource Loading
Agents automatically load shared resources from `.bmad-core/`:
- Templates from `.bmad-core/templates/` (5 YAML templates for documentation)
- Task workflows from `.bmad-core/tasks/` (10 executable workflows for planning and documentation)
- Validation checklists from `.bmad-core/checklists/` (3 validation checklists for quality assurance)
- Methodology knowledge from `.bmad-core/data/bmad-kb.md`

### Document Sharding Strategy
Large documents are "sharded" by the PO agent to manage context limits:
- Breaks comprehensive documentation into manageable sections
- Maintains document coherence while enabling focused review and validation
- Essential for quality assurance and collaborative document development

### Documentation Workflow Management
BMad workflows track progression through structured documentation phases:
- Each workflow defines documentation agent sequence and deliverables
- Supports both new documentation projects and existing document enhancement
- Includes quality gates, validation checkpoints, and content review processes

### Configuration Constraints
Bird.com documentation emphasizes manual-only configuration:
- No JSON/YAML configuration files for Bird.com
- All setup through web interface
- Documentation must remain generic (no client-specific content)

## Important Files

- **`.cursorrules`**: Defines KISS methodology and file structure constraints
- **`.bmad-core/data/bmad-kb.md`**: Complete BMad methodology knowledge base
- **`MIGRATION_PLAN.md`**: Strategy for agent system evolution
- **`.github/workflows/ci.yml`**: Comprehensive validation pipeline including link checking and security scanning

## Agent Command Reference (Documentation Focus)

### 🎯 **Fully Functional Agents (Primary)**
Each agent accesses optimized resources from `.bmad-core/`:

- **bmad-master**: `*kb`, `*task`, `*create-doc`, `*shard-doc`, `*execute-checklist` - Universal access to all BMad resources
- **pm**: `*create-prd`, `*create-doc` - PRD templates, project briefs, market research templates  
- **analyst**: `*facilitate-brainstorming`, `*create-research` - Market research, competitor analysis, brainstorming templates
- **po**: `*shard-doc`, `*execute-checklist` - Document validation, quality workflows, change management checklists

### 🔧 **Specialized Documentation Agents**
- **api-documenter**: `*help` - API documentation specialist with comprehensive documentation capabilities
- **research-analyst**: `*help` - Strategic research and market analysis expert
- **openai-specialist**: `*help` - OpenAI integration and configuration specialist  
- **ux-expert**: `*help` - UX design and frontend specification specialist

### ⚠️ **Limited Functionality Agents** (Software Development Focus - Reduced Capabilities)
- **dev**: `*help` - Basic commands available (lost story and architecture templates)
- **architect**: `*help` - Generic commands only (lost architecture-specific templates)
- **qa**: `*help` - Basic validation only (lost story-specific checklists)
- **sm**: `*help` - Basic commands only (lost story creation capabilities)

## Repository Optimization Summary

**AgentBird has been optimized for its dual purpose:**
- **Primary Focus**: Bird.com AI Employee documentation with comprehensive Spanish-language guides
- **Secondary Enhancement**: BMad agents specialized for documentation, research, and content creation tasks
- **Optimization Result**: 45% reduction in `.bmad-core` files while maintaining core documentation capabilities
- **Agent Status**: 4 fully functional documentation agents, 4 specialized agents, 4 limited-function agents

The optimized agent system prioritizes documentation excellence while maintaining methodology-driven workflows for professional document creation and validation.