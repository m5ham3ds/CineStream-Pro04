with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

text = text.replace(
    "onMovieClick = {  id -> com.example.utils.AdManager.showInterstitial(context); navController.navigate(Screen.MovieDetails.createRoute(id)) },",
    "onMovieClick = { id -> \n                                        com.example.utils.AdManager.showInterstitial(context)\n                                        navController.navigate(Screen.MovieDetails.createRoute(id))\n                                    },"
)

text = text.replace(
    "onSeriesClick = {  id -> com.example.utils.AdManager.showInterstitial(context); navController.navigate(Screen.SeriesDetails.createRoute(id)) }",
    "onSeriesClick = { id -> \n                                        com.example.utils.AdManager.showInterstitial(context)\n                                        navController.navigate(Screen.SeriesDetails.createRoute(id))\n                                    }"
)

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(text)
