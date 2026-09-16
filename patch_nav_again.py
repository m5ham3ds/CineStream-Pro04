with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

import re
old_profile_block = re.search(r"composable\(Screen\.Profile\.route\)\s*\{\s*ProfileScreen\([^)]+\)\s*\}", content)

if old_profile_block:
    new_profile_block = """composable(Screen.Profile.route) {
                ProfileScreen(
                    onNavigateToAuth = {
                        navController.navigate(Screen.Auth.route) { popUpTo(0) }
                    },
                    onNavigateToEditProfile = {
                        navController.navigate(Screen.EditProfile.route)
                    },
                    onNavigateToSettings = {
                        navController.navigate(Screen.Settings.route)
                    },
                    onNavigateToSecurity = {
                        navController.navigate(Screen.Security.route)
                    },
                    onNavigateToSubscription = {
                        navController.navigate(Screen.Subscription.route)
                    },
                    onNavigateToHelpSupport = {
                        navController.navigate(Screen.HelpSupport.route)
                    }
                )
            }"""
    content = content.replace(old_profile_block.group(0), new_profile_block)
    with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
        f.write(content)
    print("Patched AppNavigation successfully.")
else:
    print("Could not match ProfileScreen block in AppNavigation.")
