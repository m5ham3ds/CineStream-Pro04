import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

broken_part = "val bottomBarRoutes = listOf(Screen.Home.route, Screen.Library.route, Screen.Search.route, Screen.Extensions.route, Screen.Social.route)"
fixed_part = "val bottomBarRoutes = listOf(Screen.Home.route, Screen.Movies.route, Screen.Search.route, Screen.Series.route, Screen.Anime.route)"

if broken_part in text:
    text = text.replace(broken_part, fixed_part)
    with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
        f.write(text)
    print("Fixed BottomBar Routes!")
else:
    print("Could not find broken part.")

