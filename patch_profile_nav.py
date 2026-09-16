with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

import re
old_profile_block = re.search(r"composable\(Screen\.Profile\.route\)\s*\{\s*ProfileScreen\(\s*authViewModel\s*=\s*authViewModel,\s*onNavigateToEditProfile\s*=\s*\{\s*navController\.navigate\(Screen\.EditProfile\.route\)\s*\},\s*onNavigateToSettings\s*=\s*\{\s*navController\.navigate\(Screen\.Settings\.route\)\s*\},\s*onNavigateToSecurity\s*=\s*\{\s*navController\.navigate\(Screen\.Security\.route\)\s*\},\s*onNavigateToSubscription\s*=\s*\{\s*navController\.navigate\(Screen\.Subscription\.route\)\s*\}\s*\)\s*\}", content)

if old_profile_block:
    new_profile_block = """composable(Screen.Profile.route) {
                            ProfileScreen(
                                authViewModel = authViewModel,
                                onNavigateToEditProfile = { navController.navigate(Screen.EditProfile.route) },
                                onNavigateToSettings = { navController.navigate(Screen.Settings.route) },
                                onNavigateToSecurity = { navController.navigate(Screen.Security.route) },
                                onNavigateToSubscription = { navController.navigate(Screen.Subscription.route) },
                                onNavigateToHelpSupport = { navController.navigate(Screen.HelpSupport.route) }
                            )
                        }"""
    content = content.replace(old_profile_block.group(0), new_profile_block)
    with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
        f.write(content)
    print("Patched ProfileScreen in AppNavigation")
else:
    print("Could not find ProfileScreen in AppNavigation")
