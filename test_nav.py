import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

# Replace the BackHandler
old_back_handler = """    androidx.activity.compose.BackHandler(enabled = true) {
        if (currentRoute == Screen.Home.route) {
            showLogoutDialog = true
        } else {
            navController.navigate(Screen.Home.route) {
                popUpTo(navController.graph.startDestinationId) { inclusive = true }
                launchSingleTop = true
            }
        }
    }"""

new_back_handler = """    var showExitDialog by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
    val backStack by navController.currentBackStack.collectAsState()
    var lastBackStackSize by androidx.compose.runtime.remember { androidx.compose.runtime.mutableIntStateOf(0) }
    var backPressCount by androidx.compose.runtime.remember { androidx.compose.runtime.mutableIntStateOf(0) }
    
    androidx.compose.runtime.LaunchedEffect(backStack.size) {
        if (backStack.size > lastBackStackSize) {
            backPressCount = 0
        }
        lastBackStackSize = backStack.size
    }

    androidx.activity.compose.BackHandler(enabled = true) {
        if (currentRoute == Screen.Home.route) {
            showExitDialog = true
        } else {
            if (backPressCount < 2) {
                backPressCount++
                val popped = navController.popBackStack()
                if (!popped) {
                    showExitDialog = true
                }
            } else {
                backPressCount = 0
                navController.navigate(Screen.Home.route) {
                    popUpTo(navController.graph.startDestinationId) { inclusive = false }
                    launchSingleTop = true
                }
            }
        }
    }"""

text = text.replace(old_back_handler, new_back_handler)

# Add showExitDialog AlertDialog
old_logout_dialog = """        if (showLogoutDialog) {"""

new_logout_dialog = """        if (showExitDialog) {
            AlertDialog(
                onDismissRequest = { showExitDialog = false },
                title = { Text("الخروج من التطبيق") },
                text = { Text("هل أنت متأكد أنك تريد الخروج من التطبيق؟") },
                confirmButton = {
                    TextButton(onClick = {
                        val activity = context as? android.app.Activity
                        activity?.finish()
                    }) { Text("نعم", color = Color.Red) }
                },
                dismissButton = {
                    TextButton(onClick = { showExitDialog = false }) { Text("لا", color = MaterialTheme.colorScheme.onSurface) }
                },
                containerColor = MaterialTheme.colorScheme.surface,
                titleContentColor = MaterialTheme.colorScheme.onSurface,
                textContentColor = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
        if (showLogoutDialog) {"""
        
text = text.replace(old_logout_dialog, new_logout_dialog)

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(text)
