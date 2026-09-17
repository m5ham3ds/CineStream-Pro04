with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f: c = f.read()

# Add 1 brace before SeriesDetailsScreen
c = c.replace("    }}\n@Composable\nfun SeriesDetailsScreen", "    }\n    }\n}\n@Composable\nfun SeriesDetailsScreen")

# Add 1 brace before TrailerCard
c = c.replace("    }}\n@Composable\nfun TrailerCard", "    }\n    }\n}\n@Composable\nfun TrailerCard")

# Remove 2 braces from the end
c = c[::-1].replace("}", "", 2)[::-1]

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f: f.write(c)

