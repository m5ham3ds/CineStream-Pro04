import os
import re

color_file = "app/src/main/java/com/example/ui/theme/Color.kt"
with open(color_file, "r") as f:
    c = f.read()

if "val SuccessGreen" not in c:
    c += "\nval SuccessGreen = Color(0xFF00C853)\n"
    with open(color_file, "w") as f:
        f.write(c)

files = [
    "app/src/main/java/com/example/ui/screens/social/ChatScreen.kt",
    "app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt",
    "app/src/main/java/com/example/ui/screens/share/ShareScreen.kt"
]

for filepath in files:
    with open(filepath, "r") as f:
        content = f.read()
    
    # Add import if missing
    if "MaterialTheme.colorScheme.tertiary" in content:
        if "import com.example.ui.theme.SuccessGreen" not in content:
            # find package and add import
            content = content.replace("package ", "package ")  # dummy
            if "import androidx.compose." in content:
                content = re.sub(r'(import androidx\.compose\.[^\n]+)', r'\1\nimport com.example.ui.theme.SuccessGreen', content, count=1)
        
        content = content.replace("MaterialTheme.colorScheme.tertiary", "SuccessGreen")
        
        with open(filepath, "w") as f:
            f.write(content)
            
