import re

def replace_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Add imports if missing
    if "import com.example.R" not in content:
        content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport com.example.R\nimport androidx.compose.ui.res.stringResource")
    
    # Replace colors
    content = content.replace("Color(0xFFFF0033)", "MaterialTheme.colorScheme.primary")
    
    # String replacements in SplashScreen
    if "SplashScreen.kt" in filepath:
        content = content.replace('"Your Cinematic World,\\nAnytime, Anywhere."', "stringResource(R.string.slogan1)")
        content = content.replace('"Movies"', 'stringResource(R.string.movies)')
        content = content.replace('"Series"', 'stringResource(R.string.category_series)')
        content = content.replace('"Anime"', 'stringResource(R.string.category_anime)')
        content = content.replace('"GOOD STORIES NEVER END"', 'stringResource(R.string.good_stories_never_end)')

    # String replacements in OnboardingScreen
    if "OnboardingScreen.kt" in filepath:
        content = content.replace('"Welcome to"', 'stringResource(R.string.welcome_to)')
        content = content.replace('"Your ultimate destination for\\nmovies and series. Enjoy endless\\nentertainment, anytime, anywhere."', 'stringResource(R.string.slogan2)')
        content = content.replace('"Next"', 'stringResource(R.string.onboarding_next)')
        content = content.replace('"Get Started"', 'stringResource(R.string.onboarding_get_started)')
        content = content.replace('"Already have an account? "', 'stringResource(R.string.already_have_account) + " "')
        content = content.replace('"Sign In"', 'stringResource(R.string.sign_in)')
        content = content.replace('"GOOD\\nSTORIES\\nNEVER\\nEND"', 'stringResource(R.string.good_stories_never_end).replace(" ", "\\n")')
        content = content.replace('"MOVIES\\nSERIES\\nANIME"', '(stringResource(R.string.movies) + "\\n" + stringResource(R.string.category_series) + "\\n" + stringResource(R.string.category_anime)).uppercase()')
        content = content.replace('"HD Quality"', 'stringResource(R.string.hd_quality)')
        content = content.replace('"Movies & Series"', 'stringResource(R.string.movies_and_series)')
        content = content.replace('"Anytime,\\nAnywhere"', 'stringResource(R.string.anytime_anywhere)')
        
        # Download text is complex since "Offline" has a different color
        content = content.replace('append("Download & Watch ")', 'append(stringResource(R.string.download_watch_offline).substringBefore("Offline"))')
        content = content.replace('append("Offline")', 'append("Offline")') # Offline is part of the translation, let's just keep it simple, or better yet, since it's hardcoded style, let's extract the pieces. Actually `stringResource(R.string.download_watch_offline)` is "Download & Watch Offline". We can do `append(stringResource(R.string.download_watch_offline).split("Offline")[0])` and `append("Offline")` etc. Let's just hardcode the split.
        content = content.replace('"Download any movie or episode\\nand watch it offline anytime."', 'stringResource(R.string.download_any_movie_offline)')
        
        content = content.replace('"Personalized\\nRecommendations"', 'stringResource(R.string.personalized_recommendations)')
        content = content.replace('"Your Favorite\\nGenres"', 'stringResource(R.string.your_favorite_genres)')
        content = content.replace('"Build Your\\nWatchlist"', 'stringResource(R.string.build_your_watchlist)')
        
        content = content.replace('append("Personalized ")', 'append(stringResource(R.string.personalized_for_you).substringBefore("for You"))')
        content = content.replace('append("for You")', 'append("for You")')
        content = content.replace('"Get recommendations tailored\\nto your taste."', 'stringResource(R.string.get_recommendations_tailored)')
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

replace_in_file("app/src/main/java/com/example/ui/screens/splash/SplashScreen.kt")
replace_in_file("app/src/main/java/com/example/ui/screens/onboarding/OnboardingScreen.kt")
print("Done replacements")
