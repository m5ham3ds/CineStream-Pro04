import re

file_path = "app/src/main/java/com/example/navigation/AppNavigation.kt"
with open(file_path, "r") as f:
    content = f.read()

# 1. Add Library to hasTopBar
if "Screen.Library.route" not in content.split('hasTopBar')[1].split(')')[0]:
    content = content.replace("Screen.Profile.route,", "Screen.Library.route, Screen.Profile.route,")

# 2. Fix TopBar Colors
content = content.replace("Color(0xFFE50914)", "MaterialTheme.colorScheme.primary")
content = content.replace("tint = androidx.compose.ui.graphics.Color.UnspecifiedVariant", "tint = MaterialTheme.colorScheme.onSurfaceVariant")

# 3. Add LTR Wrapper to the top bar
target = "                    if (hasTopBar) {\n                    Column("
replacement = "                    if (hasTopBar) {\n                    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Ltr) {\n                    Column("
if target in content and "CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Ltr)" not in content.split("if (hasTopBar) {")[1]:
    content = content.replace(target, replacement)
    
    # Need to close the CompositionLocalProvider.
    # Where does `if (hasTopBar) {` close?
    # It closes right before `bottomBar = {`
    # Let's see context around bottomBar
    #
    #                     }
    #                 }
    #                 }
    #             },
    #             bottomBar = {
    # 
    
    # We can just replace
    close_target = "                }\n                }\n            },\n            bottomBar = {"
    close_replacement = "                }\n                }\n                }\n            },\n            bottomBar = {"
    content = content.replace(close_target, close_replacement)

with open(file_path, "w") as f:
    f.write(content)
