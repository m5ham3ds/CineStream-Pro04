import re

file_path = "app/src/main/java/com/example/navigation/AppNavigation.kt"
with open(file_path, "r") as f:
    content = f.read()

# The ModalNavigationDrawer is wrapped in RTL hardcode. Let's remove it and use LocalLayoutDirection.current.
# Actually, if we just remove the CompositionLocalProvider overrides entirely, Jetpack Compose will automatically inherit the correct LayoutDirection based on the context's Locale (which MainActivity sets correctly using AppCompatDelegate).

# Let's see if we can find the exact strings to replace/remove.
rtl_str = "    androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Rtl) {\n"
ltr_str = "        androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {\n"

# We should also replace the closing braces for these providers.

if rtl_str in content:
    content = content.replace(rtl_str, "")
    # The first closing brace of that block is at the very end of AppNavigation.kt
    # We will remove the last '}' in the file.
    last_brace_idx = content.rfind('}')
    content = content[:last_brace_idx] + content[last_brace_idx+1:]

if ltr_str in content:
    content = content.replace(ltr_str, "")
    # Find the closing brace for this LTR block. It's likely right before the bottomBar closing or inside ModalNavigationDrawer.
    # It wraps `if (showExitDialog) { ... }` up to the end of `Scaffold`.
    # Let's find `bottomBar = {`
    
with open(file_path, "w") as f:
    f.write(content)

