#!/usr/bin/env python3
"""
BMad Document Creator Tool
Creates documents using BMad templates with interactive workflows
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
    if len(sys.argv) < 2:
        # List available templates
        project_root = Path.cwd()
        templates_dir = project_root / ".bmad-core" / "templates"
        
        if templates_dir.exists():
            available_templates = [f.name for f in templates_dir.glob("*.yaml")]
        else:
            available_templates = []
        
        print(json.dumps({
            "error": "Usage: create_document <template_name> [output_file]",
            "description": "Create a document using a BMad template",
            "available_templates": available_templates,
            "example": "create_document prd-tmpl.yaml docs/prd.md"
        }))
        sys.exit(1)
    
    template_name = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Ensure template has .yaml extension if not provided
    if not template_name.endswith('.yaml'):
        template_name += '.yaml'
    
    # Build path to template
    project_root = Path.cwd()
    template_path = project_root / ".bmad-core" / "templates" / template_name
    
    if not template_path.exists():
        # List available templates
        templates_dir = project_root / ".bmad-core" / "templates"
        if templates_dir.exists():
            available_templates = [f.name for f in templates_dir.glob("*.yaml")]
        else:
            available_templates = []
        
        print(json.dumps({
            "error": f"Template not found: {template_name}",
            "searched_path": str(template_path),
            "available_templates": available_templates
        }))
        sys.exit(1)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Parse template YAML (if available)
        template_data = None
        if HAS_YAML:
            try:
                template_data = yaml.safe_load(template_content)
            except yaml.YAMLError as e:
                print(json.dumps({
                    "error": f"Invalid YAML template: {str(e)}",
                    "template_path": str(template_path)
                }))
                sys.exit(1)
        else:
            print(json.dumps({
                "error": "YAML parsing not available - install PyYAML to use templates",
                "template_path": str(template_path),
                "raw_content": template_content
            }))
            sys.exit(1)
        
        result = {
            "template_name": template_name,
            "template_path": str(template_path),
            "template_data": template_data,
            "output_file": output_file,
            "status": "template_loaded",
            "instructions": "Template loaded successfully. Use template data to create document following BMad methodology."
        }
        
        # Extract key template information
        if isinstance(template_data, dict):
            if 'name' in template_data:
                result['document_type'] = template_data['name']
            if 'description' in template_data:
                result['description'] = template_data['description']
            if 'elicit' in template_data:
                result['interactive'] = template_data['elicit']
            if 'sections' in template_data:
                result['sections'] = list(template_data['sections'].keys()) if isinstance(template_data['sections'], dict) else []
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "error": f"Failed to load template: {str(e)}",
            "template_path": str(template_path)
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()