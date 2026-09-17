import os
import re

files_to_fix = [
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt",
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt"
]

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        continue
    with open(filepath, "r") as f:
        content = f.read()
    
    if "val scrollState = rememberScrollState()" not in content:
        continue
        
    print(f"Fixing {filepath}")
    
    # 1. Remove scrollState
    content = re.sub(r'\s*val scrollState = rememberScrollState\(\)', '', content)
    
    # 2. Add import for LazyColumn and items
    if "import androidx.compose.foundation.lazy.LazyColumn" not in content:
        content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.lazy.LazyColumn")
        
    # We need to find the `Column(` that has `.verticalScroll(scrollState)`
    # It usually looks like this:
    # Column(
    #     modifier = Modifier
    #         .fillMaxSize()
    #         .verticalScroll(scrollState)
    # ) {
    
    # Let's find the start of `Column(`
    match = re.search(r'Column\(\s*modifier\s*=\s*Modifier[^)]*\.verticalScroll\(scrollState\)[^)]*\)\s*\{', content)
    if not match:
        # Fallback
        match = re.search(r'Column\(\s*modifier\s*=\s*Modifier[\s\S]*?\.verticalScroll\(scrollState\)[\s\S]*?\)\s*\{', content)
    
    if not match:
        print(f"Could not find Column in {filepath}")
        continue
        
    start_idx = match.start()
    end_idx = match.end()
    
    # Replace Column(...) { with LazyColumn(modifier = Modifier.fillMaxSize()) {
    new_header = "LazyColumn(\n        modifier = Modifier.fillMaxSize()\n    ) {"
    
    # Now we need to parse the contents of this Column block.
    # We find the matching closing brace.
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
    # A block starts at the first non-whitespace character, and ends when brace_count goes to 0 AND we hit a newline or EOF.
    # Actually, simpler: we just wrap each top-level statement in `item { \n ... \n}`.
    
    wrapped_body = ""
    
    idx2 = 0
    while idx2 < len(column_body):
        # skip whitespace
        while idx2 < len(column_body) and column_body[idx2].isspace():
            wrapped_body += column_body[idx2]
            idx2 += 1
            
        if idx2 >= len(column_body):
            break
            
        # We are at the start of a statement.
        start_stmt = idx2
        stmt_brace_count = 0
        in_string = False
        in_comment = False
        in_line_comment = False
        
        while idx2 < len(column_body):
            c = column_body[idx2]
            
            # Handle strings
            if c == '"' and not in_comment and not in_line_comment:
                # check escape
                if idx2 == 0 or column_body[idx2-1] != '\\':
                    in_string = not in_string
                    
            # Handle comments
            if not in_string:
                if c == '/' and idx2 + 1 < len(column_body) and column_body[idx2+1] == '/':
                    in_line_comment = True
                elif c == '\n' and in_line_comment:
                    in_line_comment = False
                elif c == '/' and idx2 + 1 < len(column_body) and column_body[idx2+1] == '*':
                    in_comment = True
                elif c == '*' and idx2 + 1 < len(column_body) and column_body[idx2+1] == '/':
                    in_comment = False
                    
                if not in_comment and not in_line_comment:
                    if c == '{':
                        stmt_brace_count += 1
                    elif c == '}':
                        stmt_brace_count -= 1
                        
            idx2 += 1
            
            # If we are not in braces, not in string, not in block comment, and we hit a newline or are at EOF
            if stmt_brace_count == 0 and not in_string and not in_comment and not in_line_comment:
                # We reached the end of a top-level statement. 
                # Let's see if the statement is just a comment.
                stmt_text = column_body[start_stmt:idx2].strip()
                if stmt_text.startswith('//') and '\n' not in stmt_text:
                    # just a comment, don't wrap it yet
                    break
                else:
                    break

        stmt_text = column_body[start_stmt:idx2]
        
        # Don't wrap if it's just comments
        if stmt_text.strip().startswith('//') and not re.search(r'\w', re.sub(r'//.*', '', stmt_text)):
            wrapped_body += stmt_text
        else:
            # Wrap!
            # Indent the statement by 4 spaces
            indented = "\n".join("    " + line if line.strip() else line for line in stmt_text.split('\n'))
            wrapped_body += f"item {{\n{indented}\n}}"
            
    # Reassemble
    new_content = content[:start_idx] + new_header + wrapped_body + content[column_content_end:]
    
    with open(filepath, "w") as f:
        f.write(new_content)

