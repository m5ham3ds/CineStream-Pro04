import re

with open('app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt', 'r') as f:
    text = f.read()

# We need to replace the content of `if (selectedCategory == "Movies") { ... }` with the new order.
# Let's find the boundaries of the "Movies" content block. We know it starts with `if (selectedCategory == "Movies") {` and ends near the end of the file or before another block if any. Actually, there's no other category in MoviesScreen since `selectedCategory` logic was copied from HomeScreen and partially removed.
# Let's check where it ends.

