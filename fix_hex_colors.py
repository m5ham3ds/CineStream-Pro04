import re
import os

color_map = {
    # Backgrounds
    r'Color\(0xFF121212\)': 'MaterialTheme.colorScheme.background',
    r'Color\(0xFF0F0F11\)': 'MaterialTheme.colorScheme.background',
    # Surfaces
    r'Color\(0xFF1C1C1E\)': 'MaterialTheme.colorScheme.surface',
    r'Color\(0xFF1E1E1E\)': 'MaterialTheme.colorScheme.surface',
    r'Color\(0xFF19191C\)': 'MaterialTheme.colorScheme.surface',
    # Surface Variants (borders, unselected tabs, secondary backgrounds)
    r'Color\(0xFF2A2A2E\)': 'MaterialTheme.colorScheme.surfaceVariant',
    r'Color\(0xFF2C2C2E\)': 'MaterialTheme.colorScheme.surfaceVariant'
}

import glob

for filepath in glob.glob('app/src/main/java/com/example/ui/**/*.kt', recursive=True):
    if 'Theme.kt' in filepath or 'Color.kt' in filepath:
        continue

    with open(filepath, 'r') as f:
        content = f.read()
        
    original_content = content
    
    for old_regex, new_val in color_map.items():
        content = re.sub(old_regex, new_val, content)
        
    if content != original_content:
        # Add import if needed
        if 'import androidx.compose.material3.MaterialTheme' not in content:
            content = content.replace('import androidx.compose.runtime.Composable', 'import androidx.compose.material3.MaterialTheme\nimport androidx.compose.runtime.Composable')
            
        with open(filepath, 'w') as f:
            f.write(content)

print("Hex Color replacements done.")
