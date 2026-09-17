import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    c = f.read()

c = c.replace("!handleBackPress()", "!navController.popBackStack()")

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(c)

