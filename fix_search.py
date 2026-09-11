import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    text = f.read()

idx = text.find("onMovieClick = {  id -> com.example.utils.AdManager.showInterstitial(context)")
end_idx = text.find("bottomBar = {", idx)

if idx != -1 and end_idx != -1:
    fixed_part = """onMovieClick = {  id -> com.example.utils.AdManager.showInterstitial(context); navController.navigate(Screen.MovieDetails.createRoute(id)) },
                                    onSeriesClick = {  id -> com.example.utils.AdManager.showInterstitial(context); navController.navigate(Screen.SeriesDetails.createRoute(id)) }
                                )
                            }
                        }
                    }
                }
            },
            """
    new_text = text[:idx] + fixed_part + text[end_idx:]
    with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
        f.write(new_text)
    print("Fixed!")
else:
    print("Not found")
