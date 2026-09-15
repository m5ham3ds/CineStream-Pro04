import re
with open("app/src/main/res/values/strings.xml", "r", encoding="utf-8") as f:
    content = f.read()

new_strings = """
    <string name="onboarding_next">Next</string>
    <string name="onboarding_get_started">Get Started</string>
    <string name="already_have_account">Already have an account?</string>
    <string name="good_stories_never_end">GOOD STORIES NEVER END</string>
    <string name="hd_quality">HD Quality</string>
    <string name="movies_and_series">Movies &amp; Series</string>
    <string name="anytime_anywhere">Anytime,\nAnywhere</string>
    <string name="download_watch_offline">Download &amp; Watch Offline</string>
    <string name="download_any_movie_offline">Download any movie or episode\nand watch it offline anytime.</string>
    <string name="personalized_recommendations">Personalized\nRecommendations</string>
    <string name="your_favorite_genres">Your Favorite\nGenres</string>
    <string name="build_your_watchlist">Build Your\nWatchlist</string>
    <string name="personalized_for_you">Personalized for You</string>
    <string name="get_recommendations_tailored">Get recommendations tailored\nto your taste.</string>
    <string name="welcome_to_cinestream">Welcome to CineStream</string>
</resources>
"""

content = content.replace("</resources>", new_strings)

with open("app/src/main/res/values/strings.xml", "w", encoding="utf-8") as f:
    f.write(content)
