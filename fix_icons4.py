import os
import re

for root, dirs, files in os.walk('app/src/main/java/com/example'):
    for file in files:
        if file.endswith('.kt'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            original = content
            
            # For some reason HelpOutline and Send are still failing because they didn't get replaced correctly?
            # Let's fix them manually.
            content = content.replace('Icons.Filled.HelpOutline', 'Icons.AutoMirrored.Filled.HelpOutline')
            content = content.replace('Icons.Filled.Send', 'Icons.AutoMirrored.Filled.Send')
            content = content.replace('Icons.Filled.ArrowBack', 'Icons.AutoMirrored.Filled.ArrowBack')

            if "Icons." in content and "import androidx.compose.material.icons.Icons" not in content:
                match = re.search(r'package\s+[a-zA-Z0-9_\.]+\n', content)
                if match:
                    idx = match.end()
                    content = content[:idx] + "import androidx.compose.material.icons.Icons\n" + content[idx:]

            if content != original:
                with open(filepath, 'w') as f:
                    f.write(content)
