#!/usr/bin/env python3
"""
BMad Task Executor Tool
Executes BMad methodology tasks and workflows
"""

import json
import os
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: execute_bmad_task <task_name> [task_args...]",
            "description": "Execute a BMad methodology task from the _shared/tasks directory",
            "example": "execute_bmad_task create-doc prd-tmpl.yaml"
        }))
        sys.exit(1)
    
    task_name = sys.argv[1]
    task_args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    # Build path to task
    project_root = Path.cwd()
    task_path = project_root / ".bmad-core" / "tasks" / f"{task_name}.md"
    
    if not task_path.exists():
        # List available tasks
        tasks_dir = project_root / ".bmad-core" / "tasks"
        if tasks_dir.exists():
            available_tasks = [f.stem for f in tasks_dir.glob("*.md")]
        else:
            available_tasks = []
        
        print(json.dumps({
            "error": f"Task not found: {task_name}",
            "searched_path": str(task_path),
            "available_tasks": available_tasks
        }))
        sys.exit(1)
    
    try:
        with open(task_path, 'r', encoding='utf-8') as f:
            task_content = f.read()
        
        result = {
            "task_name": task_name,
            "task_path": str(task_path),
            "task_args": task_args,
            "task_content": task_content,
            "status": "loaded",
            "instructions": "Task loaded successfully. Execute the instructions in the task_content following BMad methodology."
        }
        
        # Parse task metadata if available
        lines = task_content.split('\n')
        metadata = {}
        in_frontmatter = False
        
        for i, line in enumerate(lines):
            if line.strip() == '---' and i == 0:
                in_frontmatter = True
                continue
            elif line.strip() == '---' and in_frontmatter:
                break
            elif in_frontmatter and ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        if metadata:
            result["task_metadata"] = metadata
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "error": f"Failed to load task: {str(e)}",
            "task_path": str(task_path)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()