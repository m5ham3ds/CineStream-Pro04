import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    c = f.read()

target = """.clickable { /* Handle Notifications */ },"""
replacement = """.clickable { navController.navigate(Screen.Notifications.route) },"""
c = c.replace(target, replacement)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(c)
