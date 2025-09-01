# AgentBird to Claude Code Migration Plan

## Phase 1: Agent Conversion and Technical Implementation (Priority 1)

### 1. Directory Structure Setup
Create Claude Code compliant directory structure:
```
.claude/
├── agents/                    # Project-level subagents (highest priority)
│   ├── bmad-master.md
│   ├── dev.md
│   ├── po.md
│   ├── pm.md
│   ├── architect.md
│   ├── qa.md
│   ├── analyst.md
│   ├── ux-expert.md
│   └── sm.md
├── settings.json             # Permissions and configuration
└── hooks.json               # Tool execution hooks
```

### 2. Agent File Structure Conversion
Transform existing agents to Claude Code subagent format:

**Required YAML frontmatter structure:**
```yaml
---
name: agent-name
description: Concise description of when this subagent should be invoked
tools: Read, Edit, Bash, Grep, Glob  # Optional - inherits all if omitted
---

Agent system prompt and instructions go here...
```

**Key conversions:**
- Convert `*` command syntax to natural language descriptions
- Maintain specialized expertise while optimizing for Claude Code delegation
- Each agent operates in separate context window (prevents context pollution)
- Enable automatic delegation based on task matching

### 3. Permissions Configuration (settings.json)
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(agents/_shared/**)",
      "Edit(docs/**)",
      "Write(output/**)"
    ],
    "deny": [
      "Read(.env*)",
      "Edit(.env*)",
      "Bash(rm -rf*)",
      "Bash(sudo*)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1"
  }
}
```

### 4. Shared Resource Integration
- Migrate `agents/_shared/` to accessible location for Claude Code subagents
- Update resource loading to use Claude Code's native file access patterns
- Maintain existing YAML template structure with interactive workflows
- Ensure templates remain compatible with both systems during transition

## Phase 2: MCP Integration and External Tools (Priority 2)

### 1. Model Context Protocol (MCP) Server Configuration
Set up MCP servers for enhanced agent capabilities:

**Create `.mcp.json` configuration:**
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {}
    },
    "filesystem": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-filesystem"],
      "env": {}
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### 2. Hook System Implementation
Create automated workflows with tool execution hooks:

**Example hooks.json configuration:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint -- --fix"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash(git commit*)",
        "hooks": [
          {
            "type": "command", 
            "command": "npm test"
          }
        ]
      }
    ]
  }
}
```

### 3. Enhanced Agent Capabilities with MCP
- **Memory persistence**: Agents maintain context across sessions
- **Git integration**: Automated version control workflows
- **GitHub integration**: PR creation, issue tracking, code review
- **Filesystem**: Enhanced file operations beyond basic tools

### 4. Template Library Expansion with MCP Support
- React/Next.js frontend templates with GitHub Actions
- Node.js/Express backend templates with database MCP
- Python/FastAPI service templates with testing automation
- Database schema templates with migration tracking
- Mobile app (React Native) templates with deployment hooks
- DevOps/Infrastructure templates with monitoring integration

## Phase 3: New Specialized Agents (Priority 2)

### 5. Security Specialist Agent
- Security audit and vulnerability assessment
- Compliance validation (GDPR, SOC2, etc.)
- Security architecture review

### 6. Performance Optimizer Agent
- Code performance analysis
- Database query optimization
- Frontend performance auditing

### 7. Documentation Expert Agent
- API documentation generation
- Technical writing and editing
- Knowledge base curation

### 8. Testing Specialist Agent
- Test strategy design
- Test automation setup
- Quality metrics analysis

## Phase 4: Configuration and Optimization (Priority 2)

### 1. Custom Status Line Configuration
Create contextual status information display:

**Example statusline script (.claude/statusline.sh):**
```bash
#!/bin/bash
input=$(cat)

# Helper functions for JSON parsing
get_model_name() { echo "$input" | jq -r '.model.display_name'; }
get_current_dir() { echo "$input" | jq -r '.workspace.current_dir'; }
get_git_branch() { git branch --show-current 2>/dev/null || echo "no-git"; }

MODEL=$(get_model_name)
DIR=$(basename $(get_current_dir))
BRANCH=$(get_git_branch)

echo "[$MODEL] 📁 $DIR 🌿 $BRANCH"
```

### 2. GitHub Actions Integration
Configure automated Claude Code workflows:

**Example .github/workflows/claude-review.yml:**
```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  claude-review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review this PR for code quality, security issues, and adherence to BMad methodology"
          claude_args: "--max-turns 5 --append-system-prompt 'You are the QA agent from BMad methodology'"
```

### 3. Performance Optimization
- **Context Management**: Each subagent maintains separate context to prevent pollution
- **Intelligent Delegation**: Automatic task routing based on agent descriptions
- **Resource Caching**: Efficient shared resource loading
- **Memory Management**: MCP memory server for persistent context

### 4. Testing and Validation Framework
- Agent response validation scripts
- Template functionality testing
- MCP server connectivity verification
- Hook execution testing

## Phase 5: Quality System and Advanced Features (Priority 3)

### 1. Automated validation checklists
- Cross-document consistency checks with MCP memory
- Template quality validation with automated testing
- Workflow completion verification through hooks
- Real-time quality metrics via status line

### 2. Advanced Agent Capabilities
- **Multi-agent collaboration**: Chained subagent workflows
- **Dynamic tool management**: Context-aware tool allocation
- **Adaptive delegation**: Learning from user preferences
- **Cross-session memory**: Persistent context via MCP

## Enhanced Expected Outcomes

### Core BMad Methodology Preservation ✅
- **Maintain** all existing BMad methodology workflows with enhanced execution
- **Preserve** specialized agent expertise while optimizing for Claude Code's architecture
- **Retain** comprehensive template system with improved accessibility
- **Continue** structured workflow progression (Planning → Development → Quality)

### Significant Technical Improvements 🚀
- **Separate Context Windows**: Each subagent operates independently, preventing context pollution
- **Intelligent Delegation**: Automatic task routing based on agent descriptions and capabilities
- **Enhanced Tool Management**: Granular permissions and tool allocation per agent
- **Memory Persistence**: Cross-session context retention via MCP memory server

### New Capabilities 🆕
- **Real-time Automation**: Hook system enables automatic linting, testing, and validation
- **External Integrations**: MCP servers provide GitHub, Git, filesystem, and memory capabilities
- **Performance Monitoring**: Built-in telemetry and status line for workflow visibility
- **GitHub Actions Integration**: Automated code review and quality checks in CI/CD pipeline

### Expanded Coverage 📈
- **Technology Stack Support**: Templates and agents for React, Node.js, Python, FastAPI, mobile
- **Domain Expertise**: Security, performance, documentation, and testing specialists
- **Deployment Automation**: Infrastructure templates with monitoring integration
- **Quality Systems**: Automated validation with cross-document consistency checks

## Migration Benefits Summary

### Immediate Benefits (Phase 1)
- ✅ **Better Context Management**: No more context window pollution between agents
- ✅ **Simplified Invocation**: Natural language agent selection vs. command memorization
- ✅ **Enhanced Security**: Granular tool permissions and access control
- ✅ **Native Integration**: Optimized for Claude Code's architecture and performance

### Medium-term Benefits (Phases 2-3)
- 🔄 **Persistent Memory**: Agents remember context across sessions
- 🔄 **Automated Workflows**: Hooks eliminate manual repetitive tasks
- 🔄 **External Tool Integration**: Direct access to GitHub, Git, and development tools
- 🔄 **Enhanced Collaboration**: Multi-agent workflows with chained delegation

### Long-term Benefits (Phases 4-5)
- 🎯 **Adaptive Intelligence**: Agents learn user preferences and optimize delegation
- 🎯 **Quality Automation**: Real-time validation and quality metrics
- 🎯 **Advanced Integrations**: Custom MCP servers for domain-specific tools
- 🎯 **Comprehensive Monitoring**: Performance analytics and workflow optimization

## Current Structure Analysis (Preserved + Enhanced)

### Existing Agents (9) → Claude Code Subagents
1. **BMad Master** → Intelligent orchestrator with MCP memory access
2. **Dev Agent (James)** → Enhanced with automated testing and linting hooks  
3. **Product Owner (Sarah)** → Integrated with GitHub for PR and issue management
4. **Product Manager (John)** → Template-driven PRD creation with validation hooks
5. **Architect (Winston)** → Architecture templates with deployment automation
6. **QA Agent (Quinn)** → Automated code review with security scanning
7. **Business Analyst (Mary)** → Research capabilities with web search MCP integration
8. **UX Expert (Sally)** → UI/UX templates with component library integration
9. **Scrum Master (Bob)** → Story management with GitHub issue integration

### Enhanced Shared Resources
- **Templates**: 12+ YAML templates → Enhanced with MCP integration and automation
- **Tasks**: 15+ executable workflows → Converted to Claude Code compatible format
- **Checklists**: 6 validation checklists → Automated via hooks and MCP validation
- **Data**: Knowledge base → Accessible via MCP memory server with persistent storage
- **Workflows**: 6 complete workflows → Enhanced with CI/CD integration and monitoring

## Implementation Technical Details

### Migration Scripts and Commands

**1. Directory Setup Script:**
```bash
#!/bin/bash
# setup-claude-code.sh

# Create Claude Code directory structure
mkdir -p .claude/agents
mkdir -p .claude/hooks

# Copy existing agents with conversion
for agent in agents/*.md; do
  agent_name=$(basename "$agent" .md)
  echo "Converting $agent_name..."
  
  # Add YAML frontmatter and convert to Claude Code format
  {
    echo "---"
    echo "name: $agent_name"
    echo "description: $(grep -m1 '# ' "$agent" | sed 's/# //')"
    echo "tools: Read, Edit, Bash, Grep, Glob"
    echo "---"
    echo ""
    sed '1,/^# /d' "$agent"  # Remove original title
  } > ".claude/agents/$agent_name.md"
done

echo "Agent conversion complete!"
```

**2. Validation Commands:**
```bash
# Validate agent configuration
claude /agents                    # Open agents management interface

# Test specific agent
echo "Test task for dev agent" | claude --subagent dev

# Validate MCP servers
claude --mcp-config .mcp.json --verbose

# Test hooks
touch test.md && echo "test" > test.md  # Should trigger hooks
```

**3. Template Migration Script:**
```bash
#!/bin/bash
# migrate-templates.sh

# Ensure shared resources are accessible
ln -sf "$(pwd)/agents/_shared" ".claude/shared"

# Update template paths in agent files
for agent_file in .claude/agents/*.md; do
  sed -i 's|agents/_shared|.claude/shared|g' "$agent_file"
done
```

### Testing Framework

**Agent Response Testing:**
```bash
# Test agent delegation
test_agent_delegation() {
  local test_prompt="Create a simple REST API endpoint"
  local response=$(echo "$test_prompt" | claude --print)
  
  if [[ "$response" == *"dev"* ]] || [[ "$response" == *"architect"* ]]; then
    echo "✅ Delegation working"
  else
    echo "❌ Delegation failed"
  fi
}

# Test MCP connectivity  
test_mcp_servers() {
  claude --print "List available MCP tools" | grep -q "mcp__"
  if [ $? -eq 0 ]; then
    echo "✅ MCP servers connected"
  else
    echo "❌ MCP servers not available"
  fi
}
```

### Troubleshooting Common Issues

**1. Agent Not Found:**
```bash
# Check agent file structure
ls -la .claude/agents/
# Verify YAML frontmatter syntax
head -10 .claude/agents/dev.md
```

**2. Permission Denied:**
```bash
# Check settings.json permissions
claude config list
# Add specific permissions
claude config add permissions.allow "Bash(your-command)"
```

**3. MCP Server Connection Issues:**
```bash
# Test MCP server individually
npx @modelcontextprotocol/server-memory --help
# Check environment variables
echo $GITHUB_TOKEN
```

### Performance Monitoring

**Enable telemetry for monitoring:**
```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "console",
    "OTEL_METRIC_EXPORT_INTERVAL": "10000"
  }
}
```

This migration maintains the power of your BMad-Method framework while optimizing it for Claude Code's environment and significantly expanding its capabilities.