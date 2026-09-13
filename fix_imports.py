import re
def fix_file(path, import_str):
    with open(path, 'r') as f:
        content = f.read()
    
    # Remove it if it was added at the very beginning
    if content.startswith(import_str + '\n'):
        content = content[len(import_str + '\n'):]
        
    # Find package declaration
    match = re.search(r'package\s+[a-zA-Z0-9_\.]+\n', content)
    if match:
        idx = match.end()
        if import_str not in content:
            content = content[:idx] + import_str + '\n' + content[idx:]
    with open(path, 'w') as f:
        f.write(content)

fix_file("app/src/main/java/com/example/navigation/AppNavigation.kt", "import com.example.ui.components.swipeToNavigate")
fix_file("app/src/main/java/com/example/utils/NotificationHelper.kt", "import com.example.R")
