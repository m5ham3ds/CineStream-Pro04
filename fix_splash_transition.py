import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    c = f.read()

target = """                enterTransition = { 
                    val route = targetState.destination.route ?: ""
                    if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {"""

replacement = """                enterTransition = { 
                    val route = targetState.destination.route ?: ""
                    val initialRoute = initialState.destination.route ?: ""
                    if (initialRoute == Screen.Splash.route && topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(700))
                    } else if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {"""

c = c.replace(target, replacement)

target2 = """                exitTransition = { 
                    val route = targetState.destination.route ?: ""
                    if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {"""

replacement2 = """                exitTransition = { 
                    val route = targetState.destination.route ?: ""
                    val initialRoute = initialState.destination.route ?: ""
                    if (initialRoute == Screen.Splash.route) {
                        androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(700))
                    } else if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {"""

c = c.replace(target2, replacement2)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(c)

