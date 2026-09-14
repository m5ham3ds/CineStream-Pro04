import re

file_path = "app/src/main/java/com/example/navigation/AppNavigation.kt"
with open(file_path, "r") as f:
    content = f.read()

target_start = """    val hasTopBar = bottomBarRoutes.contains(currentRoute) || currentRoute in listOf(
        Screen.Library.route, Screen.Profile.route, Screen.Downloads.route, Screen.Settings.route, Screen.Extensions.route, Screen.Share.route, Screen.About.route, Screen.Social.route
    )

    ModalNavigationDrawer("""

replacement_start = """    val hasTopBar = bottomBarRoutes.contains(currentRoute) || currentRoute in listOf(
        Screen.Library.route, Screen.Profile.route, Screen.Downloads.route, Screen.Settings.route, Screen.Extensions.route, Screen.Share.route, Screen.About.route, Screen.Social.route
    )

    val currentAppLayoutDirection = LocalLayoutDirection.current
    CompositionLocalProvider(LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {
    ModalNavigationDrawer("""

content = content.replace(target_start, replacement_start)

# Now we need to insert CompositionLocalProvider(LocalLayoutDirection provides currentAppLayoutDirection) { 
# right after ModalNavigationDrawer( ... ) {

target_drawer_end = """                            .padding(16.dp),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(if (isGuest) stringResource(R.string.login) else stringResource(R.string.logout), fontSize = 16.sp)
                        Spacer(modifier = Modifier.width(12.dp))
                        Icon(if (isGuest) Icons.Default.Person else Icons.AutoMirrored.Filled.ExitToApp, contentDescription = "Log", tint = MaterialTheme.colorScheme.primary)
                    }
                }
            }
        }
    ) {"""

replacement_drawer_end = """                            .padding(16.dp),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(if (isGuest) stringResource(R.string.login) else stringResource(R.string.logout), fontSize = 16.sp)
                        Spacer(modifier = Modifier.width(12.dp))
                        Icon(if (isGuest) Icons.Default.Person else Icons.AutoMirrored.Filled.ExitToApp, contentDescription = "Log", tint = MaterialTheme.colorScheme.primary)
                    }
                }
            }
        }
    ) {
        CompositionLocalProvider(LocalLayoutDirection provides currentAppLayoutDirection) {"""

content = content.replace(target_drawer_end, replacement_drawer_end)

target_closing = """            }
        }
    }
}

fun NavGraphBuilder.addAuthGraph(navController: NavHostController) {"""

replacement_closing = """            }
        }
        }
    }
}

fun NavGraphBuilder.addAuthGraph(navController: NavHostController) {"""

# There are multiple closing brackets at the end of the AppNavigation function.
# Let's find exactly the end of `AppNavigation` function

import sys
if target_drawer_end not in content:
    print("Could not find drawer end")
    sys.exit(1)

# Write to a temp file and patch
with open("temp_app_nav.kt", "w") as f:
    f.write(content)
