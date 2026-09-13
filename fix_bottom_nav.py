file_path = "app/src/main/java/com/example/ui/components/BottomNavBar.kt"
with open(file_path, "r") as f:
    content = f.read()

import_str = "import androidx.compose.runtime.CompositionLocalProvider\nimport androidx.compose.ui.platform.LocalLayoutDirection\nimport androidx.compose.ui.unit.LayoutDirection"

if "CompositionLocalProvider" not in content:
    content = content.replace("import androidx.compose.runtime.Composable", "import androidx.compose.runtime.Composable\n" + import_str)

target = "    Box(\n        modifier = Modifier"
replacement = "    CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Ltr) {\n    Box(\n        modifier = Modifier"

if target in content and "provides LayoutDirection.Ltr" not in content:
    content = content.replace(target, replacement)
    
    # find the last closing brace and add another
    idx = content.rfind("}")
    content = content[:idx] + "}\n}"

with open(file_path, "w") as f:
    f.write(content)
