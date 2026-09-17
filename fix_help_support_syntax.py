import re

with open("app/src/main/java/com/example/ui/screens/profile/HelpSupportScreen.kt", "r") as f:
    c = f.read()

c = c.replace("import androidx.compose.material.icons.filled.AttachFile", "import androidx.compose.material.icons.filled.AttachFile\nimport androidx.compose.material.icons.filled.MoreVert\nimport androidx.compose.material.icons.filled.Check\nimport androidx.compose.foundation.lazy.LazyRow\nimport androidx.compose.foundation.lazy.items\nimport androidx.compose.foundation.lazy.itemsIndexed")
c = c.replace("crossAxisAlignment =", "horizontalAlignment =")

with open("app/src/main/java/com/example/ui/screens/profile/HelpSupportScreen.kt", "w") as f:
    f.write(c)

