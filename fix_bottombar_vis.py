import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

broken_part = """            bottomBar = {
                if (hasTopBar) {
                    com.example.ui.components.BottomNavBar(navController = navController)
                }
            }"""

fixed_part = """            bottomBar = {
                if (bottomBarRoutes.contains(currentRoute)) {
                    com.example.ui.components.BottomNavBar(navController = navController)
                }
            }"""

if broken_part in text:
    text = text.replace(broken_part, fixed_part)
    with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
        f.write(text)
    print("Fixed BottomBar Visibility!")
else:
    print("Could not find broken part.")

