#!/usr/bin/env python3
"""
BMad Knowledge Base Mode Toggle Tool
Toggles knowledge base mode for accessing BMad methodology documentation
"""

import json
import os
import sys
from pathlib import Path

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(json.dumps({
            "description": "Toggle knowledge base mode to access BMad methodology documentation",
            "usage": "toggle_kb_mode [on|off]",
            "default": "Toggle current state if no argument provided"
        }))
        sys.exit(0)
    
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else None
    
    # Build path to knowledge base
    project_root = Path.cwd()
    kb_path = project_root / ".bmad-core" / "data" / "bmad-kb.md"
    
    if not kb_path.exists():
        print(json.dumps({
            "error": f"BMad knowledge base not found: {kb_path}",
            "status": "kb_not_found"
        }))
        sys.exit(1)
    
    try:
        # Always load the knowledge base when toggling
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb_content = f.read()
        
        # Determine the mode
        if mode is None:
            kb_mode = "toggle"
        elif mode in ["on", "true", "1", "enable"]:
            kb_mode = "on"
        elif mode in ["off", "false", "0", "disable"]:
            kb_mode = "off"
        else:
            kb_mode = "toggle"
        
        result = {
            "kb_mode": kb_mode,
            "kb_path": str(kb_path),
            "status": "loaded",
            "instructions": f"Knowledge base mode {kb_mode}. BMad methodology documentation loaded for consultation."
        }
        
        # Always include the knowledge base content when KB mode is activated
        if kb_mode in ["on", "toggle"]:
            result["kb_content"] = kb_content
            
            # Extract key sections for quick reference
            lines = kb_content.split('\n')
            sections = []
            current_section = None
            
            for line in lines:
                if line.startswith('## '):
                    if current_section:
                        sections.append(current_section)
                    current_section = {
                        "title": line.strip('## ').strip(),
                        "content": []
                    }
                elif current_section and line.strip():
                    current_section["content"].append(line)
            
            if current_section:
                sections.append(current_section)
            
            result["kb_sections"] = [{"title": s["title"], "preview": s["content"][:3]} for s in sections]
            result["total_sections"] = len(sections)
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "error": f"Failed to access knowledge base: {str(e)}",
            "kb_path": str(kb_path)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()