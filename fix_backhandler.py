import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

# I will inject BackHandler into AppNavigation composable.
# Right after: val currentRoute = navBackStackEntry?.destination?.route

inject_point = "val currentRoute = navBackStackEntry?.destination?.route"
back_handler_code = """
    androidx.activity.compose.BackHandler(enabled = true) {
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

if inject_point in text:
    text = text.replace(inject_point, inject_point + "\n" + back_handler_code)
    with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
        f.write(text)
    print("Injected BackHandler!")
else:
    print("Could not find inject point.")
