import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    c = f.read()

# We need to ensure that the import list is valid and there's no random @file:OptIn in the middle
if c.count("@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)") > 1:
    c = c.replace("@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)\n", "", c.count("@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)") - 1)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(c)
