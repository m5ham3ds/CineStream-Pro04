with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

import re

# Find the Help & Support drawer item block
match = re.search(r"NavigationDrawerItem\(\s*icon = \{ Icon\(Icons\.AutoMirrored\.Filled\.Help.*?onClick = \{ scope\.launch \{ drawerState\.close\(\) \} \},", content, re.DOTALL)
if match:
    old_block = match.group(0)
    new_block = old_block.replace("onClick = { scope.launch { drawerState.close() } },", "onClick = { navController.navigate(Screen.HelpSupport.route); scope.launch { drawerState.close() } },")
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
        f.write(content)
    print("Patched drawer navigation")
else:
    print("Could not find drawer item")
