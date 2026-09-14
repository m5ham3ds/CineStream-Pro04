import re

file_path = "app/src/main/java/com/example/navigation/AppNavigation.kt"
with open(file_path, "r") as f:
    content = f.read()

# Replace the explicit icon tint and text color with just basic Icon and Text,
# and add complete NavigationDrawerItemDefaults.colors to all items.

# Helper function to find NavigationDrawerItem blocks and replace them.
# Alternatively, I can just use regex for the colors parameter.
# Currently they have:
# colors = NavigationDrawerItemDefaults.colors(
#     selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
#     unselectedContainerColor = Color.Transparent
# ),

import re

def replacer(match):
    full_match = match.group(0)
    # Just replace colors = NavigationDrawerItemDefaults.colors(...) with the correct one
    # We can match `colors = NavigationDrawerItemDefaults.colors([^)]+)`
    new_colors = """colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurface,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurface
                        )"""
    return re.sub(r'colors = NavigationDrawerItemDefaults\.colors\([^)]+\)', new_colors, full_match)

content = re.sub(r'NavigationDrawerItem\([^)]+onClick = \{', replacer, content)

# But `NavigationDrawerItem` blocks contain `{` and `}` (e.g. for label and icon).
# The regex `NavigationDrawerItem\([^)]+` won't work well due to nested parentheses.

# Let's just do a simpler replacement.
content = content.replace("colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),", 
"""colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurface,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurface
                        ),""")

content = content.replace("""colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
                            unselectedContainerColor = Color.Transparent
                        ),""",
"""colors = NavigationDrawerItemDefaults.colors(
                            selectedContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.2f),
                            unselectedContainerColor = Color.Transparent,
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            unselectedIconColor = MaterialTheme.colorScheme.onSurface,
                            unselectedTextColor = MaterialTheme.colorScheme.onSurface
                        ),""")

# Also fix the manual tints
content = re.sub(r'tint = if \(currentRoute == [^)]+\) MaterialTheme\.colorScheme\.primary else MaterialTheme\.colorScheme\.on[a-zA-Z]+', 'tint = androidx.compose.ui.graphics.Color.Unspecified', content)
content = content.replace('tint = MaterialTheme.colorScheme.onSurface', 'tint = androidx.compose.ui.graphics.Color.Unspecified')
content = content.replace('color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp', 'fontSize = 16.sp')

with open(file_path, "w") as f:
    f.write(content)
