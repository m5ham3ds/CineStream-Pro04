import re

# Fix HomeScreen.kt
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    c = f.read()
c = c.replace('contentDescription = "See All"', 'contentDescription = stringResource(R.string.see_all)')
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(c)
    
# Fix LibraryScreen.kt
with open("app/src/main/java/com/example/ui/screens/library/LibraryScreen.kt", "r") as f:
    c = f.read()
c = c.replace('contentDescription = "Empty"', 'contentDescription = stringResource(R.string.empty)')
with open("app/src/main/java/com/example/ui/screens/library/LibraryScreen.kt", "w") as f:
    f.write(c)

