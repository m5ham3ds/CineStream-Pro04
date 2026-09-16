with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

content = content.replace("authViewModel: AuthViewModel,", "")
content = content.replace("fun ProfileScreen(", "fun ProfileScreen(\n    authViewModel: AuthViewModel = androidx.hilt.navigation.compose.hiltViewModel(),")
content = content.replace("onNavigateToHelpSupport: () -> Unit", "onNavigateToHelpSupport: () -> Unit,\n    onNavigateToAuth: () -> Unit = {}")

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
