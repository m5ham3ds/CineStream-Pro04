with open("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt", "r") as f:
    text = f.read()

import_lines = "import com.example.ui.components.rememberCardMediaDetail\nimport com.example.ui.components.CardMediaDetail\nimport kotlin.math.absoluteValue\nimport androidx.compose.ui.text.style.TextOverflow\nimport androidx.compose.material.icons.filled.Pause\n"

text = text.replace("package com.example.ui.screens.home", "package com.example.ui.screens.home\n" + import_lines)

with open("app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt", "w") as f:
    f.write(text)
