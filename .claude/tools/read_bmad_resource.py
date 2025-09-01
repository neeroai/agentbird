#!/usr/bin/env python3
"""
BMad Resource Reader Tool
Provides access to BMad shared resources (templates, tasks, checklists, data, workflows)
"""

import json
import os
import sys
from pathlib import Path

# Try to import yaml, but work without it if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

def main():
    if len(sys.argv) != 3:
        print(json.dumps({
            "error": "Usage: read_bmad_resource <resource_type> <resource_name>",
            "available_types": ["templates", "tasks", "checklists", "data", "workflows"],
            "example": "read_bmad_resource templates prd-tmpl.yaml"
        }))
        sys.exit(1)
    
    resource_type = sys.argv[1]
    resource_name = sys.argv[2]
    
    # Valid resource types
    valid_types = ["templates", "tasks", "checklists", "data", "workflows"]
    if resource_type not in valid_types:
        print(json.dumps({
            "error": f"Invalid resource type: {resource_type}",
            "available_types": valid_types
        }))
        sys.exit(1)
    
    # Build path to resource
    project_root = Path.cwd()
    resource_path = project_root / ".bmad-core" / resource_type / resource_name
    
    if not resource_path.exists():
        print(json.dumps({
            "error": f"Resource not found: {resource_path}",
            "searched_path": str(resource_path)
        }))
        sys.exit(1)
    
    try:
        with open(resource_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            "resource_type": resource_type,
            "resource_name": resource_name,
            "path": str(resource_path),
            "content": content
        }
        
        # If it's a YAML file, also parse it (if yaml is available)
        if resource_name.endswith(('.yaml', '.yml')) and HAS_YAML:
            try:
                parsed_content = yaml.safe_load(content)
                result["parsed_yaml"] = parsed_content
            except yaml.YAMLError as e:
                result["yaml_parse_error"] = str(e)
        elif resource_name.endswith(('.yaml', '.yml')) and not HAS_YAML:
            result["yaml_parse_note"] = "YAML parsing not available - install PyYAML for structured parsing"
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "error": f"Failed to read resource: {str(e)}",
            "resource_path": str(resource_path)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()