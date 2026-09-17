import re

def move_brace(filepath, marker, count):
    with open(filepath, "r") as f: c = f.read()
    
    # Remove `count` braces from the end of the file
    for _ in range(count):
        c = c[::-1].replace("}", "", 1)[::-1]
    
    # Insert `count` braces before the marker
    c = c.replace(marker, ("    }\n"*count) + marker)
    
    with open(filepath, "w") as f: f.write(c)

move_brace("app/src/main/java/com/example/ui/screens/about/AboutScreen.kt", "@Composable\nfun FeatureCard", 1)
move_brace("app/src/main/java/com/example/ui/screens/share/ShareScreen.kt", "@Composable\nfun RowScope.ContentTypeCard", 1)

# In DetailsScreens.kt, I need to check how many were missing
# I had:
# e: file:///app/src/main/java/com/example/navigation/AppNavigation.kt:80:39 Unresolved reference 'SeriesDetailsScreen'.
# e: file:///app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt:323:29 Unresolved reference 'TrailerCard'.
# e: file:///app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt:925:17 Unresolved reference 'AnimatedDownloadIcon'.
# SeriesDetailsScreen is nested inside MovieDetailsScreen. (needs 1 brace)
# TrailerCard is nested inside SeriesDetailsScreen! wait, TrailerCard is at the bottom of the file!

# Let's see what DetailsScreens.kt looks like.
