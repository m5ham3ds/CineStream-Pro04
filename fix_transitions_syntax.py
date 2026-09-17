import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    c = f.read()

target = """            NavHost(
                navController = navController,
                startDestination = Screen.Splash.route,
                modifier = navHostModifier,
                enterTransition = { 
                    val route = targetState.destination.route ?: ""
                    if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {
                        androidx.compose.animation.slideIntoContainer(
                            towards = androidx.compose.animation.AnimatedContentTransitionScope.Towards.Start, 
                            animationSpec = androidx.compose.animation.core.tween(400, easing = androidx.compose.animation.core.FastOutSlowInEasing)
                        ) + androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(400))
                    }
                },
                exitTransition = { 
                    val route = targetState.destination.route ?: ""
                    if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {
                        androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(400))
                    }
                },
                popEnterTransition = { 
                    val route = targetState.destination.route ?: ""
                    if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {
                        androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(400))
                    }
                },
                popExitTransition = { 
                    val route = targetState.destination.route ?: ""
                    if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {
                        androidx.compose.animation.slideOutOfContainer(
                            towards = androidx.compose.animation.AnimatedContentTransitionScope.Towards.End, 
                            animationSpec = androidx.compose.animation.core.tween(400, easing = androidx.compose.animation.core.FastOutSlowInEasing)
                        ) + androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(400))
                    }
                }
            ) {"""

replacement = """            NavHost(
                navController = navController,
                startDestination = Screen.Splash.route,
                modifier = navHostModifier,
                enterTransition = { 
                    val route = targetState.destination.route ?: ""
                    if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {
                        slideIntoContainer(
                            towards = androidx.compose.animation.AnimatedContentTransitionScope.Towards.Start, 
                            animationSpec = androidx.compose.animation.core.tween(400, easing = androidx.compose.animation.core.FastOutSlowInEasing)
                        ) + androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(400))
                    }
                },
                exitTransition = { 
                    val route = targetState.destination.route ?: ""
                    if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {
                        androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(400))
                    }
                },
                popEnterTransition = { 
                    val route = targetState.destination.route ?: ""
                    if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {
                        androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(400))
                    }
                },
                popExitTransition = { 
                    val route = targetState.destination.route ?: ""
                    if (topLevelRoutes.any { route.startsWith(it) }) {
                        androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) 
                    } else {
                        slideOutOfContainer(
                            towards = androidx.compose.animation.AnimatedContentTransitionScope.Towards.End, 
                            animationSpec = androidx.compose.animation.core.tween(400, easing = androidx.compose.animation.core.FastOutSlowInEasing)
                        ) + androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(400))
                    }
                }
            ) {"""

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(c)
