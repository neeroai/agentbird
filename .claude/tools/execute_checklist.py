#!/usr/bin/env python3
"""
BMad Checklist Executor Tool
Executes validation checklists from the BMad methodology
"""

import json
import os
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        # List available checklists
        project_root = Path.cwd()
        checklists_dir = project_root / ".bmad-core" / "checklists"
        
        if checklists_dir.exists():
            available_checklists = [f.stem for f in checklists_dir.glob("*.md")]
        else:
            available_checklists = []
        
        print(json.dumps({
            "error": "Usage: execute_checklist <checklist_name> [target_document]",
            "description": "Execute a BMad validation checklist",
            "available_checklists": available_checklists,
            "example": "execute_checklist po-master-checklist docs/prd.md"
        }))
        sys.exit(1)
    
    checklist_name = sys.argv[1]
    target_document = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Ensure checklist has .md extension if not provided
    if not checklist_name.endswith('.md'):
        checklist_name += '.md'
    
    # Build path to checklist
    project_root = Path.cwd()
    checklist_path = project_root / ".bmad-core" / "checklists" / checklist_name
    
    if not checklist_path.exists():
        # List available checklists
        checklists_dir = project_root / ".bmad-core" / "checklists"
        if checklists_dir.exists():
            available_checklists = [f.stem for f in checklists_dir.glob("*.md")]
        else:
            available_checklists = []
        
        print(json.dumps({
            "error": f"Checklist not found: {checklist_name}",
            "searched_path": str(checklist_path),
            "available_checklists": available_checklists
        }))
        sys.exit(1)
    
    try:
        with open(checklist_path, 'r', encoding='utf-8') as f:
            checklist_content = f.read()
        
        result = {
            "checklist_name": checklist_name,
            "checklist_path": str(checklist_path),
            "target_document": target_document,
            "checklist_content": checklist_content,
            "status": "loaded",
            "instructions": "Checklist loaded successfully. Execute each checklist item systematically following BMad methodology."
        }
        
        # Parse checklist items (look for - [ ] or - [x] patterns)
        import re
        checklist_items = []
        lines = checklist_content.split('\n')
        
        for line in lines:
            # Match checklist items
            match = re.match(r'^[\s]*[-*]\s*\[([ x])\]\s*(.+)', line)
            if match:
                is_checked = match.group(1).lower() == 'x'
                item_text = match.group(2).strip()
                checklist_items.append({
                    "checked": is_checked,
                    "text": item_text
                })
        
        if checklist_items:
            result["checklist_items"] = checklist_items
            result["total_items"] = len(checklist_items)
            result["checked_items"] = sum(1 for item in checklist_items if item["checked"])
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "error": f"Failed to load checklist: {str(e)}",
            "checklist_path": str(checklist_path)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()