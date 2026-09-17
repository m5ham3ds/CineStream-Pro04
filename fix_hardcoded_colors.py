import os
import re

def replace_hardcoded_colors(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r") as f:
        content = f.read()
    
    # In ProfileScreen, replace redPrimary with MaterialTheme.colorScheme.primary
    if "ProfileScreen.kt" in filepath:
        content = re.sub(r'val redPrimary = Color\(0xFFE50914\)', 'val redPrimary = androidx.compose.material3.MaterialTheme.colorScheme.primary', content)
        
    if "SettingsScreen.kt" in filepath:
        content = re.sub(r'val redPrimary = Color\(0xFFE50914\)', 'val redPrimary = androidx.compose.material3.MaterialTheme.colorScheme.primary', content)
        content = re.sub(r'Color\(0xFFE50914\)', 'androidx.compose.material3.MaterialTheme.colorScheme.primary', content)

    with open(filepath, "w") as f:
        f.write(content)

replace_hardcoded_colors("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt")
replace_hardcoded_colors("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt")

