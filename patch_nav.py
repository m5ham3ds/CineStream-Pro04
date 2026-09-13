with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

import_str = "import com.example.ui.components.swipeToNavigate"
if import_str not in content:
    content = content.replace("import com.example.navigation.Screen", "import com.example.navigation.Screen\n" + import_str)

# Find the NavHost creation
old_navhost = '''val navHostModifier = if (hasTopBar) {
                Modifier.padding(innerPadding).consumeWindowInsets(innerPadding)
            } else {
                Modifier.padding(innerPadding).consumeWindowInsets(innerPadding).then(Modifier.windowInsetsPadding(WindowInsets.statusBars).consumeWindowInsets(WindowInsets.statusBars))
            }'''

new_navhost = '''val pagerRoutes = listOf(Screen.Home.route, Screen.Movies.route, Screen.Search.route, Screen.Series.route, Screen.Anime.route)
            val baseNavHostModifier = if (hasTopBar) {
                Modifier.padding(innerPadding).consumeWindowInsets(innerPadding)
            } else {
                Modifier.padding(innerPadding).consumeWindowInsets(innerPadding).then(Modifier.windowInsetsPadding(WindowInsets.statusBars).consumeWindowInsets(WindowInsets.statusBars))
            }
            
            val navHostModifier = if (pagerRoutes.contains(currentRoute)) {
                baseNavHostModifier.swipeToNavigate(
                    onSwipeLeft = {
                        val idx = pagerRoutes.indexOf(currentRoute)
                        if (idx < pagerRoutes.size - 1) {
                            navController.navigate(pagerRoutes[idx + 1]) {
                                popUpTo(Screen.Home.route) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    },
                    onSwipeRight = {
                        val idx = pagerRoutes.indexOf(currentRoute)
                        if (idx > 0) {
                            navController.navigate(pagerRoutes[idx - 1]) {
                                popUpTo(Screen.Home.route) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    }
                )
            } else {
                baseNavHostModifier
            }'''

if old_navhost in content:
    content = content.replace(old_navhost, new_navhost)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
