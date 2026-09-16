with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.hilt.navigation.compose.hiltViewModel", "import androidx.lifecycle.viewmodel.compose.viewModel")
content = content.replace("authViewModel: AuthViewModel = hiltViewModel()", "authViewModel: AuthViewModel = viewModel()")

with open("app/src/main/java/com/example/ui/screens/profile/ProfileScreen.kt", "w") as f:
    f.write(content)
