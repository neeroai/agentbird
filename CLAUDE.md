# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

AgentBird is a dual-purpose repository combining Bird.com AI Employee documentation with the BMad-Method agent system. Understanding this architecture is crucial for productive work:

### Documentation Layer (Root Level)
- **Numbered Documentation Files** (01-14): Spanish-language Bird.com AI setup guides following KISS methodology
- **Template System** (`templates/`): Reusable configuration guides for Bird.com manual setup
- **KISS Compliance**: Enforced by `.cursorrules` - max 20 root files, max 3 templates, no nesting beyond 2 levels

### BMad Agent System (Optimized Architecture)
- **Claude Code Agent Definitions** (`.claude/agents/`): 10 specialized agents following Claude Code best practices with hyper-detailed descriptions and standardized YAML frontmatter
- **Consolidated Resource Architecture** (`.bmad-core/`):
  - `tasks/`: 17 executable workflow definitions for agent operations
  - `templates/`: 12 YAML templates for documents (PRD, architecture, stories) with interactive elicitation workflows
  - `workflows/`: Complete project workflows (greenfield-fullstack.yaml, brownfield-ui.yaml, etc.)
  - `checklists/`: 6 validation checklists for quality assurance
  - `data/`: Knowledge base and methodology documentation
- **Legacy Directory** (`agents/`): Contains only README.md documentation, agent definitions have been consolidated

### Workflow Architecture Pattern
The BMad system follows a structured flow:
1. **Planning Phase** (Web UI): Analyst → PM → UX Expert → Architect → PO validation
2. **Development Phase** (IDE): PO sharding → SM story creation → Dev implementation → QA review

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

### Working with BMad Agents
```bash
# Access agents in Claude Code using / prefix
/bmad-master             # Universal executor
/dev                     # Development implementation
/po                      # Product owner validation
/pm                      # Product management and PRDs
/architect               # System architecture design

# Agent commands use * prefix
*help                    # Show available commands
*create-doc             # Interactive document creation
*develop-story          # Execute development workflow
*shard-doc              # Break large docs for development
```

### File Structure Validation
```bash
# Check numbered documentation files (01-14)
for i in {01..14}; do ls ${i}-*.md 2>/dev/null || echo "Missing ${i}"; done

# Validate templates directory structure
ls templates/            # Should contain max 3 files
ls .bmad-core/           # Consolidated BMad resources
```

## Key Architectural Insights

### Optimized Agent Architecture (Claude Code Best Practices)
The agent system has been optimized following Claude Code best practices research:
- **Single Source of Truth**: All agent definitions consolidated in `.claude/agents/` directory
- **Hyper-Detailed Descriptions**: Agent descriptions follow Claude Code recommendation for 3-4+ sentences with specific use cases, capabilities, and constraints
- **Standardized YAML Frontmatter**: Each agent includes name, detailed description, color, and tool definitions
- **Resource Consolidation**: Eliminated duplication between `agents/_shared/` and `.bmad-core/` - single `.bmad-core/` location
- **Tool-Based Resource Access**: Agents access BMad resources through standardized tools rather than direct file references
- **90% Duplication Reduction**: Reduced from 30+ duplicated agent files across 3 locations to 10 optimized agents

### YAML-Driven Templates
The BMad system uses sophisticated YAML templates with interactive workflows:
- Templates define document structure, elicitation strategies, and validation rules
- Interactive mode enables progressive document building through agent conversations
- Templates are versioned and support multiple output formats

### Agent Resource Loading
Agents automatically load shared resources from `.bmad-core/`:
- Templates from `.bmad-core/templates/` (12 YAML templates)
- Task workflows from `.bmad-core/tasks/` (17 executable workflows)
- Validation checklists from `.bmad-core/checklists/` (6 validation checklists)
- Methodology knowledge from `.bmad-core/data/bmad-kb.md`

### Document Sharding Strategy
Large documents are "sharded" by the PO agent to manage context limits:
- Breaks comprehensive PRDs into development-sized pieces
- Maintains document coherence while enabling focused work
- Essential for the SM → Dev implementation cycle

### Workflow State Management
BMad workflows track progression through structured phases:
- Each workflow defines agent sequence and deliverables
- Supports both greenfield (new) and brownfield (existing) projects
- Includes quality gates and validation checkpoints

### Configuration Constraints
Bird.com documentation emphasizes manual-only configuration:
- No JSON/YAML configuration files for Bird.com
- All setup through web interface
- Documentation must remain generic (no client-specific content)

## Important Files

- **`.cursorrules`**: Defines KISS methodology and file structure constraints
- **`agents/_shared/data/bmad-kb.md`**: Complete BMad methodology knowledge base
- **`MIGRATION_PLAN.md`**: Strategy for agent system evolution
- **`.github/workflows/ci.yml`**: Comprehensive validation pipeline including link checking and security scanning

## BMad Agent Command Reference

Each agent has specialized commands accessible via `*command` syntax and accesses resources from `.bmad-core/`:
- **bmad-master**: `*kb` (knowledge base mode), `*task` (execute any workflow), `*create-doc`, `*shard-doc`
- **dev**: `*develop-story` (full implementation cycle), `*run-tests` - accesses story templates and development workflows
- **po**: `*shard-doc` (document breaking), `*execute-checklist` - accesses validation checklists and quality workflows  
- **pm**: `*create-prd` (requirements documents) - accesses PRD templates and project brief templates
- **architect**: `*create-architecture` - accesses fullstack, frontend, and brownfield architecture templates
- **qa**: `*review-code`, `*execute-checklist` - accesses quality assurance checklists and testing workflows
- **analyst**: `*facilitate-brainstorming`, `*create-research` - accesses market research and competitive analysis templates

The optimized agent system eliminates duplication while maintaining role-switching capability for fresh context and specialized expertise throughout the development lifecycle.