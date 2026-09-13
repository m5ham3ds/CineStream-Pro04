import re

file_path = "app/src/main/java/com/example/navigation/AppNavigation.kt"
with open(file_path, "r") as f:
    content = f.read()

# I want to remove the specific wrapper around ModalNavigationDrawer:
# androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Rtl) {
# ModalNavigationDrawer(...)
# }
# And the wrapper around NavHost/AlertDialog:
# androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {

# It's easier to just strip these specific lines, and then we need to strip their corresponding closing braces.
# Since counting braces is hard in regex, I'll use a simple parser.

def remove_composition_local(content, start_str):
    idx = content.find(start_str)
    if idx == -1:
        return content
    
    # Remove the start string
    new_content = content[:idx] + content[idx + len(start_str):]
    
    # Now find the matching closing brace.
    # Start looking from the index where we removed the start_str
    open_braces = 0
    in_string = False
    escape = False
    
    for i in range(idx, len(new_content)):
        char = new_content[i]
        
        if escape:
            escape = False
            continue
            
        if char == '\\':
            escape = True
            continue
            
        if char == '"' and not escape:
            in_string = not in_string
            continue
            
        if not in_string:
            if char == '{':
                open_braces += 1
            elif char == '}':
                if open_braces == 0:
                    # Found the closing brace for the removed wrapper!
                    return new_content[:i] + new_content[i+1:]
                else:
                    open_braces -= 1
                    
    return new_content

rtl_start = "    androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Rtl) {\n"
ltr_start = "        androidx.compose.runtime.CompositionLocalProvider(androidx.compose.ui.platform.LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {\n"

c1 = remove_composition_local(content, rtl_start)
c2 = remove_composition_local(c1, ltr_start)

if c2 != content:
    with open(file_path, "w") as f:
        f.write(c2)

