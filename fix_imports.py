import re

for filename in ["app/src/main/java/com/example/ui/screens/movies/MoviesViewModel.kt", "app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt"]:
    with open(filename, "r") as f:
        content = f.read()
    
    # Remove the invalid import at the very top
    content = content.replace("import kotlinx.coroutines.flow.map\npackage", "package")
    
    # Insert it after the package declaration
    content = re.sub(r"(package .+?\n)", r"\1import kotlinx.coroutines.flow.map\n", content)
    
    with open(filename, "w") as f:
        f.write(content)

