import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    c = f.read()

target = "    val navController = rememberNavController()"
replacement = """    val navController = rememberNavController()
    val context = LocalContext.current
    val activity = context as? android.app.Activity
    var consecutiveBackPresses by remember { mutableStateOf(0) }
    var lastBackPressTime by remember { mutableStateOf(0L) }
    
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    BackHandler(enabled = currentRoute != Screen.Home.route && currentRoute != Screen.Splash.route && currentRoute != Screen.Auth.route && currentRoute != Screen.Onboarding.route) {
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
    }
    
    // Reset consecutive counter when navigating forward
    LaunchedEffect(currentRoute) {
        // We only really want to reset if it's a new screen, but this resets on any route change. 
        // We will just let it naturally reset by time (3 seconds).
    }"""
    
c = c.replace(target, replacement)
# missing import for BackHandler
c = c.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.activity.compose.BackHandler")

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(c)

