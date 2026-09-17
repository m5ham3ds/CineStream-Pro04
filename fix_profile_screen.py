import re

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    c = f.read()

target = """@Composable
fun ProfileScreen(
    onNavigateToEditProfile: () -> Unit,
    onNavigateToSettings: () -> Unit,
    onNavigateToSecurity: () -> Unit,
    onNavigateToSubscription: () -> Unit,
    onNavigateToHelpSupport: () -> Unit,
    onNavigateToAuth: () -> Unit = {},
    authViewModel: AuthViewModel = viewModel()
) {
    val context = LocalContext.current"""

replacement = """@Composable
fun ProfileScreen(
    onNavigateToEditProfile: () -> Unit,
    onNavigateToSettings: () -> Unit,
    onNavigateToSecurity: () -> Unit,
    onNavigateToSubscription: () -> Unit,
    onNavigateToHelpSupport: () -> Unit,
    onNavigateToAuth: () -> Unit = {},
    authViewModel: AuthViewModel = viewModel()
) {
    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(600)
        isLoading = false
    }
    if (isLoading) {
        com.example.ui.components.ProfileScreenSkeleton()
        return
    }

    val context = LocalContext.current"""

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(c)

