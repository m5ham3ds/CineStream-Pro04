import os
import re

replacements = {
    'Icons.Filled.ArrowBack': 'Icons.AutoMirrored.Filled.ArrowBack',
    'Icons.Filled.KeyboardArrowRight': 'Icons.AutoMirrored.Filled.KeyboardArrowRight',
    'Icons.Filled.KeyboardArrowLeft': 'Icons.AutoMirrored.Filled.KeyboardArrowLeft',
    'Icons.Filled.HelpOutline': 'Icons.AutoMirrored.Filled.HelpOutline',
    'androidx.compose.material.icons.androidx.compose.material.icons': 'androidx.compose.material.icons'
}

for root, dirs, files in os.walk('app/src/main/java/com/example'):
    for file in files:
        if file.endswith('.kt'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            original = content
            for old, new in replacements.items():
                content = content.replace(old, new)
            if content != original:
                with open(filepath, 'w') as f:
                    f.write(content)
