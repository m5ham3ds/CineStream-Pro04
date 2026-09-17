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
    
    # 1. Add LazyColumn import
    if "import androidx.compose.foundation.lazy.LazyColumn" not in content:
        content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.lazy.LazyColumn")
        
    # 2. Find the Column
    header_pattern = r'(\s*)val scrollState = rememberScrollState\(\)\s*Column\(\s*modifier\s*=\s*Modifier[\s\S]*?\.verticalScroll\(scrollState\)[\s\S]*?\)\s*\{'
    match = re.search(header_pattern, content)
    if not match:
        continue
        
    indent = match.group(1)
    start_idx = match.start()
    end_idx = match.end()
    
    new_header = f"{indent}LazyColumn(\n{indent}    modifier = Modifier.fillMaxSize()\n{indent}) {{"
    
    # 3. Find end of Column
    brace_count = 1
    idx = end_idx
    while idx < len(content) and brace_count > 0:
        if content[idx] == '{':
            brace_count += 1
        elif content[idx] == '}':
            brace_count -= 1
        idx += 1
    
    col_end_idx = idx - 1
    
    col_body = content[end_idx:col_end_idx]
    
    # 4. Wrap top-level blocks in `item { ... }`
    # We will iterate character by character.
    # When brace_count == 0, we accumulate characters.
    # When we see `{`, we accumulate the whole block until brace_count == 0 again.
    # We yield the block, and wrap it if it contains actual code (not just whitespace/comments).
    
    idx2 = 0
    wrapped_body = ""
    current_block = ""
    
    def is_code(text):
        # remove comments
        text = re.sub(r'//.*', '', text)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        return bool(re.search(r'\w', text))
    
    while idx2 < len(col_body):
        # find start of a token/block
        c = col_body[idx2]
        
        # We need to correctly parse braces, strings, comments.
        # But we only care about brace level.
        if c.isspace():
            current_block += c
            idx2 += 1
            continue
            
        # Start of a non-whitespace element
        # It could be a comment, or an identifier.
        # We read until we hit `{`, then read the block, OR we read until `;` or newline.
        # Wait, if we just split by top-level `{` blocks:
        # A statement like `Spacer(modifier = Modifier.height(16.dp))` has NO `{`.
        # So we can't just look for `{`.
        break # This approach is too complex for python.

