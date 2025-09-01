#!/usr/bin/env python3
"""
Claude Code BMad Agent Configuration Validator
"""

import json
import os
from pathlib import Path

def validate_agent_configuration():
    """Validate the Claude Code agent configuration"""
    
    results = {
        "status": "success",
        "agents_found": [],
        "tools_found": [],
        "issues": [],
        "summary": {}
    }
    
    project_root = Path.cwd()
    claude_dir = project_root / ".claude"
    
    # Check .claude directory exists
    if not claude_dir.exists():
        results["status"] = "error"
        results["issues"].append(".claude directory not found")
        return results
    
    # Check agents directory
    agents_dir = claude_dir / "agents"
    if not agents_dir.exists():
        results["status"] = "error"
        results["issues"].append("agents directory not found")
        return results
    
    # Expected agents
    expected_agents = [
        "bmad-master.md", "dev.md", "po.md", "pm.md", "architect.md",
        "qa.md", "analyst.md", "ux-expert.md", "sm.md"
    ]
    
    # Check each agent
    for agent in expected_agents:
        agent_path = agents_dir / agent
        if agent_path.exists():
            results["agents_found"].append(agent)
        else:
            results["issues"].append(f"Missing agent: {agent}")
    
    # Check tools directory
    tools_dir = claude_dir / "tools"
    if not tools_dir.exists():
        results["issues"].append("tools directory not found")
    else:
        # Expected tools
        expected_tools = [
            "read_bmad_resource.py", "execute_bmad_task.py", "create_document.py",
            "execute_checklist.py", "shard_document.py", "toggle_kb_mode.py"
        ]
        
        for tool in expected_tools:
            tool_path = tools_dir / tool
            if tool_path.exists() and os.access(tool_path, os.X_OK):
                results["tools_found"].append(tool)
            elif tool_path.exists():
                results["issues"].append(f"Tool exists but not executable: {tool}")
            else:
                results["issues"].append(f"Missing tool: {tool}")
    
    # Check tools.json
    tools_json = claude_dir / "tools.json"
    if not tools_json.exists():
        results["issues"].append("tools.json configuration file not found")
    
    # Check BMad shared resources
    bmad_core = project_root / ".bmad-core"
    if not bmad_core.exists():
        results["issues"].append("BMad core resources directory not found")
    else:
        # Check key resource directories
        resource_dirs = ["templates", "tasks", "checklists", "data"]
        for resource_dir in resource_dirs:
            dir_path = bmad_core / resource_dir
            if dir_path.exists():
                file_count = len(list(dir_path.glob("*")))
                results["summary"][f"{resource_dir}_files"] = file_count
            else:
                results["issues"].append(f"Missing resource directory: {resource_dir}")
    
    # Update status based on issues
    if results["issues"]:
        results["status"] = "warning" if len(results["agents_found"]) > 6 else "error"
    
    # Summary
    results["summary"]["agents_found"] = len(results["agents_found"])
    results["summary"]["agents_expected"] = len(expected_agents)
    results["summary"]["tools_found"] = len(results["tools_found"])
    results["summary"]["issues_count"] = len(results["issues"])
    
    return results

def main():
    results = validate_agent_configuration()
    print(json.dumps(results, indent=2))
    
    # Exit with appropriate code
    if results["status"] == "error":
        exit(1)
    elif results["status"] == "warning":
        exit(2)
    else:
        exit(0)

if __name__ == "__main__":
    main()