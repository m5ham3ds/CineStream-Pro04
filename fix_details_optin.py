with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    lines = f.readlines()

new_lines = []
opt_in_seen = False
for line in lines:
    if "@OptIn(ExperimentalFoundationApi::class)" in line:
        if not opt_in_seen:
            new_lines.append(line)
            opt_in_seen = True
    elif "@OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)" in line:
        pass # remove duplicates
    else:
        new_lines.append(line)
        opt_in_seen = False # reset for next composable

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.writelines(new_lines)

