with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f: c = f.read()

# Fix the ambiguity by specifying type
c = c.replace("topLevelRoutes.any { route.startsWith(it) }", "topLevelRoutes.any { r: String -> route.startsWith(r) }")
with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f: f.write(c)
