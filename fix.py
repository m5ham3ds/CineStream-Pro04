with open("app/src/main/java/com/example/ui/screens/splash/SplashScreen.kt", "r") as f:
    lines = f.read().split('\n')

lines = [line for line in lines if "import com.example.R" not in line and "import androidx.compose.ui.res.stringResource" not in line]

lines.insert(2, "import com.example.R")
lines.insert(2, "import androidx.compose.ui.res.stringResource")

with open("app/src/main/java/com/example/ui/screens/splash/SplashScreen.kt", "w") as f:
    f.write('\n'.join(lines))
