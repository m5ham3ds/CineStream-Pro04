import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    c = f.read()

# Just remove all @OptIn for ExperimentalFoundationApi and add it to the file top
c = re.sub(r'@OptIn\(.*ExperimentalFoundationApi::class\)\s*', '', c)
c = c.replace('import androidx.compose.foundation.combinedClickable', 'import androidx.compose.foundation.combinedClickable\n@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)')

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(c)

