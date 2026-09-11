import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

back_handler = """    androidx.activity.compose.BackHandler(enabled = true) {
        if (currentRoute == Screen.Home.route) {
            showLogoutDialog = true
        } else {
            navController.navigate(Screen.Home.route) {
                popUpTo(navController.graph.startDestinationId) { inclusive = true }
                launchSingleTop = true
            }
        }
    }
"""

if back_handler in text:
    text = text.replace(back_handler, "")
    
    inject_point = "var showLogoutDialog by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }"
    text = text.replace(inject_point, inject_point + "\n" + back_handler)
    
    with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
        f.write(text)
    print("Fixed BackHandler order!")
else:
    print("Could not find back handler.")
