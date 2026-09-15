import re
with open("app/src/main/java/com/example/ui/screens/splash/SplashScreen.kt", "r") as f:
    content = f.read()

content = content.replace("SplashCard(iconRes = R.drawable.ic_movie_placeholder, text = \"Movies\")", "SplashCard(icon = Icons.Default.Movie, text = \"Movies\")")
content = content.replace("SplashCard(iconRes = R.drawable.ic_series_placeholder, text = \"Series\")", "SplashCard(icon = Icons.Default.Tv, text = \"Series\")")
content = content.replace("SplashCard(iconRes = R.drawable.ic_anime_placeholder, text = \"Anime\")", "SplashCard(icon = Icons.Default.Face, text = \"Anime\")")

content = content.replace("fun SplashCard(iconRes: Int, text: String)", "fun SplashCard(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String)")
content = content.replace("painter = painterResource(id = iconRes)", "imageVector = icon")

content = "import androidx.compose.material.icons.filled.Movie\nimport androidx.compose.material.icons.filled.Tv\nimport androidx.compose.material.icons.filled.Face\n" + content

with open("app/src/main/java/com/example/ui/screens/splash/SplashScreen.kt", "w") as f:
    f.write(content)

