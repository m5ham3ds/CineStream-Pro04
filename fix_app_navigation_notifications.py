import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    c = f.read()

# Add Notifications to topLevelRoutes
target = "Screen.Social.route, Screen.Splash.route, Screen.Onboarding.route, Screen.Auth.route"
replacement = "Screen.Social.route, Screen.Splash.route, Screen.Onboarding.route, Screen.Auth.route, Screen.Notifications.route"
c = c.replace(target, replacement)

# Pass onNotificationsClick to CineStreamHeader
# We need to find `com.example.ui.components.CineStreamHeader(`
header_target = """                                    com.example.ui.components.CineStreamHeader(
                                        onProfileClick = {
                                            if (userPrefs.isGuest.firstOrNull() == true) {
                                                navController.navigate(Screen.Auth.route)
                                            } else {
                                                navController.navigate(Screen.Profile.route)
                                            }
                                        },
                                        onSearchClick = { navController.navigate(Screen.Search.route) },
                                        onMenuClick = { coroutineScope.launch { drawerState.open() } }
                                    )"""

header_replacement = """                                    com.example.ui.components.CineStreamHeader(
                                        onProfileClick = {
                                            if (userPrefs.isGuest.firstOrNull() == true) {
                                                navController.navigate(Screen.Auth.route)
                                            } else {
                                                navController.navigate(Screen.Profile.route)
                                            }
                                        },
                                        onSearchClick = { navController.navigate(Screen.Search.route) },
                                        onMenuClick = { coroutineScope.launch { drawerState.open() } },
                                        onNotificationsClick = { navController.navigate(Screen.Notifications.route) }
                                    )"""

if header_target in c:
    c = c.replace(header_target, header_replacement)

# Add Notifications Composable
composable_target = """                composable(Screen.Downloads.route) {
                    com.example.ui.screens.downloads.DownloadsScreen(
                        onNavigateToHome = { navController.navigate(Screen.Home.route) },
                        onItemClick = { id, isMovie -> 
                            if (isMovie) {
                                navController.navigate(Screen.MovieDetails.createRoute(id))
                            } else {
                                navController.navigate(Screen.SeriesDetails.createRoute(id))
                            }
                        }
                    )
                }"""
                
composable_replacement = composable_target + """
                composable(Screen.Notifications.route) {
                    com.example.ui.screens.notifications.NotificationsScreen(
                        onBack = { navController.popBackStack() }
                    )
                }"""

if composable_target in c:
    c = c.replace(composable_target, composable_replacement)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(c)
