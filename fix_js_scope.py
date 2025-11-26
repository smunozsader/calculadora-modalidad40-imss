#!/usr/bin/env python3
"""
Fix JavaScript scope error for desglose variable in index.html
Moves the 2029 and 2030 payment updates inside the if blocks where desglose is defined.
"""

import re

def fix_js_scope():
    file_path = r"G:\My Drive\2025. SEMANAS COTIZADAS SERGIO\webapp\templates\index.html"
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the problematic structure
    pattern = r'(if \(resultado\.inversion\.desglose_anual\) \{\s*const desglose = resultado\.inversion\.desglose_anual;\s*(?:if \(desglose\[\'[0-9]+\'\]\).*?\n)*\s*)\}\s*(if \(desglose\[\'2029\'\]\).*?\n\s*if \(desglose\[\'2030\'\]\).*?\n)'
    
    def replacement_func(match):
        inside_block = match.group(1)
        outside_lines = match.group(2)
        
        # Move the outside lines inside the block, but before the closing }
        fixed_block = inside_block.rstrip() + '\n                ' + outside_lines.strip().replace('\n', '\n                ') + '\n            }'
        
        return fixed_block
    
    # Apply the fix
    fixed_content = re.sub(pattern, replacement_func, content, flags=re.MULTILINE | re.DOTALL)
    
    # If regex didn't work, try a more direct approach
    if content == fixed_content:
        # Look for the specific problematic lines and fix them
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Look for the pattern where we have the closing } followed by desglose usage
            if (line.strip() == '}' and 
                i + 1 < len(lines) and 
                'desglose[\'2029\']' in lines[i + 1]):
                
                # Found the problematic pattern
                # Move the next two lines (2029 and 2030) up before the }
                line_2029 = lines[i + 1]
                line_2030 = lines[i + 2] if i + 2 < len(lines) and 'desglose[\'2030\']' in lines[i + 2] else None
                
                # Add the moved lines with proper indentation before the }
                if line_2029:
                    fixed_lines.append('            ' + line_2029.strip())
                if line_2030:
                    fixed_lines.append('            ' + line_2030.strip())
                
                # Add the closing }
                fixed_lines.append(line)
                
                # Skip the original problematic lines
                i += 1
                if line_2030:
                    i += 2  # Skip both 2029 and 2030 lines
                else:
                    i += 1  # Skip just the 2029 line
                
            else:
                fixed_lines.append(line)
                i += 1
        
        fixed_content = '\n'.join(fixed_lines)
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("JavaScript scope error fixed successfully!")
    print("The desglose['2029'] and desglose['2030'] lines have been moved inside their respective if blocks.")

if __name__ == "__main__":
    fix_js_scope()