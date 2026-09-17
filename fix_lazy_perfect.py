import os
import re

files_to_fix = [
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt",
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt"
]

for filepath in files_to_fix:
    with open(filepath, "r") as f:
        content = f.read()
    
    if "val scrollState = rememberScrollState()" not in content:
        continue
        
    print(f"Fixing {filepath}")
    
    # 1. Remove scrollState
    content = re.sub(r'\s*val scrollState = rememberScrollState\(\)', '', content)
    
    # 2. Add import for LazyColumn
    if "import androidx.compose.foundation.lazy.LazyColumn" not in content:
        content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.lazy.LazyColumn")
        
    # Find Column
    match = re.search(r'Column\(\s*modifier\s*=\s*Modifier[^)]*\.verticalScroll\(scrollState\)[^)]*\)\s*\{', content)
    if not match:
        match = re.search(r'Column\(\s*modifier\s*=\s*Modifier[\s\S]*?\.verticalScroll\(scrollState\)[\s\S]*?\)\s*\{', content)
    
    if not match:
        continue
        
    start_idx = match.start()
    end_idx = match.end()
    
    new_header = "LazyColumn(\n        modifier = Modifier.fillMaxSize()\n    ) {"
    
    brace_count = 1
    idx = end_idx
    while idx < len(content) and brace_count > 0:
        if content[idx] == '{':
            brace_count += 1
        elif content[idx] == '}':
            brace_count -= 1
        idx += 1
        
    column_content_end = idx - 1
    
    column_body = content[end_idx:column_content_end]
    
    # Now, parse top-level blocks inside column_body.
    # We will iterate through column_body.
    # When brace_count == 0, we are at the top level.
    # If we encounter a non-whitespace character, we start a new block.
    # We read until brace_count == 0 AND we hit two newlines (or EOF), or just read until brace_count == 0 and the next character is not part of a chained call.
    # Actually, a much safer way: 
    # Just wrap each line/block that starts at the current indentation level.
    # But Kotlin can span multiple lines.
    
    # Let's use a very simple heuristic:
    # Any top level `if` statement, `Spacer`, `SectionTitle`, `LazyRow` etc.
    # We can just split the body by top-level nodes using a proper AST parser.
    # Since we don't have one, we can do this:
    # A top level node starts at a non-whitespace char. It ends when brace_count returns to 0 AND we reach a newline.
    
    wrapped_body = ""
    i = 0
    while i < len(column_body):
        # skip leading whitespace but KEEP it in the output
        ws = ""
        while i < len(column_body) and column_body[i].isspace():
            ws += column_body[i]
            i += 1
        wrapped_body += ws
        
        if i >= len(column_body):
            break
            
        start_node = i
        bc = 0
        in_string = False
        
        while i < len(column_body):
            c = column_body[i]
            
            if c == '"' and (i == 0 or column_body[i-1] != '\\'):
                in_string = not in_string
                
            if not in_string:
                if c == '{':
                    bc += 1
                elif c == '}':
                    bc -= 1
                    
            i += 1
            
            # If we returned to brace_count 0 and the character is a newline, 
            # this is a complete node.
            # Wait, `if (...) {\n ... \n}` ends at `}`, then a newline.
            # But what if there's `else {`? 
            # If the next non-ws token is `else`, it's part of the same node.
            if bc == 0 and i < len(column_body) and column_body[i] == '\n':
                # lookahead to see if next word is 'else'
                temp_i = i + 1
                while temp_i < len(column_body) and column_body[temp_i].isspace():
                    temp_i += 1
                if temp_i + 4 <= len(column_body) and column_body[temp_i:temp_i+4] == 'else':
                    continue # keep parsing
                else:
                    break

        node_text = column_body[start_node:i]
        
        # Don't wrap if it's purely a comment (starts with // and has no newlines, or is just comments)
        # Actually, let's just wrap everything that contains an alphanumeric char.
        if re.search(r'[a-zA-Z0-9]', node_text):
            # indent node_text
            indented = "\n".join("    " + line if line.strip() else line for line in node_text.split("\n"))
            wrapped_body += f"item {{\n{indented}\n}}"
        else:
            wrapped_body += node_text

    new_content = content[:start_idx] + new_header + wrapped_body + content[column_content_end:]
    
    with open(filepath, "w") as f:
        f.write(new_content)

