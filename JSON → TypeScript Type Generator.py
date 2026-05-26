# Input : line 1 = T; then per case: line A = root name, line B = compact JSON.
# Output: per-case blocks joined by a line `---`, ending with one '\n'.

import sys
import json

class TypeNode:
    def __init__(self):
        self.primitives = set()
        self.has_array = False
        self.array_node = None
        self.has_object = False
        self.object_fields = {}
        self.object_count = 0
        self.field_counts = {}
        self.interface_name = None

    def add(self, val):
        if val is None:
            self.primitives.add("null")
        elif isinstance(val, bool):
            self.primitives.add("boolean")
        elif isinstance(val, (int, float)):
            self.primitives.add("number")
        elif isinstance(val, str):
            self.primitives.add("string")
        elif isinstance(val, list):
            self.has_array = True
            if self.array_node is None:
                self.array_node = TypeNode()
            for item in val:
                self.array_node.add(item)
        elif isinstance(val, dict):
            self.has_object = True
            self.object_count += 1
            for k, v in val.items():
                if k not in self.object_fields:
                    self.object_fields[k] = TypeNode()
                    self.field_counts[k] = 0
                self.field_counts[k] += 1
                self.object_fields[k].add(v)

def get_name(base_name, used_names):
    if base_name not in used_names:
        used_names.add(base_name)
        return base_name
    idx = 2
    while f"{base_name}{idx}" in used_names:
        idx += 1
    new_name = f"{base_name}{idx}"
    used_names.add(new_name)
    return new_name

def compute_type_string(node):
    types = []
    for p in sorted(list(node.primitives)):
        types.append(p)
    
    if node.has_object:
        types.append(node.interface_name)
        
    if node.has_array:
        if node.array_node is None or (
            not node.array_node.primitives and 
            not node.array_node.has_object and 
            not node.array_node.has_array):
            types.append("unknown[]")
        else:
            elem_type = compute_type_string(node.array_node)
            if " | " in elem_type:
                types.append(f"({elem_type})[]")
            else:
                types.append(f"{elem_type}[]")
                
    types.sort()
    return " | ".join(types)

def solve(root_name, json_text):
    data = json.loads(json_text)
    
    if not data:
        return f"export interface {root_name} {{}}"
        
    root_node = TypeNode()
    for item in data:
        root_node.add(item)
        
    used_names = {root_name}
    root_node.interface_name = root_name
    interfaces = {}
    
    def traverse(node):
        if node.has_object:
            fields_dict = {}
            interfaces[node.interface_name] = fields_dict
            
            sorted_keys = sorted(node.object_fields.keys())
            for k in sorted_keys:
                child_node = node.object_fields[k]
                
                if child_node.has_object:
                    base = k[0].upper() + k[1:]
                    child_node.interface_name = get_name(base, used_names)
                    traverse(child_node)
                    
                if child_node.has_array:
                    if child_node.array_node and child_node.array_node.has_object:
                        base = k[0].upper() + k[1:]
                        child_node.array_node.interface_name = get_name(base, used_names)
                        traverse(child_node.array_node)
                        
                field_type_str = compute_type_string(child_node)
                is_optional = node.field_counts[k] < node.object_count
                
                fields_dict[k] = {
                    "type": field_type_str,
                    "optional": is_optional
                }

    traverse(root_node)
    
    iface_blocks = []
    for iface_name in sorted(interfaces.keys()):
        fields = interfaces[iface_name]
        if not fields:
            iface_blocks.append(f"export interface {iface_name} {{}}")
        else:
            lines = []
            lines.append(f"export interface {iface_name} {{")
            for k in sorted(fields.keys()):
                opt = "?" if fields[k]["optional"] else ""
                lines.append(f"  {k}{opt}: {fields[k]['type']};")
            lines.append("}")
            iface_blocks.append("\n".join(lines))
            
    return "\n\n".join(iface_blocks)

def main():
    raw_input = sys.stdin.read().strip()
    if not raw_input:
        return
    lines = raw_input.split('\n')
    t = int(lines[0].strip())
    
    blocks = []
    idx = 1
    for _ in range(t):
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        if idx >= len(lines):
            break
            
        root_name = lines[idx].strip()
        json_text = lines[idx+1].strip()
        idx += 2
        
        blocks.append(solve(root_name, json_text))
        
    sys.stdout.write('\n---\n'.join(blocks) + '\n')

if __name__ == '__main__':
    main()
