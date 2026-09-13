import glob

for filepath in glob.glob('app/src/main/java/com/example/**/*.kt', recursive=True):
    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.splitlines()
    new_lines = []
    seen_imports = set()
    
    for line in lines:
        if line.startswith('import '):
            if line in seen_imports:
                continue
            seen_imports.add(line)
        new_lines.append(line)
        
    new_content = '\n'.join(new_lines)
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)

print("Duplicate import fix done.")
