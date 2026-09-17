import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    c = f.read()

func_addition = """    val handleBackPress = {
        val currentTime = System.currentTimeMillis()
        if (currentTime - lastBackPressTime > 3000) {
            consecutiveBackPresses = 1
        } else {
            consecutiveBackPresses++
        }
        lastBackPressTime = currentTime
        
        if (consecutiveBackPresses >= 3) {
            navController.navigate(Screen.Home.route) {
                popUpTo(Screen.Home.route) { inclusive = true }
            }
            consecutiveBackPresses = 0
        } else {
            if (!navController.popBackStack()) {
                activity?.finish()
            }
        }
    }
    
    BackHandler(enabled = currentRoute != Screen.Home.route && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
        handleBackPress()
    }"""

c = c.replace("""    BackHandler(enabled = currentRoute != Screen.Home.route && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
        val currentTime = System.currentTimeMillis()
        if (currentTime - lastBackPressTime > 3000) {
            consecutiveBackPresses = 1
        } else {
            consecutiveBackPresses++
        }
        lastBackPressTime = currentTime
        
        if (consecutiveBackPresses >= 3) {
            navController.popBackStack(Screen.Home.route, inclusive = false)
            consecutiveBackPresses = 0
        } else {
            if (!navController.popBackStack()) {
                activity?.finish()
            }
        }
    }""", func_addition)

c = c.replace("navController.popBackStack()", "handleBackPress()")

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(c)
