import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    c = f.read()

c = c.replace("androidx.compose.animation.AnimatedContentTransitionScope.Towards.Start", "androidx.compose.animation.AnimatedContentTransitionScope.SlideDirection.Start")
c = c.replace("androidx.compose.animation.AnimatedContentTransitionScope.Towards.End", "androidx.compose.animation.AnimatedContentTransitionScope.SlideDirection.End")
c = c.replace("towards =", "towards =") # it's actually `towards` parameter

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(c)
