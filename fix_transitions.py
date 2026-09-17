import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    c = f.read()

target = """            NavHost(
                navController = navController,
                startDestination = Screen.Splash.route,
                modifier = navHostModifier,
                enterTransition = { androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) },
                exitTransition = { androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) },
                popEnterTransition = { androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) },
                popExitTransition = { androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)) }
            ) {"""

replacement = """            // Define Top-Level Routes that should use simple crossfade instead of slide
            val topLevelRoutes = listOf(
                Screen.Home.route, Screen.Movies.route, Screen.Search.route, 
                Screen.Series.route, Screen.Anime.route, Screen.Library.route, 
                Screen.Profile.route, Screen.Downloads.route, Screen.Settings.route, 
                Screen.Extensions.route, Screen.Share.route, Screen.About.route, 
                Screen.Social.route, Screen.Splash.route, Screen.Onboarding.route, Screen.Auth.route
            )

            NavHost(
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

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(c)

