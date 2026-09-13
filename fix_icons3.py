import os
import re

for root, dirs, files in os.walk('app/src/main/java/com/example'):
    for file in files:
        if file.endswith('.kt'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            original = content
            
            content = content.replace('androidx.compose.material.icons.automirrored.filled.ArrowBack', 'Icons.AutoMirrored.Filled.ArrowBack')
            content = content.replace('androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight', 'Icons.AutoMirrored.Filled.KeyboardArrowRight')
            content = content.replace('androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft', 'Icons.AutoMirrored.Filled.KeyboardArrowLeft')
            content = content.replace('androidx.compose.material.icons.automirrored.filled.Send', 'Icons.AutoMirrored.Filled.Send')
            content = content.replace('androidx.compose.material.icons.automirrored.filled.HelpOutline', 'Icons.AutoMirrored.Filled.HelpOutline')
            content = content.replace('androidx.compose.material.icons.automirrored.outlined.ArrowBack', 'Icons.AutoMirrored.Outlined.ArrowBack')

            if "Icons.AutoMirrored" in content and "import androidx.compose.material.icons.automirrored" not in content:
                # add imports
                imports = """import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
"""
                match = re.search(r'package\s+[a-zA-Z0-9_\.]+\n', content)
                if match:
                    idx = match.end()
                    content = content[:idx] + imports + content[idx:]

            if content != original:
                with open(filepath, 'w') as f:
                    f.write(content)
