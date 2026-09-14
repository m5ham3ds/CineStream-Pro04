import re

with open("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt", "r") as f:
    text = f.read()

import_lines = "import com.example.ui.components.rememberCardMediaDetail\nimport com.example.ui.components.CardMediaDetail\nimport kotlin.math.absoluteValue\nimport androidx.compose.ui.text.style.TextOverflow\nimport androidx.compose.material.icons.filled.Pause\n"

if "import com.example.ui.components.rememberCardMediaDetail" not in text:
    text = text.replace("package com.example.ui.screens.home", "package com.example.ui.screens.home\n" + import_lines)
    
text = text.replace("item.id.hashCode().absoluteValue", "Math.abs(item.id.hashCode())")

with open("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt", "w") as f:
    f.write(text)
