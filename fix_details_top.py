with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    lines = f.readlines()

new_lines = ["@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)\n"]
for line in lines:
    if "@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)" in line:
        continue
    new_lines.append(line)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.writelines(new_lines)
