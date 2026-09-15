import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

imports = """import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.tween
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.unit.dp
"""

# Insert imports at the top
if "import androidx.compose.animation.core.animateFloat" not in content:
    content = content.replace("package com.example.ui.screens.details", "package com.example.ui.screens.details\n\n" + imports)

# Fix ExtensionManager path
content = content.replace("com.example.data.extension.ExtensionManager", "com.example.extensions.ExtensionManager")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
