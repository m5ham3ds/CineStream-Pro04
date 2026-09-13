import os
import re

directories_to_scan = ['app/src/main/java/com/example/ui']

# Safe replacements for colors
color_replacements = {
    r'Color\.White': 'MaterialTheme.colorScheme.onBackground',
    r'Color\.Black': 'MaterialTheme.colorScheme.background',
    r'Color\.Gray': 'MaterialTheme.colorScheme.onSurfaceVariant',
    r'Color\.DarkGray': 'MaterialTheme.colorScheme.surfaceVariant',
    r'Color\(0xFFE50914\)': 'MaterialTheme.colorScheme.primary',
    r'Color\(0xFFB20710\)': 'MaterialTheme.colorScheme.secondary',
    r'Color\(0xFF141414\)': 'MaterialTheme.colorScheme.background',
    r'Color\(0xFF2F2F2F\)': 'MaterialTheme.colorScheme.surfaceVariant'
}

# Exceptional replacements:
# Sometimes Color.Black is used for text in light mode (which is fine, but in dark mode it should be white).
# Wait, if they hardcoded Color.White for text, they want white in dark mode. If we switch to light mode, it should be black.
# So Color.White -> MaterialTheme.colorScheme.onBackground is perfect!
# But what if they used Color.Black for the background of a Box?
# Color.Black -> MaterialTheme.colorScheme.background is perfect.
# What if they used Color.Black for text in AuthScreen? 
# Let's check AuthScreen: `Text("G ", color = Color.Black)` - Google button is usually white with black text in both themes, or adapting.

def replace_colors_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content
    
    # We should NOT replace colors in Theme.kt or Color.kt
    if 'Theme.kt' in filepath or 'Color.kt' in filepath:
        return
        
    # We shouldn't replace Color.Transparent or Color.Green/Red used for status (like downloads) unless we want to.
    
    # Special cases in AuthScreen for the Google button:
    # "Sign in with Google" has containerColor = Color.White, color = Color.Black.
    # If we replace Color.White -> onBackground (which is Black in light mode), the button becomes Black on Black!
    # So for ButtonDefaults.buttonColors(containerColor = Color.White), maybe we change it to surface?
    
    for old, new in color_replacements.items():
        # Only replace if it's not part of another word
        content = re.sub(r'(?<![a-zA-Z0-9_])' + old + r'(?![a-zA-Z0-9_])', new, content)
        
    # Fix imports if MaterialTheme is missing
    if content != original_content and 'import androidx.compose.material3.MaterialTheme' not in content:
        content = content.replace('import androidx.compose.runtime.Composable', 'import androidx.compose.material3.MaterialTheme\nimport androidx.compose.runtime.Composable')
        
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)

for root, dirs, files in os.walk(directories_to_scan[0]):
    for file in files:
        if file.endswith('.kt'):
            replace_colors_in_file(os.path.join(root, file))

print("Color replacements done.")
