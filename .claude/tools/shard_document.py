#!/usr/bin/env python3
"""
BMad Document Sharding Tool
Shards large documents into manageable pieces for development consumption
"""

import json
import os
import sys
from pathlib import Path
import re

def estimate_tokens(text):
    """Rough token estimation (1 token ≈ 4 characters)"""
    return len(text) // 4

def find_section_breaks(content):
    """Find natural section breaks in markdown content"""
    lines = content.split('\n')
    breaks = []
    
    for i, line in enumerate(lines):
        # Look for markdown headers
        if re.match(r'^#{1,6}\s+', line):
            header_level = len(line) - len(line.lstrip('#'))
            breaks.append({
                "line": i,
                "level": header_level,
                "title": line.strip('#').strip(),
                "type": "header"
            })
        # Look for horizontal rules
        elif re.match(r'^[-*_]{3,}$', line.strip()):
            breaks.append({
                "line": i,
                "level": 0,
                "title": "Section Break",
                "type": "rule"
            })
    
    return breaks

def create_shards(content, max_tokens=3000):
    """Create document shards with optimal size and natural breaks"""
    lines = content.split('\n')
    breaks = find_section_breaks(content)
    
    shards = []
    current_shard = []
    current_tokens = 0
    
    last_break_index = 0
    
    for i, line in enumerate(lines):
        current_shard.append(line)
        current_tokens += estimate_tokens(line)
        
        # Check if we should create a shard at this point
        should_break = False
        
        # If we're over the token limit and at a natural break
        if current_tokens > max_tokens:
            # Find the nearest break point
            for break_point in breaks:
                if break_point["line"] >= last_break_index and break_point["line"] <= i:
                    should_break = True
                    break
            
            # If no natural break found and we're significantly over limit, force break
            if not should_break and current_tokens > max_tokens * 1.5:
                should_break = True
        
        if should_break and len(current_shard) > 10:  # Ensure minimum shard size
            shard_content = '\n'.join(current_shard)
            shards.append({
                "index": len(shards) + 1,
                "content": shard_content,
                "tokens": estimate_tokens(shard_content),
                "lines": len(current_shard)
            })
            
            current_shard = []
            current_tokens = 0
            last_break_index = i
    
    # Add remaining content as final shard
    if current_shard:
        shard_content = '\n'.join(current_shard)
        shards.append({
            "index": len(shards) + 1,
            "content": shard_content,
            "tokens": estimate_tokens(shard_content),
            "lines": len(current_shard)
        })
    
    return shards

def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: shard_document <input_file> <output_directory> [max_tokens]",
            "description": "Shard a large document into manageable pieces for development",
            "default_max_tokens": 3000,
            "example": "shard_document docs/prd.md docs/prd_shards 2500"
        }))
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_directory = sys.argv[2]
    max_tokens = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    
    input_path = Path(input_file)
    output_dir = Path(output_directory)
    
    if not input_path.exists():
        print(json.dumps({
            "error": f"Input file not found: {input_file}",
            "searched_path": str(input_path)
        }))
        sys.exit(1)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create shards
        shards = create_shards(content, max_tokens)
        
        # Write shards to files
        shard_files = []
        for shard in shards:
            shard_filename = f"{input_path.stem}_shard_{shard['index']:02d}.md"
            shard_path = output_dir / shard_filename
            
            with open(shard_path, 'w', encoding='utf-8') as f:
                f.write(shard['content'])
            
            shard_files.append({
                "filename": shard_filename,
                "path": str(shard_path),
                "tokens": shard['tokens'],
                "lines": shard['lines']
            })
        
        # Create index file
        index_content = f"# {input_path.stem} - Document Shards Index\n\n"
        index_content += f"Original document: {input_file}\n"
        index_content += f"Total shards: {len(shards)}\n"
        index_content += f"Max tokens per shard: {max_tokens}\n\n"
        index_content += "## Shards\n\n"
        
        for i, shard_file in enumerate(shard_files, 1):
            index_content += f"{i}. [{shard_file['filename']}](./{shard_file['filename']}) "
            index_content += f"({shard_file['tokens']} tokens, {shard_file['lines']} lines)\n"
        
        index_path = output_dir / f"{input_path.stem}_index.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        result = {
            "input_file": input_file,
            "output_directory": output_directory,
            "max_tokens": max_tokens,
            "total_shards": len(shards),
            "shard_files": shard_files,
            "index_file": str(index_path),
            "status": "success",
            "instructions": "Document successfully sharded. Use individual shards for development following BMad methodology."
        }
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({
            "error": f"Failed to shard document: {str(e)}",
            "input_file": input_file
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()